import time
import psutil

process = psutil.Process()

def start_metrics():
    return {
        "time": time.perf_counter()
    }

def end_metrics(start):

    elapsed = (time.perf_counter() - start["time"]) * 1000

    ram = process.memory_info().rss / (1024 * 1024)

    cpu = psutil.cpu_percent(interval=0.05)

    return {
        "time": round(elapsed,2),
        "ram": round(ram,2),
        "cpu": cpu
    }