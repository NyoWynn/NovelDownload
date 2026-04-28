@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   Novel Downloader
echo ========================================
echo.

:: Verificar Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    echo Descargalo en https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" al instalar.
    pause
    exit /b 1
)

:: Crear entorno virtual si no existe
if not exist ".venv\" (
    echo Configurando entorno virtual por primera vez...
    python -m venv .venv
)

:: Activar entorno virtual
call .venv\Scripts\activate.bat

:: Instalar / actualizar dependencias
echo Verificando dependencias...
pip install -q -r requirements.txt

:: Ejecutar la app
echo.
echo Iniciando Novel Downloader...
echo.
python main.py

pause
