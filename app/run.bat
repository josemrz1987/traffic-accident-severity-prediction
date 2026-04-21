
@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% neq 0 (
  where python >nul 2>nul
  if %errorlevel% neq 0 (
    echo [ERROR] Necesitas Python 3.9+ instalado.
    echo Descarga: python.org
    pause
    exit /b 1
  )
)

if not exist ".venv\Scripts\python.exe" (
  py -3.9 -m venv .venv
)

call ".venv\Scripts\activate.bat"

python -m pip install --upgrade pip
pip install -r requirements.txt

python -m streamlit run app.py --server.port 8501 --server.address localhost --server.headless true

pause

