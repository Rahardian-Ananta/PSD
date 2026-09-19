import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Float, Date, DateTime

# 1. Konfigurasi Koneksi PostgreSQL Aiven
# Masukkan kredensial Aiven Anda atau set environment variable AIVEN_DB_URI:
DB_URI = os.getenv("AIVEN_DB_URI", "postgresql://avnadmin:<PASSWORD_AIVEN_ANDA>@<HOST_AIVEN>:<PORT>/defaultdb?sslmode=require")
engine = create_engine(DB_URI)

print("🚀 Memulai proses ingest database Aiven untuk Kecamatan Jabon...")

# 2. Ingest Tabel Spesifik jabon_no2 (Untuk Alur KNIME)
no2_path = "data/downloads/jabon_pollutants_data/jabon_NO2.csv"

df_no2 = pd.read_csv(no2_path)
df_no2['date'] = pd.to_datetime(df_no2['date'])
df_no2 = df_no2.rename(columns={'NO2': 'no2'})

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS jabon_no2;"))
    conn.execute(text("""
        CREATE TABLE jabon_no2 (
            id BIGSERIAL PRIMARY KEY,
            date TIMESTAMPTZ NOT NULL,
            feature_index INT DEFAULT 0,
            no2 DOUBLE PRECISION
        );
    """))
    conn.commit()

df_no2.to_sql('jabon_no2', engine, if_exists='append', index=False, dtype={'no2': Float(53)})
print("✅ Tabel jabon_no2 berhasil diunggah!")

# 3. Ingest Tabel Gabungan Multi-Polutan Mentah (jabon_pollutants_raw)
raw_path = "data/downloads/jabon_pollutants_data/jabon_pollutants.csv"

if os.path.exists(raw_path):
    df_raw = pd.read_csv(raw_path)
    df_raw['date'] = pd.to_datetime(df_raw['date']).dt.date
    df_raw.columns = [c.lower() for c in df_raw.columns]
    raw_dtypes = {c: Float(53) for c in ['no2', 'co', 'hcho', 'so2', 'o3', 'ch4']}
    raw_dtypes['date'] = Date()
    df_raw.to_sql('jabon_pollutants_raw', engine, if_exists='replace', index=False, dtype=raw_dtypes)
    print("✅ Tabel jabon_pollutants_raw (Mentah) berhasil diunggah!")

# 4. Ingest Tabel Gabungan Multi-Polutan Bersih (jabon_pollutants_clean)
clean_path = "data/downloads/jabon_clean_data/jabon_pollutants_clean.csv"
if os.path.exists(clean_path):
    df_clean = pd.read_csv(clean_path)
    df_clean['date'] = pd.to_datetime(df_clean['date']).dt.date
    df_clean.columns = [c.lower() for c in df_clean.columns]
    raw_dtypes = {c: Float(53) for c in ['no2', 'co', 'hcho', 'so2', 'o3', 'ch4']}
    raw_dtypes['date'] = Date()
    df_clean.to_sql('jabon_pollutants_clean', engine, if_exists='replace', index=False, dtype=raw_dtypes)
    print("✅ Tabel jabon_pollutants_clean (Bersih) berhasil diunggah!")

engine.dispose()
print("🔒 Seluruh data berhasil diunggah dan koneksi database ditutup dengan aman.")
