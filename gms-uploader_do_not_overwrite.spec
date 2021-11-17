# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['gms_uploader/gms-uploader.py'],
             pathex=['D:/PycharmProjects/GMS-uploader'],
             datas=[('venv/Lib/site-packages/qdarktheme', 'qdarktheme'),
                    ('gms_uploader/config', 'config'),
                    ('gms_uploader/icons', 'icons'),
                    ('gms_uploader/fx', 'fx')
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

splash = Splash('gms_uploader/img/gms-splash.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(10, 50),
                text_size=12,
                text_color='black')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          splash,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='gms-uploader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='gms_uploader/icons/AppIcons/GMS-logo.ico'
          )
coll = COLLECT(exe,
               splash.binaries,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='gms-uploader_v0.2.0')
