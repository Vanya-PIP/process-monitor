import csv
import datetime
from pathlib import Path
import platform
from typing import Optional

from .process_info import LinuxProcessInfo, WinProcessInfo
from .repeated_timer import RepeatedTimer
from .utils import find_pid_by_name


class ProcessLogger():
    DATE_FT = "%Y-%m-%d"
    DATETIME_FT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, interval: int, pid: Optional[int] = None,
                 name: Optional[str] = None, log_dir: str = "."):
        if not (pid or name):
            raise ValueError("At least one of pid or name args is required")

        pid = pid if pid else find_pid_by_name(name)
        self._log_dir = Path(log_dir)

        header = ["Time", "CPU usage [%]"]
        if platform.system() == "Windows":
            self._process_info = WinProcessInfo(pid)
            header.extend(["Working Set [bytes]", "Private Bytes [bytes]",
                           "Number of handles"])
        else:
            self._process_info = LinuxProcessInfo(pid)
            header.extend(["Resident Set Size [bytes]",
                           "Virtual Memory Size [bytes]",
                           "Number of file descriptors"])

        self._header = header
        self._repeated_timer = RepeatedTimer(interval, self._run)
        self._current_date = None
        self.exception = None

    def start(self):
        self._repeated_timer.start()

    def stop(self):
        self._repeated_timer.cancel()

    def _run(self):
        try:
            self._setup_current_log()
            self._write()
        except Exception as e:
            self.exception = e
            raise e

    def _setup_current_log(self):
        self._log_dir.mkdir(parents=True, exist_ok=True)

        current_date = datetime.date.today()
        if self._current_date != current_date:
            self._current_date = current_date
            self._current_log = f"{self._current_date.strftime(self.DATE_FT)}.csv"
            self._log_path = self._log_dir / self._current_log
        if not self._log_path.exists():
            with open(self._log_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self._header)

    def _write(self):
        info = self._process_info.get_info()
        current_datetime = datetime.datetime.now().strftime(self.DATETIME_FT)

        line = (current_datetime, *info.values())
        with open(self._log_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(line)
