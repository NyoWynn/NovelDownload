# NovelDownloader

App de escritorio para descargar novelas desde sitios compatibles y exportarlas como PDF o ePub.

![NovelDownloader logo](./resources/logo.png)

## Qué hace

- Obtiene metadatos y lista de capítulos desde la URL de la novela
- Descarga todos los capítulos o un rango seleccionado
- Exporta un PDF o ePub con portada, formato y estilos
- Opción de traducción automática al español
- Interfaz gráfica con tema claro/oscuro

## Sitios soportados

- [matrone-scan.xyz](https://matrone-scan.xyz) y cualquier sitio con tema WordPress Madara
- URLs de Wayback Machine (`web.archive.org`)

## Correr con un clic

**Windows:** doble clic en `run.bat`  
**Mac:** doble clic en `run.command` (requiere permiso la primera vez: clic derecho → Abrir)

Ambos scripts crean el entorno virtual e instalan dependencias automáticamente.

## Correr desde terminal

```bash
pip install -r requirements.txt
python main.py
```

## Compilar ejecutable (.exe / .app)

```bash
pyinstaller NovelDownloader.spec --clean --noconfirm
```

- **Windows** → `dist/NovelDownloader.exe`
- **Mac** → `dist/NovelDownloader.app`

> PyInstaller debe ejecutarse en cada sistema operativo por separado.

## Estructura

```
main.py              Entrada de la app
gui.py               Interfaz gráfica (CustomTkinter)
scraper.py           Descarga de capítulos y metadatos
translator.py        Traducción opcional al español
pdf_generator.py     Generación de PDF
epub_generator.py    Generación de ePub
requirements.txt     Dependencias
run.bat              Lanzador Windows
run.command          Lanzador Mac
resources/           Logos y assets
```

## Tech Stack

- Python 3.11
- CustomTkinter
- Requests + BeautifulSoup4
- ReportLab (PDF) + EbookLib (ePub)
- Pillow
- PyInstaller

## Autor

Hecho por [NyoWynn](https://github.com/NyoWynn)
