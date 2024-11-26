import pytz
import uuid
from datetime import datetime
from log import print_log
from database import *

def get_fft_value(tag, date):
    conn = None
    try:
        conn = getConnection()
        with conn.cursor() as cur:
            query = """SELECT id, tag_id, value, created_at
            FROM dl_fft_fetch 
            WHERE tag_id = %s
            AND created_at::date = %s::date
            """
            cur.execute(query, (tag, date.strftime("%Y-%m-%dT%H:%M:%SZ")))
            result = cur.fetchall()
        return result
    except Exception as e:
        print("An exception occurred:", e)
        print_log(f"An exception occurred:{e}")
        return None
    finally:
        if conn:
            conn.close()

def create_feature(equipment_id, feature_id, feature_value, date_time):
    conn = None
    try:
        # Mendapatkan koneksi ke database
        conn = get_main_connection()
        if conn is None:
            raise Exception("Database connection failed.")

        # Waktu sekarang di zona waktu Asia/Jakarta
        now = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%dT%H:%M:%SZ")

        # UUID untuk kolom ID
        unique_id = str(uuid.uuid4())

        # Query SQL untuk insert
        query = """
        INSERT INTO dl_features_data_backup (
            id, equipment_id, features_id, date_time, value, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Pastikan `date_time` adalah objek datetime
        if not isinstance(date_time, datetime):
            raise ValueError("`date_time` must be a datetime object.")

        # Data untuk query
        data = (
            unique_id, 
            equipment_id, 
            feature_id, 
            date_time, 
            feature_value, 
            now, 
            now
        )

        # Eksekusi query
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()

        print("Feature created successfully.")
        print_log("Feature created successfully.")
    except Exception as e:
        print("An exception occurred:", e)
        print_log(f"An exception occurred:{e}")
        return None
    finally:
        # Tutup koneksi jika ada
        if conn:
            conn.close()
