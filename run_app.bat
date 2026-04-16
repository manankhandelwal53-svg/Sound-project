@echo off
setlocal

set "PROJECT_ROOT=E:\codex"
set "APP_FILE=%PROJECT_ROOT%\src\cbse_result_analyzer\streamlit_app.py"
set "TESSERACT_CMD=D:\teseract\tesseract.exe"

if not exist "%APP_FILE%" (
    echo App file not found:
    echo %APP_FILE%
    pause
    exit /b 1
)

if not exist "%TESSERACT_CMD%" (
    echo Tesseract executable not found:
    echo %TESSERACT_CMD%
    echo.
    echo Update run_app.bat with the correct path before launching.
    pause
    exit /b 1
)

where python3.12 >nul 2>nul
if %errorlevel% neq 0 (
    echo python3.12 was not found on PATH.
    echo Install Python 3.12 or update this launcher to use the correct command.
    pause
    exit /b 1
)

set "TESSERACT_CMD=%TESSERACT_CMD%"
cd /d "%PROJECT_ROOT%"

echo Starting CBSE Result Analyzer...
echo.
python3.12 -m streamlit run "%APP_FILE%"

if %errorlevel% neq 0 (
    echo.
    echo The app exited with an error.
    pause
    exit /b %errorlevel%
)
