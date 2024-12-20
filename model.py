import pytz
import uuid
from datetime import datetime
from log import print_log
from database import *

def get_vibration_parts():
    try:
        conn = get_main_connection()
        cur = conn.cursor()

        query = "SELECT id, web_id, type_id, part_name  FROM pf_parts WHERE type_id = 'b45a04c6-e2e2-465a-ad84-ccefe0f324d2'"

        cur.execute(query)
        parts = cur.fetchall()
        return parts
    except Exception as e:
        print(f'An exception occurred: {e}')
        print_log(f'An exception occurred: {e}')
    finally:
        if conn:
            conn.close()

def get_feature_values(part_id,features_id):
    try:
        conn = get_main_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, part_id, date_time, value 
            FROM dl_features_data
            WHERE part_id = %s AND features_id = %s
            order by date_time asc
            """,
            (part_id, features_id),
        )
        values = cur.fetchall()
        cur.close()
        conn.close()
        print("Data fetched successfully, count: ", len(values))
        return values
    except Exception as e:
        print_log(f"An exception occurred {e}")
        print(f"An exception occurred {e}")

def get_fft_value(tag, date):
    conn = None
    try:
        conn = getConnection()
        with conn.cursor() as cur:
            query = """SELECT id, part_id, value, created_at
            FROM dl_fft_fetch 
            WHERE part_id = %s
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
        INSERT INTO dl_features_data (
            id, part_id, features_id, date_time, value, created_at, updated_at
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

def create_predict(part_id, features_id, values, timestamps):
    try:
        now = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
        conn = get_main_connection()
        cur = conn.cursor()
        
        # SQL Query
        sql = """
        INSERT INTO dl_predict (id, part_id, features_id, date_time, pfi_value, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s,%s, %s)
        """
        
        # Iterasi dan eksekusi untuk setiap prediksi
        data_to_insert = []
        for value, timestamp in zip(values, timestamps):
            predict_id = str(uuid.uuid4())  # Generate a new UUID for each record
            value = float(value)
            data_to_insert.append((predict_id, part_id, features_id, timestamp, value, "normal", now, now))
        
        # Execute batch insert
        cur.executemany(sql, data_to_insert)
        # Commit perubahan
        conn.commit()
        print_log(f"Predictions successfully saved for equipment_id {part_id}, features_id {features_id}.")
    
    except Exception as e:
        print_log(f"An exception occurred: {e}")
        print(f"An exception occurred: {e}")
    
    finally:
        # Pastikan koneksi ditutup
        if cur:
            cur.close()
        if conn:
            conn.close()


def delete_predicts(part_id, features_id):
    try:
        conn = get_main_connection()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM dl_predict
            WHERE part_id = %s AND features_id = %s
            """,
            (part_id, features_id),
        )
        conn.commit()
        print_log(f"Predictions for part_id {part_id}, features_id {features_id} successfully deleted.")
    except Exception as e:
        print(f"An exception occurred while deleting predicts: {e}")
        print_log(f"An exception occurred: {e}")
