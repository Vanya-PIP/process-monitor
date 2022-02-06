from pathlib import Path
from typing import Optional

import psutil


def find_pid_by_name(name: str) -> Optional[int]:
    name = name.lower()
    for proc in psutil.process_iter():
        try:
            proc_name = proc.name().lower()
            exe = Path(proc.exe()).name.lower().removesuffix(".exe")
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue
        if name == proc_name or name == exe:
            return proc.pid
    else:
        raise ValueError(f"Process {name} not found")
