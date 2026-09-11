@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo ================================================================
echo    PSD - Automated Commit, Push ^& GitHub Pages Deployment
echo    Repository : https://github.com/Rahardian-Ananta/PSD
echo    Live Web   : https://rahardian-ananta.github.io/PSD/
echo ================================================================
echo.

:: 1. Input Pesan Commit
set /p COMMIT_MSG="Masukkan pesan commit (tekan Enter untuk default): "
if "!COMMIT_MSG!"=="" (
    set COMMIT_MSG=Update materi dan dokumentasi Jupyter Book PSD Jabon
)

echo.
echo [1/4] Menambahkan perubahan file ke Git staging...
git add .

echo.
echo [2/4] Melakukan commit...
git commit -m "!COMMIT_MSG!"

echo.
echo [3/4] Melakukan push ke branch main...
git push origin main

echo.
echo [4/4] Mem-build Jupyter Book dan men-deploy ke gh-pages...
jupyter-book build .
if %ERRORLEVEL% equ 0 (
    ghp-import -n -p -f _build/html
    echo.
    echo ================================================================
    echo    SELESAI DENGAN SUKSES!
    echo    - Kode sumber ter-update di  : https://github.com/Rahardian-Ananta/PSD
    echo    - Website statis live di     : https://rahardian-ananta.github.io/PSD/
    echo ================================================================
) else (
    echo.
    echo [PERINGATAN] Build Jupyter Book gagal. Silakan cek pesan error di atas.
)

pause
