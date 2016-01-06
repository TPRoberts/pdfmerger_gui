# -*- mode: python -*-

block_cipher = None


a = Analysis(['pdfMergerUI.py'],
             pathex=['/home/tom/pdfmerger_gui'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
a.datas += [('info.txt','/home/tom/pdfmerger_gui/info.txt','.')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pdfMergerUI',
          debug=False,
          strip=None,
          upx=True,
          console=False)
