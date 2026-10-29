# Build on Windows: python -m PyInstaller --clean --noconfirm KLAVA.spec
from pathlib import Path

root = Path(SPECPATH)
a = Analysis(
    [str(root / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / "config.ini"), "."),
           (str(root / "resources"), "resources"),
           (str(root / "LICENSE"), ".")],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
# Supplying binaries/data directly to EXE (no COLLECT) creates a onefile build.
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="KLAVA",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(root / "resources" / "branding" / "generated" / "KLAVA.ico"),
)
