# trainer.py
# KLAVA — Application Trainer (Session Controller)

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from logic.config import Config
from logic.resources import Resources

from ui.canvas import Canvas
from ui.keyboard import Keyboard
from ui.menu import AppMenu

from exercises.typing import TypingExercise


class Trainer:
    """
    Trainer — აპლიკაციის სესიის მმართველი.

    Does:
    - კითხულობს config.ini-ს
    - ტვირთავს resources (ენა/თემა/კლავიატურის მოდელი)
    - კოორდინაციას უწევს UI + Exercise lifecycle-ს
    - მართავს kiosk რეჟიმს

    Does not:
    - ბეჭდვის ლოგიკის დათვლას
    - UI ელემენტების დახატვას (ამას Canvas/Keyboard აკეთებს)
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # ── CONFIG ──────────────────────────────────
        self.cfg = Config()

        # ── RESOURCES ───────────────────────────────
        lang = self.cfg.get("app", "language", fallback="en")
        resources_dir = self.cfg.get("paths", "resources_dir", fallback="resources")
        theme_name = self.cfg.get("ui", "theme", fallback="default")

        self.res = Resources(
            base_dir=resources_dir,
            language=lang,
            theme_name=theme_name,
        )

        # ── WINDOW TITLE (from resources) ───────────
        self.root.title(self.res.text("app", "title", fallback="KLAVA"))

        # ── STATE ──────────────────────────────────
        self.training_active: bool = False
        self.exercise: Optional[TypingExercise] = None

        self.sentences: list[str] = []
        self.current_index: int = 0

        # ── UI ─────────────────────────────────────
        self.ui = Canvas(
            root=self.root,
            theme=self.res.theme,  # Canvas-იც theme-იდან იღებს ფერებს/ფონტებს
        )

        # ── KEYBOARD ───────────────────────────────
        k = self.res.theme_section("keyboard")
        self.keyboard = Keyboard(
            canvas=self.ui.canvas,
            screen_width=self.ui.width,
            screen_height=self.ui.height,
            keyboard_model=self.res.keyboard_model,
            # theme values
            use_finger_colors=k.getboolean("use_finger_colors", fallback=True),
            finger_lighten_factor=float(
                k.get("finger_lighten_factor", fallback="0.88")
            ),
            color_target=k.get("color_target", fallback="#ffeb3b"),
            color_correct=k.get("color_correct", fallback="#7cfc9a"),
            color_wrong=k.get("color_wrong", fallback="#ff4d4d"),
            text_pale=k.get("text_pale", fallback="#cccccc"),
            text_dark=k.get("text_dark", fallback="#000000"),
            key_radius=k.getint("key_radius", fallback=18),
            key_gap_ratio=float(k.get("key_gap_ratio", fallback="0.12")),
        )

        # ── MENU ───────────────────────────────────
        self.menu = AppMenu(
            root=self.root,
            texts=self.res,
            on_start=self.start_training,
            on_exit=self.root.destroy,
            on_about=self._about,
        )
        self.menu.show()

        # ── INITIAL STATE ──────────────────────────
        self.ui.show_cover(self.res.text("cover", "welcome"))
        self.ui.hide_keyboard()

        # ── KEY BINDINGS ───────────────────────────
        self.root.bind("<Key>", self.on_key)

        exit_combo = self.cfg.get("app", "exit_combo", fallback="Control-Alt-Shift-Q")
        self.root.bind(f"<{exit_combo}>", self._secret_finish)

    # ==================================================
    # TRAINING
    # ==================================================
    def start_training(self) -> None:
        if self.training_active:
            return

        try:
            self.sentences = self._load_sentences()
        except RuntimeError as e:
            messagebox.showerror(
                self.res.text("errors", "title", fallback="Error"),
                str(e),
            )
            return

        min_lines = self.cfg.getint("training", "min_lines", fallback=2)
        if len(self.sentences) < min_lines:
            messagebox.showerror(
                self.res.text("errors", "title", fallback="Error"),
                self.res.text("errors", "min_lines").format(n=min_lines),
            )
            return

        self.training_active = True
        self.menu.hide()
        self._enable_kiosk()

        self.current_index = 0

        self.ui.hide_cover()
        self.ui.show_keyboard()

        self._load_current_line()

    def finish_training(self) -> None:
        self.training_active = False
        self.exercise = None

        self.ui.hide_keyboard()
        self.ui.show_cover(self.res.text("cover", "finished"))

        self._disable_kiosk()
        self.menu.show()

    # ==================================================
    # LINE CONTROL
    # ==================================================
    def _load_current_line(self) -> None:
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

    # ==================================================
    # INPUT
    # ==================================================
    def on_key(self, event: tk.Event) -> None:
        if not self.training_active:
            return

        if self.exercise is None:
            return

        self.exercise.on_key(event)

        if self.exercise.finished:
            self.current_index += 1
            if self.current_index < len(self.sentences):
                self._load_current_line()
            else:
                self.finish_training()

    # ==================================================
    # SECRET EXIT
    # ==================================================
    def _secret_finish(self, event: Optional[tk.Event] = None) -> None:
        if not self.training_active:
            return

        if self.exercise is not None:
            self.exercise.stop()

        self.finish_training()

    # ==================================================
    # KIOSK
    # ==================================================
    def _enable_kiosk(self) -> None:
        fullscreen = self.cfg.getboolean("app", "fullscreen", fallback=True)
        topmost = self.cfg.getboolean("app", "topmost", fallback=True)
        hide_cursor = self.cfg.getboolean("app", "hide_cursor", fallback=True)

        if fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            # windowed ზომები მხოლოდ fullscreen=false-ზე გამოიყენება
            w = self.cfg.getint("app", "width", fallback=1280)
            h = self.cfg.getint("app", "height", fallback=800)
            self.root.geometry(f"{w}x{h}")

        if topmost:
            self.root.attributes("-topmost", True)

        if hide_cursor:
            self.root.config(cursor="none")

        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def _disable_kiosk(self) -> None:
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.config(cursor="")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ==================================================
    # HELPERS
    # ==================================================
    def _load_sentences(self) -> list[str]:
        path = self.cfg.get("training", "sentence_file", fallback="data/sentences.txt")

        try:
            with open(path, encoding="utf-8") as f:
                lines = [line.strip().upper() for line in f if line.strip()]
        except Exception as e:
            msg = self.res.text("errors", "file_missing").format(path=path, err=str(e))
            raise RuntimeError(msg) from e

        if not lines:
            raise RuntimeError(self.res.text("errors", "file_empty"))

        return lines

    # ==================================================
    # ABOUT
    # ==================================================
    def _about(self) -> None:
        messagebox.showinfo(
            self.res.text("app", "about", fallback="About"),
            self.res.text("dialogs", "about_text", fallback="KLAVA"),
        )
