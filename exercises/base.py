# exercises/base.py
# KLAVA — Exercise Base Interface

import tkinter as tk


class Exercise:
    """
    სავარჯიშოს საბაზო კონტრაქტი.

    Does:
    - განსაზღვრავს Trainer-ისთვის მინიმალურ API-ს

    Does not:
    - არ მართავს root-ს
    - არ ეხება kiosk რეჟიმს
    - არ მუშაობს menu-სთან
    """

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def on_key(self, event: tk.Event) -> None:
        raise NotImplementedError

    @property
    def finished(self) -> bool:
        raise NotImplementedError
