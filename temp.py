from datetime import datetime, timedelta
from model import *
from main import calculate_psd
import pytz
import numpy as np # type: ignore


def index():
    start_date = datetime(2024, 10, 21, tzinfo=pytz.timezone("Asia/Jakarta"))
    current_date = datetime.now(pytz.timezone("Asia/Jakarta"))

    # Tags yang akan dihitung
    tags = get_vibration_parts()

    while start_date <= current_date:
        # Hitung PSD untuk setiap tag
        for tag in tags:
            calculate_psd(tag[0], start_date)

        # Cetak log proses
        print(f"PSD calculated for {start_date.strftime('%Y-%m-%d')}")

        # Pindah ke hari berikutnya
        start_date += timedelta(days=1)

        # Perbarui current_date
        current_date = datetime.now(pytz.timezone("Asia/Jakarta"))

    # next_execution = (datetime.now(pytz.timezone("Asia/Jakarta")).replace(hour=3, minute=0, second=0, microsecond=0)
    #                   + timedelta(days=1))
    # wait_time = (next_execution - datetime.now(pytz.timezone("Asia/Jakarta"))).total_seconds()
    # time.sleep(wait_time)

if __name__ == "__main__":
  index()