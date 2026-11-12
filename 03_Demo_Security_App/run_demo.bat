@echo off
title Khoi Chay TechStore Security Lab Demo
echo =======================================================================
echo KHOI DONG TECHSTORE DATABASE SECURITY LAB (CHAMPION CYBER DEMO)
echo Mon hoc: Co so du lieu | Do an mon hoc PTIT
echo =======================================================================
echo.
echo Dang kiem tra moi truong Python...
python --version
if errorlevel 1 (
    echo [LOI] Khong tim thay Python tren may tinh!
    pause
    exit /b
)

echo.
echo Dang khoi dong Web Server Flask tai http://127.0.0.1:5000...
start "" http://127.0.0.1:5000
python app.py
pause

