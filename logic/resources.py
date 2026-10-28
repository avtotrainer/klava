# logic/resources.py
# KLAVA — Resources (i18n + theme + keyboard model)

from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from pathlib import Path
import json
import os
import sys


def bundled_path(path: str) -> Path:
    """Resolve read-only assets in the source tree or PyInstaller extraction root."""
    # PyInstaller sets module __file__ inside its temporary onefile bundle.
    return Path(__file__).resolve().parent.parent / path


def exercise_path(source_path: str) -> Path:
    """Separate installed per-user data, portable data and source-mode config."""
    if getattr(sys, "frozen", False):
        directory = Path(sys.executable).resolve().parent
        # Only the installer ships this read-only seed, also marking installed mode.
        if (directory / "default-exercises.txt").is_file():
            local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
            return local / "KLAVA" / "exercises.txt"
        return directory / "exercises.txt"
    return bundled_path(source_path)


def prepare_exercise_file(source_path: str) -> Path:
    """Seed installed per-user exercises once; never overwrite an existing file.

    Portable/source files are never generated. Empty or invalid user files remain
    untouched so Trainer can report them. Installation does not access user profiles.
    """
    path = exercise_path(source_path)
    if getattr(sys, "frozen", False):
        seed = Path(sys.executable).resolve().parent / "default-exercises.txt"
        if seed.is_file() and not path.exists():
            content = seed.read_bytes()
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                # Exclusive creation also protects against two concurrent launches.
                with path.open("xb") as target:
                    target.write(content)
            except FileExistsError:
                pass
    return path


class Resources:
    """
    Does:
    - loads i18n texts: resources/i18n/<lang>.ini
    - loads theme: resources/themes/<theme>.ini
    - loads keyboard model: resources/keyboard/fingers.json

    Does not:
    - contain UI logic
    - contain typing logic
    """

    def __init__(self, base_dir: str, language: str, theme_name: str) -> None:
        self.base = bundled_path(base_dir)
        self.language = language
        self.theme_name = theme_name

        self.texts = self._load_ini(self.base / "i18n" / f"{language}.ini")
        self.theme = self._load_ini(self.base / "themes" / f"{theme_name}.ini")
        self.keyboard_model = self._load_json(self.base / "keyboard" / "fingers.json")

        self._validate_keyboard_model(self.keyboard_model)

    # ----------------------------
    def _load_ini(self, path: Path) -> ConfigParser:
        if not path.exists():
            raise FileNotFoundError(f"Resource not found: {path}")
        cp = ConfigParser()
        cp.read(path, encoding="utf-8")
        return cp

    def _load_json(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Resource not found: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _validate_keyboard_model(self, model: dict) -> None:
        if "groups" not in model or "colors" not in model:
            raise ValueError("Keyboard model must contain 'groups' and 'colors' keys")

    # ----------------------------
    def text(self, section: str, key: str, fallback: str = "") -> str:
        return self.texts.get(section, key, fallback=fallback)

    def theme_section(self, section: str) -> SectionProxy:
        return self.theme[section]
