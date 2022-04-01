# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('assets/backgrounds/*.png','assets/backgrounds'), ('assets/backgrounds/*.jpg','assets/backgrounds'), ('assets/characters/ninja/*.png','assets/characters/ninja'), ('assets/characters/zombies/male/*.png','assets/characters/zombies/male'), ('assets/characters/zombies/female/*.png','assets/characters/zombies/female'), ('assets/fonts/*.ttf','assets/fonts'), ('assets/music/*.wav','assets/music'), ('assets/soundeffects/*.wav','assets/soundeffects'), ('assets/vfx/dustCloud/*.png','assets/vfx/dustCloud'), ('assets/vfx/powerUp/*.png','assets/vfx/powerUp'), ('assets/vfx/waterSplash/*.png','assets/vfx/waterSplash') ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
