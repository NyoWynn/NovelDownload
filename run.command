#!/bin/bash
# Novel Downloader — launcher para Mac
# Doble clic en Finder para arrancar.

cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  Novel Downloader"
echo "========================================"
echo ""

# Verificar Python 3
if ! command -v python3 &>/dev/null; then
  osascript -e 'display dialog "Python 3 no está instalado.\n\nDescárgalo en https://www.python.org/downloads/\nAsegúrate de instalar la versión oficial de python.org." buttons {"OK"} default button 1 with icon stop'
  exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
  echo "Configurando entorno virtual por primera vez (solo ocurre una vez)..."
  python3 -m venv .venv
fi

source .venv/bin/activate

# Instalar / actualizar dependencias
echo "Verificando dependencias..."
pip install -q -r requirements.txt

# Ejecutar la app
echo ""
echo "Iniciando Novel Downloader..."
echo ""
python main.py
