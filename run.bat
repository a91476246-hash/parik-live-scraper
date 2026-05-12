@echo off
chcp 65001 >nul
title Parik24 Live Football Scraper

echo ========================================
echo   Parik24 Live Football Scraper
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Install Python 3.11+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Create venv if it doesn't exist
if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate venv
call .venv\Scripts\activate.bat

:: Install dependencies if not installed
pip show parik-live-scraper >nul 2>&1
if errorlevel 1 (
    echo [2/3] Installing dependencies...
    pip install -e . >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo Done!
) else (
    echo [2/3] Dependencies already installed.
)

echo [3/3] Fetching live football matches...
echo.

parik-live --live-only

echo.
pause
