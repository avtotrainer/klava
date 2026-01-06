# logic/resources.py
# KLAVA — Resources (i18n + theme + keyboard model)

from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from pathlib import Path
import json


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
        self.base = Path(base_dir)
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
