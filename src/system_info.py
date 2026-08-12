"""Recolecta información básica del computador y la guarda en data/system_info.json."""

import ctypes
import json
import os
import platform
import subprocess
import sys
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
JSON_PATH = os.path.join(DATA_DIR, "system_info.json")

CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def _run_wmic(query):
    out = subprocess.check_output(
        ["wmic", "cpu", "get", query], text=True, creationflags=CREATE_NO_WINDOW
    )
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    return lines[1:] if len(lines) > 1 else []


def get_cpu_model():
    try:
        values = _run_wmic("Name")
        if values:
            return values[0]
    except Exception:
        pass
    return platform.processor() or "No disponible"


def get_physical_cores():
    try:
        values = _run_wmic("NumberOfCores")
        if values and values[0].isdigit():
            return int(values[0])
    except Exception:
        pass
    return None


def get_memory_status():
    """Devuelve (ram_total_bytes, ram_libre_bytes) usando la API de Windows."""
    if sys.platform == "win32":
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return stat.ullTotalPhys, stat.ullAvailPhys
    return None, None


def get_total_ram_bytes():
    total, _ = get_memory_status()
    return total


def get_avail_ram_bytes():
    _, disponible = get_memory_status()
    return disponible


def main():
    info = {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "sistema_operativo": platform.system(),
        "sistema_operativo_version": platform.version(),
        "arquitectura": platform.machine(),
        "plataforma": platform.platform(),
        "version_python": platform.python_version(),
        "ejecutable_python": sys.executable,
        "modelo_procesador": get_cpu_model(),
        "nucleos_fisicos": get_physical_cores(),
        "procesadores_logicos": os.cpu_count(),
        "ram_total_bytes": get_total_ram_bytes(),
        "ram_libre_bytes": get_avail_ram_bytes(),
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
