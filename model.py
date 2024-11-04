from database import getConnection

def get_fft_value(tag, date):
    conn = None
    try:
        conn = getConnection()
        with conn.cursor() as cur:
            query = """SELECT id, tag_id, value 
            FROM dl_fft_fetch 
            WHERE tag_id = %s
            AND created_at::date = %s::date
            """
            cur.execute(query, (tag, date.strftime("%Y-%m-%dT%H:%M:%SZ")))
            result = cur.fetchall()
        return result
    except Exception as e:
        print("An exception occurred:", e)
        return None
    finally:
        if conn:
            conn.close()

def create_features(
      tag_id,
      psd,
      total_psd_interval_1,
      total_psd_interval_2,
      total_psd_interval_3,
      max_psd_interval_1,
      max_psd_interval_2,
      max_psd_interval_3,
      date
    ):
    conn = None
    try:
        conn = getConnection()
        
        query = """
        INSERT INTO dl_psd_value (
            tag_id, psd_value, total_value_1, total_value_2, total_value_3,
            max_value_1, max_value_2, max_value_3, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Data untuk satu baris
        data = (
            tag_id, psd, total_psd_interval_1, total_psd_interval_2, total_psd_interval_3,
            max_psd_interval_1, max_psd_interval_2, max_psd_interval_3, date.strftime("%Y-%m-%dT%H:%M:%SZ"), date.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        
        cur = conn.cursor()
        cur.execute(query, data)  # Gunakan `execute` untuk satu set data
        conn.commit()
        cur.close()
    except Exception as e:
        print("An exception occurred:", e)
        return None
    finally:
        if conn:
            conn.close()
