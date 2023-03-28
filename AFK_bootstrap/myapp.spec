# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Add the path to the subfiles to the sys.path list
sys.path.append(os.path.dirname(os.path.abspath("Gui.py")))

# Import the subfiles
from Shared_functions import *
from Stage_calculation import *
from Database import *
from Vision import *
from Loop import *

# Import the necessary modules
from PyInstaller.utils.hooks import collect_data_files
import ttkbootstrap as tb

# Collect image files
datas = collect_data_files('images')

# Specify the options for PyInstaller
block_cipher = None
a = Analysis(['Gui.py'],
             pathex=['H:/git/AFK_Auto_Arena_CMD/AFK_bootstrap'],
             binaries=[],
             datas=datas,
             hiddenimports=['Shared_functions'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AFK Auto Arena',
          debug=False,
		  uac_admin=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
		  argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
		  icon='images/icon.ico'
		  )
