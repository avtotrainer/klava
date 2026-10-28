"""Assemble the exact portable payload; never copy an entire build directory."""
from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]


def package(root: Path = ROOT) -> Path:
    """Validate the seed, copy only user-facing files, and verify ZIP contents."""
    seed = root / "data/sentences.klv"
    lines = [line.strip().upper() for line in seed.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    if len(lines) < 2 or any(set(line) - set("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") for line in lines):
        raise ValueError("Seed requires at least two lines using supported letters and spaces")
    payload = root / "dist/KLAVA"
    payload.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "dist/KLAVA.exe", payload / "KLAVA.exe")
    shutil.copy2(seed, payload / "exercises.klv")
    expected = {"KLAVA.exe", "exercises.klv"}
    if {p.name for p in payload.iterdir()} != expected:
        raise ValueError("Portable directory must contain exactly KLAVA.exe and exercises.klv")
    archive = root / "dist/KLAVA-windows-x64.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zipped:
        for name in sorted(expected):
            zipped.write(payload / name, f"KLAVA/{name}")
    with ZipFile(archive) as zipped:
        if set(zipped.namelist()) != {f"KLAVA/{name}" for name in expected}:
            raise ValueError("Unexpected ZIP contents")
        if zipped.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    print(archive)
    return archive


if __name__ == "__main__":
    package()
