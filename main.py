from datetime import datetime, timedelta
from model import get_fft_value, create_features
import numpy as np # type: ignore
import time
import pytz

def calculate_psd(tag,date):
  fft_values = get_fft_value(tag,date)
  values = []
  for value in fft_values:
      values.append(value[2])

  val = np.array(values)

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

  create_features(
      tag,
      psd,
      total_psd_interval_1,
      total_psd_interval_2,
      total_psd_interval_3,
      max_psd_interval_1,
      max_psd_interval_2,
      max_psd_interval_3,
      date=date
  )

  print(f"Total data for tag {tag}: {len(fft_values)} at date {date}")

def index():
  while True:
    date = datetime.now(pytz.timezone("Asia/Jakarta"))

    tags = [3871,3865,3866,3870]
    for tag in tags:
      calculate_psd(tag,date)
      
    time.sleep(86400 - 18000)



if __name__ == "__main__":
  index()