# ui/keyboard.py
# KLAVA — Screen Keyboard (SPACE restored, types cleaned)

from __future__ import annotations
import tkinter as tk
from typing import Dict, Optional, TypedDict

# ── ფერები ─────────────────────────────────────────
COLOR_IDLE_FALLBACK = "#eeeeee"
COLOR_TARGET = "#ffeb3b"
COLOR_CORRECT = "#7CFC9A"
COLOR_WRONG = "#ff4d4d"

TEXT_PALE = "#cccccc"
TEXT_DARK = "#000000"

BORDER_BLUE = "#3b82f6"

KEYBOARD = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
]

# ── თითების ჯგუფები ────────────────────────────────
FINGER_GROUPS = {
    "left_pinky": set("AQZ"),
    "left_ring": set("SWX"),
    "left_middle": set("DEC"),
    "left_index": set("FRVGTB"),
    "right_index": set("JUMHYN"),
    "right_middle": set("KI"),
    "right_ring": set("LO"),
    "right_pinky": set("P"),
}

FINGER_COLORS = {
    "left_pinky": "#e53935",
    "left_ring": "#6d4c41",
    "left_middle": "#fdd835",
    "left_index": "#43a047",
    "right_index": "#fb8c00",
    "right_middle": "#3949ab",
    "right_ring": "#8e24aa",
    "right_pinky": "#1e88e5",
}


# ── Typed storage for keys ─────────────────────────
class KeyBox(TypedDict):
    rect: int
    text: int
    base_fill: str
    outline: str
    center_x: float


class Keyboard:
    def __init__(self, canvas: tk.Canvas, screen_width: int, screen_height: int):
        self.canvas = canvas
        self.width = screen_width
        self.height = screen_height

        self.key_boxes: Dict[str, KeyBox] = {}
        self.current_target: Optional[str] = None
        self._wrong_flash_id: Optional[str] = None

        self.finger_centers: Dict[str, float] = {}

        self._draw_keys()
        self._compute_finger_centers()
        self._draw_finger_legend()

    # ==================================================
    #   Helpers
    # ==================================================
    def _finger_for_key(self, ch: str) -> Optional[str]:
        for finger, keys in FINGER_GROUPS.items():
            if ch in keys:
                return finger
        return None

    @staticmethod
    def lighten_color(hex_color: str, factor: float = 0.88) -> str:
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
        return self.canvas.create_polygon(points, smooth=True, **kw)

    # ==================================================
    #   Draw keyboard + SPACE
    # ==================================================
    def _draw_keys(self):
        key_w = self.width / 14
        key_h = self.height / 11
        gap = key_w * 0.12
        y0 = self.height / 3

        row_offsets = {
            0: 0,
            1: key_w / 6,
            2: key_w / 6 + key_w / 2,
        }

        # --- letter keys ---
        for r, row in enumerate(KEYBOARD):
            offset = row_offsets[r]
            total_w = len(row) * (key_w + gap) - gap
            x0 = self.width / 2 - total_w / 2 - offset

            for c, ch in enumerate(row):
                x1 = x0 + c * (key_w + gap)
                y1 = y0 + r * (key_h + gap)

                finger = self._finger_for_key(ch)
                outline = FINGER_COLORS[finger] if finger else "#999999"
                fill = self.lighten_color(outline)

                rect = self._round_rect(
                    x1,
                    y1,
                    x1 + key_w,
                    y1 + key_h,
                    r=18,
                    fill=fill,
                    outline=outline,
                    width=2,
                )
                txt = self.canvas.create_text(
                    x1 + key_w / 2,
                    y1 + key_h / 2,
                    text=ch,
                    font=("Arial", int(key_h * 0.42), "bold"),
                    fill=TEXT_PALE,
                )

                self.key_boxes[ch] = {
                    "rect": rect,
                    "text": txt,
                    "base_fill": fill,
                    "outline": outline,
                    "center_x": x1 + key_w / 2,
                }

        # --- SPACE ---
        third_offset = key_w / 3 + key_w / 2
        row3_w = len(KEYBOARD[2]) * (key_w + gap) - gap
        row3_x0 = self.width / 2 - row3_w / 2 - third_offset

        space_x = row3_x0 + 2 * (key_w + gap) + gap
        space_w = 5 * key_w + 4 * gap
        space_y = y0 + 3 * (key_h + gap)

        rect = self._round_rect(
            space_x,
            space_y,
            space_x + space_w,
            space_y + key_h,
            r=22,
            fill=COLOR_IDLE_FALLBACK,
            outline=BORDER_BLUE,
            width=2,
        )
        txt = self.canvas.create_text(
            space_x + space_w / 2,
            space_y + key_h / 2,
            text="SPACE",
            font=("Arial", int(key_h * 0.38), "bold"),
            fill=TEXT_PALE,
        )

        self.key_boxes[" "] = {
            "rect": rect,
            "text": txt,
            "base_fill": COLOR_IDLE_FALLBACK,
            "outline": BORDER_BLUE,
            "center_x": space_x + space_w / 2,
        }
        self.key_boxes["SPACE"] = self.key_boxes[" "]

    # ==================================================
    #   Finger centers (SPACE excluded)
    # ==================================================
    def _compute_finger_centers(self):
        acc: Dict[str, list[float]] = {}

        for ch, box in self.key_boxes.items():
            if ch in (" ", "SPACE"):
                continue
            finger = self._finger_for_key(ch)
            if finger:
                acc.setdefault(finger, []).append(box["center_x"])

        self.finger_centers = {f: sum(xs) / len(xs) for f, xs in acc.items()}

    # ==================================================
    #   Legend (unchanged, just lower)
    # ==================================================
    def _draw_finger_legend(self):
        finger_w = 36
        finger_h = 90
        nail_w = 26
        nail_h = 18

        y = self.height / 3 + 5.0 * (self.height / 11)

        for finger, cx in self.finger_centers.items():
            x = cx - finger_w / 2
            light = self.lighten_color(FINGER_COLORS[finger])

            self._round_rect(
                x,
                y,
                x + finger_w,
                y + finger_h,
                r=int(finger_w / 2),
                fill=light,
                outline=light,
                width=2,
            )

            nx = x + (finger_w - nail_w) / 2
            ny = y + 16
            self._round_rect(
                nx,
                ny,
                nx + nail_w,
                ny + nail_h,
                r=int(nail_h / 2),
                fill="#F5F5F5",
                outline="#E0E0E0",
                width=2,
            )

    # ==================================================
    #   Public API (SPACE works)
    # ==================================================
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
        self.canvas.itemconfig(box["text"], fill=TEXT_PALE)

    def clear(self):
        for key in self.key_boxes:
            self._reset_key(key)
        self.current_target = None

    def set_target(self, key: str):
        if self.current_target:
            self._reset_key(self.current_target)
        self.current_target = key
        self._set_key(key, COLOR_TARGET, TEXT_DARK)

    def highlight_correct(self, key: str):
        self._set_key(key, COLOR_CORRECT, TEXT_DARK)

    def highlight_wrong(self, key: str):
        self._set_key(key, COLOR_WRONG, TEXT_DARK)
        self.canvas.after(160, lambda k=key: self._reset_key(k))
