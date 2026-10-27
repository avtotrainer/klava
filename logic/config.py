# logic/config.py
# KLAVA — Config loader

from configparser import ConfigParser
from logic.resources import bundled_path


class Config:
    """
    Config reader for config.ini.

    Does:
    - loads config.ini relative to project root
    - provides typed getters

    Does not:
    - decide behavior (Trainer decides)
    """

    def __init__(self, path: str = "config.ini") -> None:
        self.path = bundled_path(path)

        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.path}")

        self.parser = ConfigParser()
        self.parser.read(self.path, encoding="utf-8")

    def get(self, section: str, key: str, fallback: str | None = None) -> str:
        return self.parser.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        return self.parser.getint(section, key, fallback=fallback)

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        return self.parser.getboolean(section, key, fallback=fallback)
