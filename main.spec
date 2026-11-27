# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	name='DupliFinder',
	debug=False,
	strip=False,
	upx=True,
	runtime_tmpdir=None,
	console=False 
)
