# logic/resources.py
# KLAVA — Resources (i18n + theme + keyboard model)

from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from pathlib import Path
import json
import sys


def bundled_path(path: str) -> Path:
    """Resolve read-only assets in the source tree or PyInstaller extraction root."""
    # PyInstaller sets module __file__ inside its temporary onefile bundle.
    return Path(__file__).resolve().parent.parent / path


from logic.exercise_library import DEFAULT_NAME, library_dir, selected_exercise


def exercise_path(source_path: str) -> Path:
    """Return the user's selected KLV exercise, independent of install scope."""
    return selected_exercise()


def prepare_exercise_file(source_path: str) -> Path:
    """Seed the user's library exactly once without overwriting any files.

    Existing legacy exercises.txt is copied to the default KLV on migration.
    Installed EXEs use the distributed default-exercises.klv; portable EXEs
    use exercises.klv next to the executable; source runs use configured data.
    """
    directory = library_dir()
    directory.mkdir(parents=True, exist_ok=True)
    default = directory / DEFAULT_NAME
    if not default.exists():
        if getattr(sys, "frozen", False):
            app_dir = Path(sys.executable).resolve().parent
            seed = app_dir / "default-exercises.klv"
            if not seed.is_file():
                seed = app_dir / DEFAULT_NAME
        else:
            seed = bundled_path(source_path)
        legacy = directory / "exercises.txt"
        if legacy.is_file():
            seed = legacy
        if not seed.is_file():
            raise FileNotFoundError(seed)
        try:
            with default.open("xb") as dest:
                dest.write(seed.read_bytes())
        except FileExistsError:
            pass
    return selected_exercise()


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
        return self.texts.get(section, key, fallback=fallback).replace(r"\n", "\n")

    def theme_section(self, section: str) -> SectionProxy:
        return self.theme[section]
