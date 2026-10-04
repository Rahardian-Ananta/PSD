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

REM === File sefolder 02_data_understanding (tombol 2.1b/2.2/2.7) ===
copy "02_data_understanding\jabon.geojson" "_build\html\02_data_understanding\" >nul
copy "02_data_understanding\jabon_pollutants_data.zip" "_build\html\02_data_understanding\" >nul
copy "02_data_understanding\kamal.geojson" "_build\html\02_data_understanding\" >nul
copy "02_data_understanding\s2_kamal.tif" "_build\html\02_data_understanding\" >nul
copy "02_data_understanding\s2_kamal_metadata.json" "_build\html\02_data_understanding\" >nul
copy "02_data_understanding\ingest_aiven_jabon.py" "_build\html\02_data_understanding\" >nul

REM === File sefolder 04_feature_extraction (tombol 4.2/4.6) ===
copy "04_feature_extraction\CO_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\NO2_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\SO2_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\ALL_Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\All-Pollutants-Jabon_TSFEL.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\All-Pollutants-Jabon_TSFEL_linreg.csv" "_build\html\04_feature_extraction\" >nul
copy "04_feature_extraction\All-Pollutants-Jabon_TSFEL_poly3.csv" "_build\html\04_feature_extraction\" >nul

REM === Peta mandiri 05_clustering (tombol 5.7) ===
copy "05_clustering\peta_clustering_linear.html" "_build\html\05_clustering\" >nul
copy "05_clustering\peta_clustering_poly.html" "_build\html\05_clustering\" >nul
copy "05_clustering\peta_clustering_linear_k2.html" "_build\html\05_clustering\" >nul
copy "05_clustering\peta_clustering_poly_k2.html" "_build\html\05_clustering\" >nul
copy "05_clustering\peta_clustering_linear_interaktif.html" "_build\html\05_clustering\" >nul
copy "05_clustering\peta_clustering_poly_interaktif.html" "_build\html\05_clustering\" >nul

REM === Matriks fitur gabungan (tombol 4.6) ===
mkdir "_build\html\data" 2>nul
copy "data\ekstraksi_fitur_linear.csv" "_build\html\data\" >nul
copy "data\ekstraksi_fitur_polynomial.csv" "_build\html\data\" >nul

REM === Hasil PCA + clustering + klasifikasi (tombol 5.1/5.6/6.1) ===
mkdir "_build\html\data\processed" 2>nul
copy "data\processed\pca_variance.csv" "_build\html\data\processed\" >nul
copy "data\processed\clustering_linear_204.csv" "_build\html\data\processed\" >nul
copy "data\processed\clustering_poly_204.csv" "_build\html\data\processed\" >nul
copy "data\processed\clustering_grid_linear.csv" "_build\html\data\processed\" >nul
copy "data\processed\clustering_grid_poly.csv" "_build\html\data\processed\" >nul
copy "data\processed\best_config_linear.json" "_build\html\data\processed\" >nul
copy "data\processed\best_config_poly.json" "_build\html\data\processed\" >nul
copy "data\processed\labels_best_linear.csv" "_build\html\data\processed\" >nul
copy "data\processed\labels_best_poly.csv" "_build\html\data\processed\" >nul
copy "data\processed\labels_linear_k2.csv" "_build\html\data\processed\" >nul
copy "data\processed\labels_poly_k2.csv" "_build\html\data\processed\" >nul
copy "data\processed\ladder_linear.csv" "_build\html\data\processed\" >nul
copy "data\processed\ladder_poly.csv" "_build\html\data\processed\" >nul
copy "data\processed\sawah_features.csv" "_build\html\data\processed\" >nul
copy "data\processed\sawah_metrics.csv" "_build\html\data\processed\" >nul
copy "data\processed\sawah_classified.tif" "_build\html\data\processed\" >nul
copy "data\processed\sawah_rf.joblib" "_build\html\data\processed\" >nul

REM === GeoJSON + spasial (tombol 5.7/6.1, termasuk 4 geojson besar) ===
mkdir "_build\html\data\spasial" 2>nul
copy "data\spasial\cluster_map_linear.geojson" "_build\html\data\spasial\" >nul
copy "data\spasial\cluster_map_poly.geojson" "_build\html\data\spasial\" >nul
copy "data\spasial\cluster_map_linear_k2.geojson" "_build\html\data\spasial\" >nul
copy "data\spasial\cluster_map_poly_k2.geojson" "_build\html\data\spasial\" >nul
copy "data\spasial\s2_kamal.tif" "_build\html\data\spasial\" >nul
copy "data\spasial\kamal_sawah.shp" "_build\html\data\spasial\" >nul
copy "data\spasial\kamal_sawah.dbf" "_build\html\data\spasial\" >nul
copy "data\spasial\kamal_sawah.shx" "_build\html\data\spasial\" >nul
copy "data\spasial\kamal_sawah.prj" "_build\html\data\spasial\" >nul
copy "data\spasial\kamal_sawah.cpg" "_build\html\data\spasial\" >nul

REM === Hasil PCA per polutan (tombol 5.1) ===
mkdir "_build\html\data\downloads\ekstraksi fitur\pca_results" 2>nul
copy "data\downloads\ekstraksi fitur\pca_results\jabon_pca_35fitur_co.csv" "_build\html\data\downloads\ekstraksi fitur\pca_results\" >nul
copy "data\downloads\ekstraksi fitur\pca_results\jabon_pca_35fitur_so2.csv" "_build\html\data\downloads\ekstraksi fitur\pca_results\" >nul
copy "data\downloads\ekstraksi fitur\pca_results\jabon_pca_37fitur_co.csv" "_build\html\data\downloads\ekstraksi fitur\pca_results\" >nul
copy "data\downloads\ekstraksi fitur\pca_results\jabon_pca_37fitur_no2.csv" "_build\html\data\downloads\ekstraksi fitur\pca_results\" >nul
copy "data\downloads\ekstraksi fitur\pca_results\jabon_pca_37fitur_so2.csv" "_build\html\data\downloads\ekstraksi fitur\pca_results\" >nul

REM === Workflow KNIME (tombol 5.4) ===
copy "data\downloads\Clustering_Data.knwf" "_build\html\data\downloads\" >nul

echo.
echo ============================================
echo   Build selesai! Buka _build\html\index.html
echo ============================================
pause