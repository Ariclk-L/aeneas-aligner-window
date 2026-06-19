# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Aeneas Aligner
打包命令: pyinstaller align.spec --clean --noconfirm
"""
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

block_cipher = None

a = Analysis(
    ['src/align.py'],
    pathex=[os.path.abspath(SPECPATH)],
    binaries=[],
    datas=[
        # 外部二进制资源目录，需要在 build.bat 中提前下载/放置
        ('ffmpeg', 'ffmpeg'),
        ('espeak', 'espeak'),
    ],
    hiddenimports=[
        'aeneas.executetask',
        'aeneas.task',
        'aeneas.tools.execute_task',
        'aeneas.syncmap',
        'aeneas.cdtw.cdtw',
        'aeneas.cmfcc.cmfcc',
        'aeneas.cew.cew',
        'aeneas.globalconstants',
        'aeneas.language',
        'chardet',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='align',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
