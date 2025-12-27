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

    პასუხისმგებელია:
    - menu bar-ზე
    - cover page-ზე
    - kiosk რეჟიმზე
    - exercise lifecycle-ზე
    """

    SECRET_EXIT_COMBO = "<Control-Alt-Shift-Q>"

    def __init__(self, root: tk.Tk):
        self.root = root

        # ── მდგომარეობები ─────────────────────────────
        self.training_active = False
        self.exercise = None

        # ── UI ────────────────────────────────────────
        self.ui = Canvas(root)
        self.keyboard = Keyboard(
            self.ui.canvas,
            self.ui.width,
            self.ui.height,
        )

        # ── Menu ──────────────────────────────────────
        self.menu = AppMenu(
            root=self.root,
            on_start=self.start_training,
            on_exit=self.root.destroy,
            on_about=self._about,
        )
        self.menu.show()

        # ── Cover Page ─────────────────────────────────
        self._draw_cover()

        # ── Key bindings ───────────────────────────────
        self.root.bind("<Key>", self.on_key)
        self.root.bind(self.SECRET_EXIT_COMBO, self._secret_finish)

    # ==================================================
    #   COVER
    # ==================================================
    def _draw_cover(self):
        """Cover Page — საწყისი ეკრანი"""
        self.ui.clear()
        self.ui.canvas.create_text(
            self.ui.width / 2,
            self.ui.height / 2,
            text="KLAVA\n\nPress Start to Begin",
            font=("Arial", 48, "bold"),
            fill="#444",
            justify="center",
        )

    # ==================================================
    #   TRAINING CONTROL
    # ==================================================
    def start_training(self):
        """ტრენინგის დაწყება"""
        if self.training_active:
            return

        self.training_active = True
        self.menu.hide()
        self._enable_kiosk()

        # ── Keyboard-ის შექმნა (აუცილებელია) ───────────
        from ui.keyboard import Keyboard

        self.keyboard = Keyboard(
            self.ui.canvas,
            self.ui.width,
            self.ui.height,
        )

        # ── Exercise არჩევა (ახლა ერთია) ───────────────
        self.exercise = TypingExercise(self.ui, self.keyboard)
        self.exercise.start()

    def finish_training(self):
        """ტრენინგის დასრულება"""
        self.training_active = False
        self.exercise = None

        self._disable_kiosk()
        self.menu.show()
        self._draw_cover()

    # ==================================================
    #   KIOSK MODE
    # ==================================================
    def _enable_kiosk(self):
        """kiosk რეჟიმის ჩართვა"""
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="none")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def _disable_kiosk(self):
        """kiosk რეჟიმის გამორთვა"""
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.config(cursor="")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ==================================================
    #   KEY HANDLING
    # ==================================================
    def on_key(self, event):
        """ყველა კლავიშის ცენტრალური დამმუშავებელი"""
        if not self.training_active or not self.exercise:
            return

        self.exercise.on_key(event)

        if self.exercise.finished:
            self.finish_training()

    # ==================================================
    #   SECRET EXIT
    # ==================================================
    def _secret_finish(self, event=None):
        """
        საიდუმლო კომბინაცია:
        - მუშაობს მხოლოდ ტრენინგის დროს
        - ასრულებს სავარჯიშოს
        - ხსნის kiosk რეჟიმს
        """
        if not self.training_active or not self.exercise:
            return

        self.exercise.stop()
        self.finish_training()

    # ==================================================
    #   ABOUT
    # ==================================================
    def _about(self):
        messagebox.showinfo(
            "About KLAVA", "KLAVA Typing Trainer\n\nAccuracy-first typing practice."
        )
