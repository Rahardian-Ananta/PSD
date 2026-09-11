import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Float, Integer, DateTime

import os

DB_URI = os.getenv("AIVEN_DB_URI", "postgresql://avnadmin:<PASSWORD_AIVEN_ANDA>@<HOST_AIVEN>:<PORT>/defaultdb?sslmode=require")
engine = create_engine(DB_URI)

# 1. Hapus tabel lama & buat tabel baru dengan tipe NUMERIC/DOUBLE
create_table_sql = """
DROP TABLE IF EXISTS sidoarjo_no2;

CREATE TABLE sidoarjo_no2 (
    id BIGSERIAL PRIMARY KEY,
    date TIMESTAMPTZ NOT NULL,
    feature_index INT DEFAULT 0,
    no2 NUMERIC(15, 10)
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()

# 2. Baca CSV
df = pd.read_csv('sidoarjo_NO2.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={'NO2': 'no2'})

# 3. Upload dengan mapping tipe data eksplisit
dtype_mapping = {
    'no2': Float(precision=53)
}

df.to_sql('sidoarjo_no2', engine, if_exists='append', index=False, dtype=dtype_mapping)

print("Data berhasil diunggah ulang dengan tipe float 53-bit!")