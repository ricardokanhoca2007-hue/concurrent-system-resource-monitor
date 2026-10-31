import psutil


def get_cpu_load():
    """
    Retorna a percentagem atual de utilização do CPU.
    """
    return psutil.cpu_percent(interval=None)


def get_free_ram_percentage():
    """
    Retorna a percentagem de memória RAM livre.
    """
    vm = psutil.virtual_memory()
    return vm.available / vm.total * 100


def get_available_disk_percentage(path="C:\\"):
    """
    Retorna a percentagem de espaço livre em disco.
    """
    du = psutil.disk_usage(path)
    return du.free / du.total * 100