import psutil


class ProcessInfo():
    def __init__(self, pid: int):
        self._process = psutil.Process(pid)

    def get_info(self) -> dict: ...


class LinuxProcessInfo(ProcessInfo):
    def __init__(self, pid: int):
        super().__init__(pid)

    def get_info(self) -> dict:
        info = {
            "cpu_usage": self._process.cpu_percent(),
            "rss": self._process.memory_info().rss,
            "vms": self._process.memory_info().vms,
            "fds": self._process.num_fds(),
        }

        return info


class WinProcessInfo(ProcessInfo):
    def __init__(self, pid: int):
        super().__init__(pid)

    def get_info(self) -> dict:
        info = {
            "cpu_usage": self._process.cpu_percent(),
            "wset": self._process.memory_info().wset,
            "private": self._process.memory_info().private,
            "handles": self._process.num_handles(),
        }

        return info
