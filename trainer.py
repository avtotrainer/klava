# trainer.py
# KLAVA — Application Trainer (Session Controller)

import tkinter as tk
from tkinter import messagebox

from ui.canvas import Canvas
from ui.keyboard import Keyboard
from ui.menu import AppMenu
from exercises.typing import TypingExercise


class Trainer:
    """
    Trainer — აპლიკაციის სესიის მმართველი.
    """

    SECRET_EXIT_COMBO = "<Control-Alt-Shift-Q>"

    def __init__(self, root: tk.Tk):
        self.root = root

        self.training_active = False
        self.exercise = None

        # ── UI ───────────────────────────────────────
        self.ui = Canvas(root)

        self.keyboard = Keyboard(
            self.ui.canvas,
            self.ui.width,
            self.ui.height,
        )

        # ── Menu ─────────────────────────────────────
        self.menu = AppMenu(
            root=self.root,
            on_start=self.start_training,
            on_exit=self.root.destroy,
            on_about=self._about,
        )
        self.menu.show()

        # ── Initial state ────────────────────────────
        self.ui.show_cover("KLAVA\n\nStart to begin")
        self.ui.hide_keyboard()

        # ── Key bindings ─────────────────────────────
        self.root.bind("<Key>", self.on_key)
        self.root.bind(self.SECRET_EXIT_COMBO, self._secret_finish)

    # ==================================================
    #   TRAINING CONTROL
    # ==================================================
    def start_training(self):
        if self.training_active:
            return

        self.training_active = True
        self.menu.hide()
        self._enable_kiosk()

        # UI state
        self.ui.hide_cover()
        self.ui.show_keyboard()

        # Exercise
        self.exercise = TypingExercise(self.ui, self.keyboard)
        self.exercise.start()

    def finish_training(self):
        self.training_active = False
        self.exercise = None

        # UI state
        self.ui.hide_keyboard()
        self.ui.show_cover("დავალება შესრულებულია")

        self._disable_kiosk()
        self.menu.show()

    # ==================================================
    #   KEY HANDLING
    # ==================================================
    def on_key(self, event):
        if not self.training_active or not self.exercise:
            return

        self.exercise.on_key(event)

        if self.exercise.finished:
            self.finish_training()

    # ==================================================
    #   SECRET EXIT
    # ==================================================
    def _secret_finish(self, event=None):
        if not self.training_active or not self.exercise:
            return

        self.exercise.stop()
        self.finish_training()

    # ==================================================
    #   KIOSK MODE
    # ==================================================
    def _enable_kiosk(self):
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="none")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def _disable_kiosk(self):
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.config(cursor="")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ==================================================
    #   ABOUT
    # ==================================================
    def _about(self):
        messagebox.showinfo(
            "About KLAVA",
            "KLAVA Typing Trainer\n\nAccuracy-first typing practice.",
        )
