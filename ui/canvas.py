# ui/canvas.py
# KLAVA — Canvas drawing layer (UI only)

from __future__ import annotations

import tkinter as tk

from collections.abc import Callable
from configparser import ConfigParser

from ui.hand_placement import welcome_image

SENTENCE_Y = 130
MAX_LETTER_SPACING = 70.0
SENTENCE_WIDTH_RATIO = 0.92
MIN_SENTENCE_FONT = 12
WELCOME_RESIZE_DELAY_MS = 120


class Canvas:
    """
    Canvas UI ფენა.

    Does:
    - ხატავს ტექსტს და HUD-ს
    - მართავს cover overlay-ს
    - hide/show keyboard tag-ს

    Does not:
    - ითვლის ლოგიკას
    """

    def __init__(self, root: tk.Tk, theme: ConfigParser) -> None:
        self.root = root
        self.theme = theme

        ui = theme["ui"] if "ui" in theme else {}

        self.bg = ui.get("bg", "white")
        self.pale = ui.get("pale", "#cccccc")
        self.dark = ui.get("dark", "#000000")
        self.cover_bg = ui.get("cover_bg", "white")
        self.cover_text_color = ui.get("cover_text_color", "black")

        self.font_family = ui.get("font_family", "Arial")
        self.font_sentence = int(ui.get("font_sentence", "50"))
        self.font_cover = int(ui.get("font_cover", "44"))

        self.canvas = tk.Canvas(root, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()

        self.text_ids: list[int] = []

        # HUD ids
        self.timer_display: int | None = None
        self.score_display: int | None = None
        self.result_display: int | None = None

        # Cover overlay
        self.cover_rect = self.canvas.create_rectangle(
            0,
            0,
            self.width,
            self.height,
            fill=self.cover_bg,
            outline="",
            tags=("cover",),
        )
        self.cover_text = self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text="",
            font=(self.font_family, self.font_cover, "bold"),
            fill=self.cover_text_color,
            tags=("cover",),
        )
        self.cover_image = self.canvas.create_image(0, 0, anchor="nw", tags=("cover",), state="hidden")
        self._welcome_image = None
        self._welcome_visible = False
        self._welcome_job: str | None = None
        self._resize_listeners: list[Callable[[int, int], None]] = []
        self.canvas.tag_raise("cover")
        self.canvas.bind("<Configure>", self._resize_cover)

    def add_resize_listener(self, callback: Callable[[int, int], None]) -> None:
        """Call callback(width, height) whenever the canvas size changes."""
        self._resize_listeners.append(callback)

    def _resize_cover(self, event: tk.Event) -> None:
        """Keep cover, sentence and listeners (keyboard) fitted to the current window."""
        width, height = max(1, event.width), max(1, event.height)
        self.width, self.height = width, height
        self.canvas.coords(self.cover_rect, 0, 0, width, height)
        self.canvas.coords(self.cover_text, width / 2, height / 2)
        size = max(16, min(self.font_cover, int(min(width / 13, height / 8))))
        self.canvas.itemconfigure(
            self.cover_text,
            font=(self.font_family, size, "bold"),
            width=max(1, int(width * 0.88)),
            justify="center",
        )
        self._layout_sentence()
        for callback in self._resize_listeners:
            callback(width, height)
        # Items redrawn by listeners must stay below an active cover.
        self.canvas.tag_raise("cover")
        if self._welcome_visible:
            # Rescaling the artwork is slow; do it once the window stops changing.
            if self._welcome_job is not None:
                self.canvas.after_cancel(self._welcome_job)
            self._welcome_job = self.canvas.after(WELCOME_RESIZE_DELAY_MS, self._refresh_welcome)

    def _refresh_welcome(self) -> None:
        self._welcome_job = None
        if not self._welcome_visible:
            return
        self._welcome_image = welcome_image(self.width, self.height)
        if self._welcome_image is not None:
            self.canvas.itemconfigure(self.cover_image, image=self._welcome_image)

    # ------------------------------
    def hide_keyboard(self) -> None:
        self.canvas.itemconfigure("keyboard", state="hidden")

    def show_keyboard(self) -> None:
        self.canvas.itemconfigure("keyboard", state="normal")

    # ------------------------------
    def show_start_cover(self) -> None:
        """Display instructional hand positions on the initial cover."""
        self._welcome_visible = True
        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        self._welcome_image = welcome_image(width, height)
        if self._welcome_image is None:
            self._welcome_visible = False
            self.show_cover("KLAVA")
            return
        self.canvas.itemconfigure(self.cover_image, image=self._welcome_image, state="normal")
        self.canvas.itemconfigure(self.cover_text, text="", state="hidden")
        self.canvas.itemconfigure("cover", state="normal")
        self.canvas.tag_raise("cover")

    def show_cover(self, text: str) -> None:
        self._welcome_visible = False
        self.canvas.itemconfigure(self.cover_image, state="hidden")
        self.canvas.itemconfigure(self.cover_text, state="normal")
        self.canvas.itemconfig(self.cover_text, text=text)
        self.canvas.itemconfigure("cover", state="normal")
        self.canvas.tag_raise("cover")

    def hide_cover(self) -> None:
        self.canvas.itemconfigure("cover", state="hidden")

    # ------------------------------
    def clear(self) -> None:
        self.canvas.delete("sentence")
        self.canvas.delete("hud")
        self.text_ids.clear()

    # ------------------------------
    def draw_sentence(self, letters: list[str]) -> None:
        self.clear_sentence()

        for ch in letters:
            tid = self.canvas.create_text(
                0,
                SENTENCE_Y,
                text=ch,
                fill=self.pale,
                tags=("sentence",),
            )
            self.text_ids.append(tid)
        self._layout_sentence()

    def sentence_layout(self, count: int) -> tuple[float, float, int]:
        """Return (first letter centre x, spacing px, font size) fitting the width.

        Lines that fit keep the theme's 70 px spacing and font size; longer lines
        shrink spacing and font together instead of running off the screen.
        """
        count = max(1, count)
        spacing = min(MAX_LETTER_SPACING, self.width * SENTENCE_WIDTH_RATIO / count)
        size = self.font_sentence
        if spacing < MAX_LETTER_SPACING:
            size = max(MIN_SENTENCE_FONT, int(self.font_sentence * spacing / MAX_LETTER_SPACING))
        first_x = self.width / 2 - spacing * (count - 1) / 2
        return first_x, spacing, size

    def _layout_sentence(self) -> None:
        if not self.text_ids:
            return
        first_x, spacing, size = self.sentence_layout(len(self.text_ids))
        for i, tid in enumerate(self.text_ids):
            self.canvas.coords(tid, first_x + i * spacing, SENTENCE_Y)
            self.canvas.itemconfigure(tid, font=(self.font_family, size, "bold"))

    def clear_sentence(self) -> None:
        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids.clear()

    def mark_letter(self, index: int) -> None:
        if 0 <= index < len(self.text_ids):
            self.canvas.itemconfig(self.text_ids[index], fill=self.dark)

    # ------------------------------
    def draw_score_timer(self) -> None:
        # ეს ფუნქციონალი შენს მომავალ ლოგიკაზეა (ახლა არ ვიყენებთ)
        self.timer_display = self.canvas.create_text(
            120,
            self.height - 130,
            text="0",
            font=(self.font_family, 40, "bold"),
            fill="blue",
            tags=("hud",),
        )

        self.score_display = self.canvas.create_text(
            self.width - 120,
            self.height - 130,
            text="0",
            font=(self.font_family, 40, "bold"),
            fill="green",
            tags=("hud",),
        )

        self.result_display = self.canvas.create_text(
            self.width / 2,
            self.height - 70,
            text="",
            font=(self.font_family, 28, "bold"),
            fill="purple",
            tags=("hud",),
        )

    def update_score(self, score: int) -> None:
        if self.score_display is not None:
            self.canvas.itemconfig(self.score_display, text=str(score))

    def update_timer(self, seconds: int) -> None:
        if self.timer_display is not None:
            self.canvas.itemconfig(self.timer_display, text=str(seconds))

    def show_result(self, text: str) -> None:
        if self.result_display is not None:
            self.canvas.itemconfig(self.result_display, text=text)
