@echo off
title Akira's Teacher Portal
cd /d "%~dp0"

echo ====================================================
echo   Akira's Teacher - Windows Local Network Launcher
echo ====================================================

:: Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in PATH!
    echo Please install Python 3.10 or newer from python.org
    echo and check the box "Add python.exe to PATH" during installation.
    pause
    exit /b 1
)

:: Create virtual environment if missing
if not exist ".venv" (
    echo [1/3] Creating virtual environment (.venv)...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: Check for .env file
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [!] Created .env from .env.example.
        echo [!] Remember to edit .env and add your GEMINI_API_KEY!
    )
)

echo [3/3] Starting Akira's Teacher server on local network...
python run.py
pause
