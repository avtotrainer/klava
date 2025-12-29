# ui/keyboard.py
# KLAVA — Screen Keyboard (authentic staggered layout, fixed)

from __future__ import annotations
import tkinter as tk

# ── ფერები ─────────────────────────────────────────
COLOR_IDLE = "#eeeeee"
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

# ui/keyboard.py

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
    "left_pinky": "#e53935",  # წითელი
    "left_ring": "#6d4c41",  # ყავისფერი
    "left_middle": "#fdd835",  # ყვითელი
    "left_index": "#43a047",  # მწვანე
    "right_index": "#fb8c00",  # ნარინჯისფერი
    "right_middle": "#3949ab",  # იასამნისფერი
    "right_ring": "#8e24aa",  # იისფერი
    "right_pinky": "#1e88e5",  #  ლურჯი
}


class Keyboard:
    """
    ეკრანის კლავიატურა — ავთენტური QWERTY განლაგებით.

    რიგები:
    - I რიგი: უცვლელი
    - II რიგი: მარცხნივ key_w / 6
    - III რიგი: მარცხნივ (key_w / 6 + key_w / 2)
    """

    def __init__(self, canvas: tk.Canvas, screen_width: int, screen_height: int):
        self.canvas = canvas
        self.width = screen_width
        self.height = screen_height

        self.key_boxes: dict[str, tuple[int, int]] = {}
        self.current_target: str | None = None
        self._wrong_flash_id: str | None = None

        self._draw_keys()

    def _finger_for_key(self, ch: str) -> str | None:
        """
        აბრუნებს თითის ჯგუფს მოცემული კლავიშისთვის.
        """
        for finger, keys in FINGER_GROUPS.items():
            if ch in keys:
                return finger
        return None

    @staticmethod
    def lighten_color(hex_color: str, factor: float = 0.85) -> str:
        """
        აბრუნებს უფრო ღია ფერს მოცემული HEX ფერისგან.
        factor ∈ [0.0, 1.0]
        """
        hex_color = hex_color.lstrip("#")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        return f"#{r:02x}{g:02x}{b:02x}"

    # ======================================================
    #   Drawing helpers
    # ======================================================
    def _round_rect(self, x1, y1, x2, y2, r=16, **kwargs):
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
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    # ======================================================
    #   Draw keyboard
    # ======================================================
    def _draw_keys(self):
        key_w = self.width / 14
        key_h = self.height / 11
        gap = key_w * 0.12
        y0 = self.height / 3

        # ავთენტური offset-ები (მარცხნივ!)
        row_offsets = {
            0: 0,
            1: key_w / 6,
            2: key_w / 6 + key_w / 2,
        }

        for r, row in enumerate(KEYBOARD):
            offset = row_offsets.get(r, 0)
            total_width = len(row) * (key_w + gap) - gap

            # ↓↓↓ აქ არის მთავარი გასწორება ↓↓↓
            x0 = self.width / 2 - total_width / 2 - offset

            for c, ch in enumerate(row):
                x1 = x0 + c * (key_w + gap)
                y1 = y0 + r * (key_h + gap)

                finger = self._finger_for_key(ch)
                outline = FINGER_COLORS[finger] if finger is not None else "#999999"
                fill = Keyboard.lighten_color(outline, factor=0.88)
                rect = self._round_rect(
                    x1,
                    y1,
                    x1 + key_w,
                    y1 + key_h,
                    r=18,
                    fill=fill,
                    outline=outline,
                    width=2,
                    tags=("keyboard",),
                )
                txt = self.canvas.create_text(
                    x1 + key_w / 2,
                    y1 + key_h / 2,
                    text=ch,
                    font=("Arial", int(key_h * 0.42), "bold"),
                    fill=TEXT_PALE,
                    tags=("keyboard",),
                )
                self.key_boxes[ch] = (rect, txt)

        # SPACE
        # --- SPACE (ავთენტური პოზიცია) ---
        # მესამე რიგის (ZXCVBNM) საწყისი x
        third_row_offset = key_w / 3 + key_w / 2
        third_row_total_width = len(KEYBOARD[2]) * (key_w + gap) - gap
        row3_x0 = self.width / 2 - third_row_total_width / 2 - third_row_offset

        # მესამე რიგის მესამე კლავიშის (index 2) x

        # SPACE სიგანე = 5 კლავიში + 5 gap
        space_x = row3_x0 + 2 * (key_w + gap) + gap
        space_w = 5 * key_w + 4 * gap

        space_y = y0 + 3 * (key_h + gap)

        rect = self._round_rect(
            space_x,
            space_y,
            space_x + space_w,
            space_y + key_h,
            r=22,
            fill=COLOR_IDLE,
            outline=BORDER_BLUE,
            width=2,
            tags=("keyboard",),
        )
        txt = self.canvas.create_text(
            space_x + space_w / 2,
            space_y + key_h / 2,
            text="SPACE",
            font=("Arial", int(key_h * 0.38), "bold"),
            fill=TEXT_PALE,
            tags=("keyboard",),
        )

        self.key_boxes[" "] = (rect, txt)
        self.key_boxes["SPACE"] = (rect, txt)

    # ======================================================
    #   State helpers
    # ======================================================
    def _set_key(self, key: str, color: str, text_color: str):
        if key not in self.key_boxes:
            return
        rect, txt = self.key_boxes[key]
        self.canvas.itemconfig(rect, fill=color)
        self.canvas.itemconfig(txt, fill=text_color)

    def _reset_key(self, key: str):
        self._set_key(key, COLOR_IDLE, TEXT_PALE)

    # ======================================================
    #   Public API
    # ======================================================
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
        if self._wrong_flash_id:
            self.canvas.after_cancel(self._wrong_flash_id)
            self._wrong_flash_id = None

        self._set_key(key, COLOR_WRONG, TEXT_DARK)
        self._wrong_flash_id = self.canvas.after(
            120,
            lambda k=key: self._reset_key(k),
        )
