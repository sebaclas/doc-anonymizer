# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    ('../docs/mini_manual.html', '.'),
    ('../docs/assets/logo.png', '.'),
    ('../docs/assets/logo.ico', '.'),
]
binaries = []
hiddenimports = []

for pkg in ('spacy', 'xx_ent_wiki_sm', 'customtkinter', 'text2num'):
    tmp = collect_all(pkg)
    datas         += tmp[0]
    binaries      += tmp[1]
    hiddenimports += tmp[2]

a = Analysis(
    ['../anonymizer/gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='AnonymizerPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../docs/assets/logo.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnonymizerPro',
)
