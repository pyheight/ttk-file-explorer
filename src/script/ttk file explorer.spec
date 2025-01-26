# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\main.py'],
    pathex=['C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src'],
    binaries=[],
    datas=[('C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\images\\icon.ico', './images/'), ('C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\images\\loading.gif', './images/')],
    hiddenimports=['constants', 'images', 'view', 'model', 'controller', 'controller.tab_manager', '__init__'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    'C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\script\\images\\splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(30, 345),
    text_size=12,
    minify_script=True,
    always_on_top=False,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='ttk file explorer',
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
    version='C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\script\\version.txt',
    icon=['C:\\Users\\Administrator\\Desktop\\ttk_file_explorer_v1.0.0-beta_Windows7\\src\\images\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ttk file explorer',
)
