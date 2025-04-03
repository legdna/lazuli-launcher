# -*- mode: python ; coding: utf-8 -*-

MSYS64_PATH = "C:/msys64/ucrt64"

a = Analysis( # type: ignore
    ['src/oracles.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        #("C:/msys64/ucrt64/lib/girepository-1.0/*.typelib", "girepository-1.0"),
        # Icônes et thèmes
        #("C:/msys64/ucrt64/share/icons/Adwaita", 'share/icons/Adwaita')
    ],
    hiddenimports=[
        'asyncio',
        'gi._error',
        'gi._option',
        'gi._enum'
    ],
    hookspath=[],
    hooksconfig={
        'gi': {
            'module-versions': {
                'Gtk': '4.0',
		        'Adw': '1'
            },
            'icons': ['Adwaita'],
            'themes': ['Adwaita']
        }
    },
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure) # type: ignore

exe = EXE( # type: ignore
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Oraclès Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='data/oracles.ico'
)
coll = COLLECT( # type: ignore
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Oraclès Launcher',
)