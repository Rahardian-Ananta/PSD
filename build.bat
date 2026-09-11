@echo off
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
echo ============================================
echo   Building Jupyter Book...
echo ============================================
jupyter-book build .
echo.
echo ============================================
echo   Build selesai! Buka _build\html\index.html
echo ============================================
pause
