import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Float, Date, DateTime

import os

DB_URI = os.getenv("AIVEN_DB_URI", "postgresql://avnadmin:<PASSWORD_AIVEN_ANDA>@<HOST_AIVEN>:<PORT>/defaultdb?sslmode=require")
engine = create_engine(DB_URI)

# 1. Hapus tabel lama & buat skema tabel jabon_no2 (Target Analisis KNIME)
create_table_sql = """
DROP TABLE IF EXISTS jabon_no2;

CREATE TABLE jabon_no2 (
    id BIGSERIAL PRIMARY KEY,
    date TIMESTAMPTZ NOT NULL,
    feature_index INT DEFAULT 0,
    no2 DOUBLE PRECISION
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()

# 2. Baca CSV NO2 Riil Jabon
df = pd.read_csv('jabon_NO2.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={'NO2': 'no2'})

# 3. Upload tabel jabon_no2 dengan presisi Float 53-bit
dtype_mapping = {
    'no2': Float(precision=53)
}

df.to_sql('jabon_no2', engine, if_exists='append', index=False, dtype=dtype_mapping)
print("✅ Tabel jabon_no2 berhasil diunggah ulang dengan tipe float 53-bit!")

# 4. Upload Tabel Multi-Polutan Mentah (jabon_pollutants_raw) jika berkas ada
try:
    df_raw = pd.read_csv('jabon_pollutants.csv')
    df_raw['date'] = pd.to_datetime(df_raw['date']).dt.date
    df_raw.columns = [c.lower() for c in df_raw.columns]
    raw_dtypes = {c: Float(53) for c in ['no2', 'co', 'hcho', 'so2', 'o3', 'ch4']}
    raw_dtypes['date'] = Date()
    df_raw.to_sql('jabon_pollutants_raw', engine, if_exists='replace', index=False, dtype=raw_dtypes)
    print("✅ Tabel jabon_pollutants_raw (Mentah) berhasil diunggah!")
except Exception as e:
    print("Info raw pollutants:", e)

engine.dispose()
print("🔒 Koneksi database ditutup dengan aman.")