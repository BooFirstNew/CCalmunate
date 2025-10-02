#!/usr/bin/env python3
import random
import subprocess
import time
from datetime import datetime

# ================== НАСТРОЙКИ ==================
MAX_RUNS = 5            # максимум запусков за день
MIN_SLEEP = 3600        # минимальная пауза между коммитами (1 час)
MAX_SLEEP = 21600       # максимальная пауза (6 часов)
SCRIPT_PATH = "/root/github_auto/main.py"  # путь к твоему скрипту

# ================== ЛОГИ ==================
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# ================== ОСНОВНАЯ ЛОГИКА ==================
def main():
    runs_today = random.randint(0, MAX_RUNS)
    log(f"Сегодня будет выполнено {runs_today} запусков скрипта.")

    for i in range(runs_today):
        log(f"Запуск {i+1}/{runs_today}")
        subprocess.run(["python3", SCRIPT_PATH])
        if i < runs_today - 1:  # после последнего запуска паузы не делаем
            sleep_time = random.randint(MIN_SLEEP, MAX_SLEEP)
            log(f"Следующий запуск через {sleep_time//3600} ч { (sleep_time%3600)//60 } мин")
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()

def show_frequency_response(filter_type: FilterType, samplerate: int) -> None:
    """
    Show frequency response of a filter


def show_phase_response(filter_type: FilterType, samplerate: int) -> None:
    """
    Show phase response of a filter


def process(self, sample: float) -> float:
        """
        Calculate y[n]

