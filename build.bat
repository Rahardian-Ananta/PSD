@echo off
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
echo ============================================
echo   Building Jupyter Book...
echo ============================================
jupyter-book build .
if %errorlevel% neq 0 (
    echo Build gagal!
    pause
    exit /b 1
)
echo.
echo ============================================
echo   Copying download files...
echo ============================================

REM === Copy TSFEL CSV untuk 4.2_ekstraksi_fitur_tsfel ===
copy "04_feature_extraction\CO_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\NO2_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\SO2_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\ALL_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul

REM === Create data/downloads folders ===
mkdir "_build\html\data\downloads\jabon_clean_data" 2>nul
mkdir "_build\html\data\downloads\jabon_pollutants_data" 2>nul

REM === Copy clean data untuk 3.4_validasi_data_bersih ===
copy "data\downloads\jabon_clean_data\jabon_NO2_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_CO_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_HCHO_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_SO2_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_O3_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_CH4_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul
copy "data\downloads\jabon_clean_data\jabon_pollutants_clean.csv" "_build\html\data\downloads\jabon_clean_data\" >nul

REM === Copy raw data untuk 2.2_deskripsi_dataset ===
copy "data\downloads\jabon_pollutants_data\jabon_NO2.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_CO.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_HCHO.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_SO2.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_O3.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_CH4.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_pollutants.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon_pollutants_data\jabon_pollutants_rolling30.csv" "_build\html\data\downloads\jabon_pollutants_data\" >nul
copy "data\downloads\jabon.geojson" "_build\html\data\downloads\" >nul

echo.
echo ============================================
echo   Build selesai! Buka _build\html\index.html
echo ============================================
pause