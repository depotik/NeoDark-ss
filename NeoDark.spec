# neo_bot.spec
a = Analysis(
    ['download.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[ 'requests', 'zipfile', 'threading', 'shutil', 'tempfile', 'pathlib', 'ctypes', 'datetime' , 'subprocess', 'internetspeedtest', 'json', 'email', 'pystyle', 'os', 'sys', 'time', 'random', 'urllib', 'base64', 'colored', 'colorama', 'smtplib', 'ipaddress', 'socket', 'msvcrt', ''],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NeoDark',
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
    icon='logo.ico'
)