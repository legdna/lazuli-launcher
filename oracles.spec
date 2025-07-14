# -*- mode: python ; coding: utf-8 -*-

a = Analysis( # type: ignore
    ['src/oracles.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data/background', 'data/background'),
        ('data/oracles.gresource', 'data')
    ],
    hiddenimports=[],
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
    name='Lazuli Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    onefile=True,
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
    name='Lazuli Launcher',
)
app = BUNDLE( # type: ignore
    coll,
    name='Lazuli Launcher.app',
    icon='data/oracles_macos.ico',
    bundle_identifier='dev.lazura.LazuliLauncher',
    info_plist={
        'NSMicrophoneUsageDescription': 'Nécessaire pour utiliser le chat de proximité.'
    }
)