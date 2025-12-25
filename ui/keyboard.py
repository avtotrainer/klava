# ui/keyboard.py
# KLAVA — Screen Keyboard (ძველი დიზაინის პორტი)

PALE = "#cccccc"
DARK = "#000000"

KEYBOARD = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
]


class Keyboard:
    """
    ეკრანის კლავიატურა.
    ზუსტად იმავე ზომებით, განლაგებით და ფერებით,
    რაც ძველ Trainer-ში იყო.
    """

    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.width = screen_width
        self.height = screen_height

        self.key_boxes = {}

        self._draw_keys()

    # ======================================================
    #   დამრგვალებული ღილაკი
    # ======================================================
    def _round_rect(self, x1, y1, x2, y2, r=15, **kw):
        pts = [
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
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    # ======================================================
    #   კლავიატურის დახატვა
    # ======================================================
    def _draw_keys(self):
        key_w = self.width / 12
        key_h = self.height / 8
        gap = key_w * 0.12
        y0 = self.height / 3

        # ასოები
        for r, row in enumerate(KEYBOARD):
            row_w = len(row) * (key_w + gap)
            x0 = self.width / 2 - row_w / 2

            for c, ch in enumerate(row):
                x1 = x0 + c * (key_w + gap)
                y1 = y0 + r * (key_h + gap)
                x2 = x1 + key_w
                y2 = y1 + key_h

                rect = self._round_rect(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#eeeeee",
                    outline="#444",
                    width=2,
                )
                txt = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=ch,
                    font=("Arial", int(key_h * 0.35), "bold"),
                    fill=PALE,
                )
                self.key_boxes[ch] = (rect, txt)

        # SPACE
        space_w = key_w * 6
        x1 = self.width / 2 - space_w / 2
        x2 = x1 + space_w
        y1 = y0 + 3 * (key_h + gap)
        y2 = y1 + key_h

        rect = self._round_rect(
            x1,
            y1,
            x2,
            y2,
            fill="#eeeeee",
            outline="#444",
            width=2,
        )
        txt = self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="SPACE",
            font=("Arial", int(key_h * 0.3), "bold"),
            fill=PALE,
        )

        self.key_boxes[" "] = (rect, txt)

    # ======================================================
    #   ჰაილაითი
    # ======================================================
    def highlight(self, ch, color="yellow"):
        if ch in self.key_boxes:
            rect, txt = self.key_boxes[ch]
            self.canvas.itemconfig(rect, fill=color)
            self.canvas.itemconfig(txt, fill=DARK)

    def reset_key(self, ch):
        if ch in self.key_boxes:
            rect, txt = self.key_boxes[ch]
            self.canvas.itemconfig(rect, fill="#eeeeee")
            self.canvas.itemconfig(txt, fill=PALE)

    def clear_all(self):
        for rect, txt in self.key_boxes.values():
            self.canvas.itemconfig(rect, fill="#eeeeee")
            self.canvas.itemconfig(txt, fill=PALE)
