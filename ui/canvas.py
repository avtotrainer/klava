# ui/canvas.py
# KLAVA — Canvas drawing layer
# პასუხისმგებელია ტექსტზე, ქულებზე, დროზე და შედეგებზე
# ლოგიკა აქ არ ითვლება — მხოლოდ ვიზუალი

import tkinter as tk

PALE = "#cccccc"
DARK = "#000000"


class Canvas:
    """
    Canvas UI ფენა.
    Trainer იძახებს, Canvas ხატავს.
    """

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()

        # ტექსტის ID-ები (ერთი წინადადება)
        self.text_ids: list[int] = []

        # სტატუსის ელემენტები
        self.timer_display = None
        self.score_display = None
        self.result_display = None

        # ── COVER OVERLAY ─────────────────────────

        self.cover_rect = self.canvas.create_rectangle(
            0,
            0,
            self.width,
            self.height,
            fill="white",
            outline="",
            tags=("cover",),
        )

        self.cover_text = self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text="",
            font=("Arial", 44, "bold"),
            fill="black",
            tags=("cover",),
        )

        # cover ნაგულისხმევად ჩანს
        self.canvas.tag_raise("cover")

    # ======================================================
    #   კლავიატურის ხილვადობა
    # ======================================================
    def hide_keyboard(self):
        """
        კლავიატურის დამალვა (cover page-ზე).
        """
        self.canvas.itemconfigure("keyboard", state="hidden")

    def show_keyboard(self):
        """
        კლავიატურის გამოჩენა (ტრენინგის დაწყებისას).
        """
        self.canvas.itemconfigure("keyboard", state="normal")

        # ======================================================

    #   COVER OVERLAY
    # ======================================================
    def show_cover(self, text: str):
        """
        ფარდის ჩვენება ტექსტით (მენიუ / დასრულება).
        """
        self.canvas.itemconfig(self.cover_text, text=text)
        self.canvas.itemconfigure("cover", state="normal")
        self.canvas.tag_raise("cover")

    def hide_cover(self):
        """
        ფარდის დამალვა (ტრენინგის დაწყება).
        """
        self.canvas.itemconfigure("cover", state="hidden")

    # ======================================================
    #   საერთო გაწმენდა (უსაფრთხო)
    # ======================================================
    def clear(self):
        """
        ეკრანის გაწმენდა.

        მნიშვნელოვანია:
        - არ შლის კლავიატურას
        - შლის მხოლოდ sentence და hud ელემენტებს
        """
        self.canvas.delete("sentence")
        self.canvas.delete("hud")
        self.text_ids.clear()

    # ======================================================
    #   წინადადება
    # ======================================================
    def draw_sentence(self, letters):
        """
        ხატავს წინადადებას ღია ფერით (PALE).
        """
        self.text_ids.clear()

        y = 130
        spacing = min(70, max(40, self.width * 0.75 / len(letters)))
        total = spacing * len(letters)
        start_x = self.width / 2 - total / 2

        for i, ch in enumerate(letters):
            tid = self.canvas.create_text(
                start_x + i * spacing,
                y,
                text=ch if ch != " " else " ",
                font=("Arial", 50, "bold"),
                fill=PALE,
                tags=("sentence",),
            )
            self.text_ids.append(tid)

    def clear_sentence(self):
        """
        შლის მხოლოდ წინადადების ასოებს.
        """
        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids.clear()

    def shade_letter(self, index: int):
        """
        სწორად აკრეფილი ასოს გამუქება.
        """
        if 0 <= index < len(self.text_ids):
            self.canvas.itemconfig(self.text_ids[index], fill=DARK)

    # ======================================================
    #   ქულები და ტაიმერი
    # ======================================================
    def draw_score_timer(self):
        """
        ხატავს ტაიმერს, ქულებს და შედეგის ველს.
        იძახება ერთხელ Trainer-ის init-ში.
        """
        self.timer_display = self.canvas.create_text(
            120,
            self.height - 130,
            text="0",
            font=("Arial", 40, "bold"),
            fill="blue",
            tags=("hud",),
        )

        self.score_display = self.canvas.create_text(
            self.width - 120,
            self.height - 130,
            text="0",
            font=("Arial", 40, "bold"),
            fill="green",
            tags=("hud",),
        )

        self.result_display = self.canvas.create_text(
            self.width / 2,
            self.height - 70,
            text="",
            font=("Arial", 28, "bold"),
            fill="purple",
            tags=("hud",),
        )

    def update_score(self, score):
        """
        ქულის განახლება.
        """
        if self.score_display is None:
            return
        self.canvas.itemconfig(self.score_display, text=str(score))

    def update_timer(self, seconds):
        """
        ტაიმერის განახლება წამებში.
        """
        if self.timer_display is None:
            return
        self.canvas.itemconfig(self.timer_display, text=str(seconds))

    def show_result(self, text):
        """
        საბოლოო შედეგის ჩვენება.
        """
        if self.result_display is None:
            return
        self.canvas.itemconfig(self.result_display, text=text)
