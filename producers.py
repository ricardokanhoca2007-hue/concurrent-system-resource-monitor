import time
import datetime
import queue

from resource_monitor_utils import (
    get_cpu_load,
    get_free_ram_percentage,
    get_available_disk_percentage,
)

SAMPLE_INTERVAL = 0.1


def _now():
    return datetime.datetime.now().isoformat(timespec="milliseconds")


def cpu_producer(q: queue.Queue, stop_event, interval: float = SAMPLE_INTERVAL, verbose: bool = False):
    # Produtor do CPU: corre em loop até receber sinal para parar
    while not stop_event.is_set():
    # Vai buscar a carga atual do CPU ao módulo de recursos    
        value = get_cpu_load()
        # Cria a mensagem a colocar na fila
        item = {"metric": "cpu", "value": value, "ts": _now()}

        try:
            q.put(item, timeout=0.05)
            if verbose:
                print(f"[PROD CPU] {value:.1f}% @ {item['ts']}")
        except queue.Full:
             # Se a fila estiver cheia, o valor é descartado para evitar bloqueio
            if verbose:
                print(f"[PROD CPU] fila cheia - sample descartado @ {_now()}")

        time.sleep(interval)


def ram_producer(q: queue.Queue, stop_event, interval: float = SAMPLE_INTERVAL, verbose: bool = False):
    # Produtor da RAM: corre em loop até receber sinal para parar
    while not stop_event.is_set():
        free_pct = get_free_ram_percentage()
        item = {"metric": "ram_free", "value": free_pct, "ts": _now()}

        try:
            q.put(item, timeout=0.05)
            if verbose:
                print(f"[PROD RAM] {free_pct:.1f}% livre @ {item['ts']}")
        except queue.Full:
            if verbose:
                print(f"[PROD RAM] fila cheia - sample descartado @ {_now()}")

        time.sleep(interval)


def disk_producer(q: queue.Queue, stop_event, path: str = "C:\\", interval: float = SAMPLE_INTERVAL, verbose: bool = False):
    # Produtor do disco: corre em loop até receber sinal para parar
    while not stop_event.is_set():
        free_pct = get_available_disk_percentage(path)
        item = {"metric": "disk_free", "value": free_pct, "ts": _now(), "path": path}

        try:
            q.put(item, timeout=0.05)
            if verbose:
                print(f"[PROD DISK] {free_pct:.1f}% livre ({path}) @ {item['ts']}")
        except queue.Full:
            if verbose:
                print(f"[PROD DISK] fila cheia - sample descartado @ {_now()}")

        time.sleep(interval)


__all__ = ["cpu_producer", "ram_producer", "disk_producer"]