import queue
import datetime

CPU_THRESHOLD = 50.0
RAM_FREE_THRESHOLD = 10.0
DISK_FREE_THRESHOLD = 20.0

def now():
    return datetime.datetime.now().isoformat(timespec="milliseconds")


def process_item_and_alerts(item: dict) -> str | None:
    metric = item.get("metric")
    value = item.get("value")
    ts = item.get("ts")

    if metric == "cpu":
        if value is not None and value > CPU_THRESHOLD:
            return f"ALERTA CPU: carga {value:.1f}% > {CPU_THRESHOLD}% @ {ts}"

    elif metric == "ram_free":
        if value is not None and value < RAM_FREE_THRESHOLD:
            return f"ALERTA RAM: {value:.1f}% livre < {RAM_FREE_THRESHOLD}% @ {ts}"

    elif metric == "disk_free":
        path = item.get("path", "C:\\")
        if value is not None and value < DISK_FREE_THRESHOLD:
            return f"ALERTA DISCO: {value:.1f}% livre < {DISK_FREE_THRESHOLD}% em {path} @ {ts}"

    return None


def consumer_loop(consumer_id: int, q: queue.Queue, stop_event, gui=None, gui_print: bool = True):
    # Loop do consumidor: lê a fila até o sistema pedir para parar e a fila ficar vazia
    while not stop_event.is_set() or not q.empty():
        try:
          # Loop do consumidor: lê a fila até o sistema pedir para parar e a fila ficar vazia
            item = q.get(timeout=0.5)
        except queue.Empty:
            continue

        alert = process_item_and_alerts(item)
        if alert:
            if gui_print:
                print(f"[CONSUMIDOR {consumer_id}] >>> {alert}")

            if gui is not None:
                gui.add_alert(alert)

        q.task_done()

    if gui_print:
        print(f"[CONSUMIDOR {consumer_id} terminado @ {now()}]")


__all__ = ["consumer_loop", "process_item_and_alerts"]