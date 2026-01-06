# ui/canvas.py
# KLAVA — Canvas drawing layer (UI only)

from __future__ import annotations

import tkinter as tk
from configparser import ConfigParser


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
        self.canvas.tag_raise("cover")

    # ------------------------------
    def hide_keyboard(self) -> None:
        self.canvas.itemconfigure("keyboard", state="hidden")

    def show_keyboard(self) -> None:
        self.canvas.itemconfigure("keyboard", state="normal")

    # ------------------------------
    def show_cover(self, text: str) -> None:
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

        y = 130
        spacing = min(70, max(40, self.width * 0.75 / max(1, len(letters))))
        total = spacing * len(letters)
        start_x = self.width / 2 - total / 2

        for i, ch in enumerate(letters):
            tid = self.canvas.create_text(
                start_x + i * spacing,
                y,
                text=ch if ch != " " else " ",
                font=(self.font_family, self.font_sentence, "bold"),
                fill=self.pale,
                tags=("sentence",),
            )
            self.text_ids.append(tid)

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
