import argparse
import queue
import threading
import time
import concurrent.futures

from producers import cpu_producer, ram_producer, disk_producer
from consumers import consumer_loop
from resource_monitor_gui import ResourceMonitorGUI


def supervisor(stop_event, prod_pool, cons_pool,
               producers_futures, consumers_futures,
               q, verbose, disk_path, num_consumers, gui):

    while not stop_event.is_set():
        time.sleep(1) 

        # Verificar produtores
        for i, future in enumerate(producers_futures):
            if future.done():
                print("[SUPERVISOR] Produtor falhou → reiniciando...")

                if i == 0:
                    producers_futures[i] = prod_pool.submit(cpu_producer, q, stop_event, 0.1, verbose)
                elif i == 1:
                    producers_futures[i] = prod_pool.submit(ram_producer, q, stop_event, 0.1, verbose)
                elif i == 2:
                    producers_futures[i] = prod_pool.submit(disk_producer, q, stop_event, disk_path, 0.1, verbose)

        # verificar consumidores
        for i, future in enumerate(consumers_futures):
            if future.done():
                print(f"[SUPERVISOR] Consumidor {i+1} falhou → reiniciando...")

                consumers_futures[i] = cons_pool.submit(
                    consumer_loop, i + 1, q, stop_event, gui, True
                )


def main(consumers, queue_size, duration, verbose, disk_path):

    # Fila partilhada entre produtores e consumidores
    q = queue.Queue(maxsize=queue_size)

    stop_event = threading.Event()

    gui = ResourceMonitorGUI(stop_event)

    # Fecho automático
    if duration is not None:
        gui.root.after(int(duration * 1000), gui.close)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as prod_pool, \
         concurrent.futures.ThreadPoolExecutor(max_workers=consumers) as cons_pool:

        # ===== PRODUTORES =====
        producers_futures = [
            prod_pool.submit(cpu_producer, q, stop_event, 0.1, verbose),
            prod_pool.submit(ram_producer, q, stop_event, 0.1, verbose),
            prod_pool.submit(disk_producer, q, stop_event, disk_path, 0.1, verbose),
        ]

        # ===== CONSUMIDORES =====
        consumers_futures = []
        for i in range(consumers):
            future = cons_pool.submit(consumer_loop, i + 1, q, stop_event, gui, True)
            consumers_futures.append(future)

        # ===== THREAD DAEMON =====
        threading.Thread(target=supervisor,
            args=(stop_event, prod_pool, cons_pool,
                  producers_futures, consumers_futures,
                  q, verbose, disk_path, consumers, gui),
            daemon=True
        ).start()

        gui.start()

        # Após fechar GUI para tudo
        stop_event.set()
        q.join()

    print("Encerrado. Obrigado por usar o monitor de sistema!")


# ARGUMENTOS DE EXECUÇÃO
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitorização de recursos com produtores/consumidores")

    # Número de consumidores
    parser.add_argument("--consumers", type=int, default=2, help="Número de consumidores")

    # Tamanho máximo da fila partilhada
    parser.add_argument("--queue-size", type=int, default=100, help="Tamanho máximo da fila")

    # Duração opcional do programa
    parser.add_argument("--duration", type=float, default=None, help="Duração em segundos (omitido = indefinido)")

    # Mostra mensagens dos produtores
    parser.add_argument("--verbose", action="store_true", help="Ativa mensagens dos produtores")

    # Caminho do disco a monitorizar
    parser.add_argument("--disk-path", type=str, default="C:\\", help="Caminho do disco a monitorizar")

    args = parser.parse_args()

    main(args.consumers, args.queue_size, args.duration, args.verbose, args.disk_path)