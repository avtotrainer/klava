# trainer.py
# KLAVA — Application Trainer (Session Controller)

from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox
from typing import Optional

from ui.canvas import Canvas
from ui.keyboard import Keyboard
from ui.menu import AppMenu
from exercises.typing import TypingExercise


# ===============================================
#   კონფიგურაცია
# ===============================================
MIN_LINES: int = 2

# ფაილის გზა განისაზღვრება ამ ფაილიდან მიმართებით
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
SENTENCE_FILE: str = os.path.join(BASE_DIR, "data", "sentences.txt")


class Trainer:
    """
    Trainer — აპლიკაციის სესიის მმართველი.

    პასუხისმგებლობა:
    - დავალების სრული ციკლის მართვა
    - სტრიქონებს შორის გადართვა
    - kiosk რეჟიმი
    - UI მდგომარეობების კოორდინაცია

    არ აკეთებს:
    - ბეჭდვის ლოგიკის გამოთვლას
    - ტექსტის არჩევას
    """

    SECRET_EXIT_COMBO: str = "<Control-Alt-Shift-Q>"

    # ===============================================
    #   INIT
    # ===============================================
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root

        # ── მდგომარეობა ─────────────────────────────
        self.training_active: bool = False
        self.exercise: Optional[TypingExercise] = None

        self.sentences: list[str] = []
        self.current_index: int = 0
        self.lines_done: int = 0

        # ── UI ──────────────────────────────────────
        self.ui: Canvas = Canvas(root)

        self.keyboard: Keyboard = Keyboard(
            self.ui.canvas,
            self.ui.width,
            self.ui.height,
        )

        # ── Menu ────────────────────────────────────
        self.menu: AppMenu = AppMenu(
            root=self.root,
            on_start=self.start_training,
            on_exit=self.root.destroy,
            on_about=self._about,
        )
        self.menu.show()

        # ── საწყისი მდგომარეობა ─────────────────────
        self.ui.show_cover("KLAVA\n\nStart to begin")
        self.ui.hide_keyboard()

        # ── კლავიშები ──────────────────────────────
        self.root.bind("<Key>", self.on_key)
        self.root.bind(self.SECRET_EXIT_COMBO, self._secret_finish)

    # ===============================================
    #   TRAINING CONTROL
    # ===============================================
    def start_training(self) -> None:
        """
        ვიწყებთ ახალ დავალებას.
        """
        if self.training_active:
            return

        # ── დავალებების ჩატვირთვა ──────────────────
        try:
            self.sentences = self._load_sentences()
        except RuntimeError as e:
            messagebox.showerror("დავალების შეცდომა", str(e))
            return

        # ვალიდაცია — მინიმალური ხაზები
        if len(self.sentences) < MIN_LINES:
            messagebox.showerror(
                "დავალების შეცდომა",
                f"დავალება უნდა შეიცავდეს მინიმუმ {MIN_LINES} სტრიქონს",
            )
            return

        self.training_active = True
        self.menu.hide()
        self._enable_kiosk()

        # reset ციკლი
        self.current_index = 0
        self.lines_done = 0

        # UI
        self.ui.hide_cover()
        self.ui.show_keyboard()

        # პირველი სტრიქონი
        self._load_current_line()

    def finish_training(self) -> None:
        """
        სრულდება მთელი დავალება (ყველა სტრიქონი).
        """
        self.training_active = False
        self.exercise = None

        # UI
        self.ui.hide_keyboard()
        self.ui.show_cover("დავალება შესრულებულია")

        self._disable_kiosk()
        self.menu.show()

    # ===============================================
    #   LINE CONTROL
    # ===============================================
    def _load_current_line(self) -> None:
        """
        იტვირთება მიმდინარე სტრიქონი TypingExercise-ში.
        """
        if self.current_index >= len(self.sentences):
            self.finish_training()
            return

        sentence = self.sentences[self.current_index]

        self.exercise = TypingExercise(
            ui=self.ui,
            keyboard=self.keyboard,
            sentence=sentence,
        )
        self.exercise.start()

    # ===============================================
    #   KEY HANDLING
    # ===============================================
    def on_key(self, event: tk.Event) -> None:
        """
        ყველა კლავიშის გლობალური დამუშავება.
        """
        if not self.training_active:
            return

        # Pyright-ისთვის: Optional-ის უსაფრთხო გამაგრება
        exercise = self.exercise
        if exercise is None:
            return

        exercise.on_key(event)

        if exercise.finished:
            self.lines_done += 1
            self.current_index += 1

            # თუ კიდევ არსებობს სტრიქონი — გადავდივართ შემდეგზე
            if self.current_index < len(self.sentences):
                self._load_current_line()
                return

            # ყველა სტრიქონი შესრულებულია
            self.finish_training()

    # ===============================================
    #   SECRET EXIT
    # ===============================================
    def _secret_finish(self, event: Optional[tk.Event] = None) -> None:
        """
        საიდუმლო გამოსასვლელი — ავარიული დასრულება.
        """
        if not self.training_active:
            return

        exercise = self.exercise
        if exercise is None:
            return

        exercise.stop()
        self.finish_training()

    # ===============================================
    #   KIOSK MODE
    # ===============================================
    def _enable_kiosk(self) -> None:
        """kiosk რეჟიმის ჩართვა (fullscreen + topmost + cursor hide)."""
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="none")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def _disable_kiosk(self) -> None:
        """kiosk რეჟიმის გამორთვა (ფანჯრის ნორმალურ რეჟიმში დაბრუნება)."""
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.config(cursor="")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ===============================================
    #   HELPERS
    # ===============================================
    def _load_sentences(self) -> list[str]:
        """
        კითხულობს სავარჯიშო სტრიქონებს ფაილიდან.

        აბრუნებს:
            list[str]: სტრიქონების სია (UPPERCASE, ცარიელების გარეშე)

        აგდებს:
            RuntimeError: თუ ფაილი ვერ გაიხსნა ან ცარიელია.
        """
        try:
            with open(SENTENCE_FILE, encoding="utf-8") as f:
                lines = [line.strip().upper() for line in f if line.strip()]
        except Exception as e:
            raise RuntimeError(f"დავალების ფაილი ვერ გაიხსნა: {e}") from e

        if not lines:
            raise RuntimeError("დავალების ფაილი ცარიელია")

        return lines

    # ===============================================
    #   ABOUT
    # ===============================================
    def _about(self) -> None:
        """About დიალოგი."""
        messagebox.showinfo(
            "About KLAVA",
            "KLAVA Typing Trainer\n\nAccuracy-first typing practice.",
        )
