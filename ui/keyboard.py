# ui/keyboard.py
# KLAVA — Screen Keyboard (model + theme)

from __future__ import annotations

import tkinter as tk
from typing import Dict, Optional, TypedDict


KEYBOARD = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
]


class KeyBox(TypedDict):
    rect: int
    text: int
    base_fill: str
    outline: str


class Keyboard:
    """
    UI keyboard.

    Base color:
    - თუ use_finger_colors=True -> მოდის keyboard_model-ის colors-იდან
    - თუ False -> ერთფეროვანი idle

    Overlay colors:
    - target/correct/wrong მოდის theme-იდან
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        screen_width: int,
        screen_height: int,
        *,
        keyboard_model: dict,
        use_finger_colors: bool,
        finger_lighten_factor: float,
        color_target: str,
        color_correct: str,
        color_wrong: str,
        text_pale: str,
        text_dark: str,
        key_radius: int,
        key_gap_ratio: float = 0.12,
    ):
        self.canvas = canvas
        self.width = screen_width
        self.height = screen_height

        self.use_finger_colors = use_finger_colors
        self.finger_lighten_factor = finger_lighten_factor

        self.COLOR_TARGET = color_target
        self.COLOR_CORRECT = color_correct
        self.COLOR_WRONG = color_wrong
        self.TEXT_PALE = text_pale
        self.TEXT_DARK = text_dark

        self.key_radius = key_radius
        self.key_gap_ratio = key_gap_ratio

        self.FINGER_GROUPS = {k: set(v) for k, v in keyboard_model["groups"].items()}
        self.FINGER_COLORS = keyboard_model["colors"]

        self.key_boxes: Dict[str, KeyBox] = {}
        self.current_target: Optional[str] = None

        self._draw_keys()

    # ----------------------------
    def _finger_for_key(self, ch: str) -> Optional[str]:
        for finger, keys in self.FINGER_GROUPS.items():
            if ch in keys:
                return finger
        return None

    def _lighten(self, hex_color: str) -> str:
        factor = self.finger_lighten_factor
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)

        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _round_rect(self, x1, y1, x2, y2, r=16, **kw) -> int:
        r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(points, smooth=True, tags=("keyboard",), **kw)

    # ----------------------------
    def _draw_keys(self):
        key_w = self.width / 14
        key_h = self.height / 11
        gap = key_w * self.key_gap_ratio
        y0 = self.height / 3

        row_offsets = {
            0: 0,
            1: key_w / 6,
            2: key_w / 6 + key_w / 2,
        }

        for r, row in enumerate(KEYBOARD):
            offset = row_offsets[r]
            total_w = len(row) * (key_w + gap) - gap
            x0 = self.width / 2 - total_w / 2 - offset

            for c, ch in enumerate(row):
                x1 = x0 + c * (key_w + gap)
                y1 = y0 + r * (key_h + gap)

                outline, fill = self._base_colors(ch)

                rect = self._round_rect(
                    x1,
                    y1,
                    x1 + key_w,
                    y1 + key_h,
                    r=self.key_radius,
                    fill=fill,
                    outline=outline,
                    width=2,
                )
                txt = self.canvas.create_text(
                    x1 + key_w / 2,
                    y1 + key_h / 2,
                    text=ch,
                    font=("Arial", int(key_h * 0.42), "bold"),
                    fill=self.TEXT_PALE,
                    tags=("keyboard",),
                )

                self.key_boxes[ch] = {
                    "rect": rect,
                    "text": txt,
                    "base_fill": fill,
                    "outline": outline,
                }

    def _base_colors(self, ch: str) -> tuple[str, str]:
        if self.use_finger_colors:
            finger = self._finger_for_key(ch)
            if finger and finger in self.FINGER_COLORS:
                outline = self.FINGER_COLORS[finger]
                return outline, self._lighten(outline)

        # monochrome fallback
        outline = "#999999"
        fill = "#eeeeee"
        return outline, fill

    # ----------------------------
    def _set_key(self, key: str, fill: str, text_color: str):
        box = self.key_boxes.get(key)
        if not box:
            return
        self.canvas.itemconfig(box["rect"], fill=fill)
        self.canvas.itemconfig(box["text"], fill=text_color)

    def _reset_key(self, key: str):
        box = self.key_boxes.get(key)
        if not box:
            return
        self.canvas.itemconfig(
            box["rect"], fill=box["base_fill"], outline=box["outline"]
        )
        self.canvas.itemconfig(box["text"], fill=self.TEXT_PALE)

    # ----------------------------
    def clear(self):
        for key in self.key_boxes:
            self._reset_key(key)
        self.current_target = None

    def set_target(self, key: str):
        if self.current_target:
            self._reset_key(self.current_target)
        self.current_target = key
        self._set_key(key, self.COLOR_TARGET, self.TEXT_DARK)

    def highlight_correct(self, key: str):
        self._set_key(key, self.COLOR_CORRECT, self.TEXT_DARK)

    def highlight_wrong(self, key: str):
        self._set_key(key, self.COLOR_WRONG, self.TEXT_DARK)
        self.canvas.after(160, lambda k=key: self._reset_key(k))
