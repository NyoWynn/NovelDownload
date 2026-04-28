# -*- mode: python ; coding: utf-8 -*-
# NovelDownloader.spec — PyInstaller build configuration (Windows + Mac)

import sys
from pathlib import Path

import customtkinter
ctk_path = Path(customtkinter.__file__).parent

IS_MAC = sys.platform == "darwin"

datas = [
    (str(ctk_path), "customtkinter"),
]
if Path("resources").exists():
    datas.append(("resources", "resources"))
if not IS_MAC and Path("icon.ico").exists():
    datas.append(("icon.ico", "."))

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "customtkinter",
        "PIL",
        "PIL.Image",
        "PIL.ImageTk",
        "reportlab",
        "reportlab.platypus",
        "reportlab.lib",
        "reportlab.lib.styles",
        "reportlab.lib.pagesizes",
        "reportlab.lib.units",
        "reportlab.lib.colors",
        "reportlab.lib.enums",
        "reportlab.pdfbase",
        "reportlab.pdfbase.pdfmetrics",
        "reportlab.pdfbase.ttfonts",
        "ebooklib",
        "ebooklib.epub",
        "bs4",
        "lxml",
        "lxml.etree",
        "lxml._elementpath",
        "requests",
        "charset_normalizer",
        "deep_translator",
        "tkinter",
        "tkinter.filedialog",
        "tkinter.messagebox",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "scipy", "pandas", "PySide6", "PyQt5"],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="NovelDownloader",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    argv_emulation=IS_MAC,
    icon="icon.ico" if (not IS_MAC and Path("icon.ico").exists()) else None,
)

# Mac: envuelve el binario en un .app de doble clic
if IS_MAC:
    app = BUNDLE(
        exe,
        name="NovelDownloader.app",
        icon=None,  # Cambia a "resources/logo.icns" si tienes un .icns
        bundle_identifier="com.nyowynn.noveldownloader",
        info_plist={
            "CFBundleName": "Novel Downloader",
            "CFBundleDisplayName": "Novel Downloader",
            "CFBundleVersion": "1.0.0",
            "NSHighResolutionCapable": True,
        },
    )
