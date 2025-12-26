# ui/menu.py
# KLAVA — Menu Bar (UI)

import tkinter as tk


class AppMenu:
    """
    AppMenu მართავს მხოლოდ მენიუს.
    Trainer გადასცემს callback-ებს და მენიუს ჩართვა/გამორთვა შეუძლია.
    """

    def __init__(self, root: tk.Tk, on_start, on_exit, on_about):
        """
        :param root: Tk root ფანჯარა
        :param on_start: Start პუნქტის callback
        :param on_exit: Exit პუნქტის callback
        :param on_about: About პუნქტის callback
        """
        self.root = root
        self.menu = tk.Menu(root)
        self._build(on_start, on_exit, on_about)

    def _build(self, on_start, on_exit, on_about):
        """მენიუს სტრუქტურის აგება"""
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Start", command=on_start)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=on_exit)

        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label="About", command=on_about)

        self.menu.add_cascade(label="File", menu=file_menu)
        self.menu.add_cascade(label="Help", menu=help_menu)

    def show(self):
        """მენიუს ჩვენება"""
        self.root.config(menu=self.menu)

    def hide(self):
        """მენიუს დამალვა"""
        # self.root.config(menu=None)
        self.root["menu"] = ""
