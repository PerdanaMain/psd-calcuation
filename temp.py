from datetime import datetime, timedelta
from model import *
import pytz
import time
import numpy as np # type: ignore

def calculate_psd(tag, date, equipment_id):
    fft_values = get_fft_value(tag, date)
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
    create_feature(equipment_id, "5765a11a-2f89-45dc-a37b-46d384a1ff9e", psd, timestamp)
    create_feature(equipment_id, "8baab334-6e63-487d-91ea-cf8cd7f8b88d", total_psd_interval_1, timestamp)
    create_feature(equipment_id, "9b0b9845-e59b-4b85-9ba3-66ff9cb826b8", total_psd_interval_2, timestamp)
    create_feature(equipment_id, "a94a2f9a-d798-4e54-8373-ff68f486f266", total_psd_interval_3, timestamp)
    create_feature(equipment_id, "88a07a75-1f84-4436-bcf0-12739900bf4a", max_psd_interval_1, timestamp)
    create_feature(equipment_id, "c0e9494d-443e-4515-ba2a-34a15400c551", max_psd_interval_2, timestamp)
    create_feature(equipment_id, "5cf62522-a140-4b26-bbfb-d76e4ae10a81", max_psd_interval_3, timestamp)
       

    print(f"Total data for tag {tag}: {len(fft_values)} processed successfully.")


def index():
    start_date = datetime(2024, 10, 21, tzinfo=pytz.timezone("Asia/Jakarta"))
    current_date = datetime.now(pytz.timezone("Asia/Jakarta"))

    # Tags yang akan dihitung
    tags = [[3871, "b538d5d4-7e3c-46ac-b3f0-c35136317557"],
            [3865, "990fb37b-33c4-44f4-b6a8-cf4b9d3b9c74"],
            [3866, "2462c395-95ee-49b3-8abb-dc8dd67276bc"],
            [3870, "8294f761-cfd1-44d9-966a-613ab1b89fe9"]
            ]

    while start_date <= current_date:
        # Hitung PSD untuk setiap tag
        for tag in tags:
            calculate_psd(tag[0], start_date, tag[1])

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