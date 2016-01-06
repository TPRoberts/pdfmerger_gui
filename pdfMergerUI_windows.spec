# -*- mode: python -*-
a = Analysis(['pdfMergerUI.py'],
             pathex=['C:\\pdfmerger_gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('pdfmerger.ico','C:\\pdfmerger_gui\\pdfmerger.ico','DATA')]
a.datas += [('info.txt','C:\\pdfmerger_gui\\info.txt','.')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pdfMergerUI.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , version='version.txt', icon='pdfmerger.ico')
