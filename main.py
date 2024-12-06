from datetime import datetime, timedelta
from log import print_log
from model import *
from arima import execute_arima
import numpy as np # type: ignore
import time
import pytz

def calculate_psd(part_id, date):
    fft_values = get_fft_value(part_id, date)
    values = []
    timestamp = fft_values[0][3]

    for value in fft_values:
        values.append(value[2])

    val = np.array(values)

    # Proses FFT
    fft_result = np.fft.fft(val)
    data = np.abs(fft_result)
    data = data[: len(data)]

    # Memisahkan data langsung menggunakan slicing
    interval_1 = data[:320]
    interval_2 = data[320:640]
    interval_3 = data[640:]

    # Menghitung total PSD untuk setiap interval
    total_psd_interval_1 = float(np.sum(interval_1))
    total_psd_interval_2 = float(np.sum(interval_2))
    total_psd_interval_3 = float(np.sum(interval_3))

    # Menghitung nilai maksimal untuk setiap interval
    max_psd_interval_1 = float(np.max(interval_1))
    max_psd_interval_2 = float(np.max(interval_2))
    max_psd_interval_3 = float(np.max(interval_3))
    psd = float(np.sum(data))

    # Iterasi melalui semua timestamp untuk membuat fitur
    create_feature(part_id, "5765a11a-2f89-45dc-a37b-46d384a1ff9e", psd, timestamp)
    create_feature(part_id, "8baab334-6e63-487d-91ea-cf8cd7f8b88d", total_psd_interval_1, timestamp)
    create_feature(part_id, "9b0b9845-e59b-4b85-9ba3-66ff9cb826b8", total_psd_interval_2, timestamp)
    create_feature(part_id, "a94a2f9a-d798-4e54-8373-ff68f486f266", total_psd_interval_3, timestamp)
    create_feature(part_id, "88a07a75-1f84-4436-bcf0-12739900bf4a", max_psd_interval_1, timestamp)
    create_feature(part_id, "c0e9494d-443e-4515-ba2a-34a15400c551", max_psd_interval_2, timestamp)
    create_feature(part_id, "5cf62522-a140-4b26-bbfb-d76e4ae10a81", max_psd_interval_3, timestamp)

    print(f"Total data for part {part_id}: {len(fft_values)} processed successfully.")
    print_log(f"Total data for part {part_id}: {len(fft_values)} processed successfully.")

  
    

def index():
  while True:
    date = datetime.now(pytz.timezone("Asia/Jakarta"))

    tags = get_vibration_parts()
    for tag in tags:
      calculate_psd(tag[0], date)

    for tag in tags:
      execute_arima(tag[0], "8baab334-6e63-487d-91ea-cf8cd7f8b88d")
      execute_arima(tag[0], "9b0b9845-e59b-4b85-9ba3-66ff9cb826b8")
      execute_arima(tag[0], "a94a2f9a-d798-4e54-8373-ff68f486f266")
      execute_arima(tag[0], "88a07a75-1f84-4436-bcf0-12739900bf4a")
      execute_arima(tag[0], "c0e9494d-443e-4515-ba2a-34a15400c551")
      execute_arima(tag[0], "5cf62522-a140-4b26-bbfb-d76e4ae10a81")

    
      
    next_execution = (datetime.now(pytz.timezone("Asia/Jakarta")).replace(hour=4, minute=0, second=0, microsecond=0) + timedelta(days=1))
    wait_time = (next_execution - datetime.now(pytz.timezone("Asia/Jakarta"))).total_seconds()

    print(f"Next execution will be at {next_execution.strftime('%Y-%m-%d %H:%M:%S')}")
    print_log(f"Next execution will be at {next_execution.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(wait_time)



if __name__ == "__main__":
  index()