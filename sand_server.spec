# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [( './packages/*', 'packages' ), ( './SAND_Images/*', 'SAND_Images' )]

a = Analysis(['sand_server.py'],
             pathex=['E:\\SAND_Y3_PROJECT\\SAND_Demo\\SAND_Server'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=['.'],
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
          name='sand_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )









