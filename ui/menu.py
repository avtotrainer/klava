# ui/menu.py
# KLAVA — Menu Bar (UI)

import tkinter as tk


class AppMenu:
    """
    UI-only menu.
    ტექსტებს იღებს Resources-იდან.
    """

    def __init__(self, root: tk.Tk, texts, on_start, on_exit, on_about):
        self.root = root
        self.texts = texts
        self.menu = tk.Menu(root)
        self._build(on_start, on_exit, on_about)

    def _build(self, on_start, on_exit, on_about):
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label=self.texts.text("app", "start"), command=on_start)
        file_menu.add_separator()
        file_menu.add_command(label=self.texts.text("app", "exit"), command=on_exit)

        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label=self.texts.text("app", "about"), command=on_about)

        self.menu.add_cascade(
            label=self.texts.text("menu", "file", "File"), menu=file_menu
        )
        self.menu.add_cascade(
            label=self.texts.text("menu", "help", "Help"), menu=help_menu
        )

    def show(self):
        self.root.config(menu=self.menu)

    def hide(self):
        self.root["menu"] = ""
