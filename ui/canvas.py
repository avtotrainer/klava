# ui/canvas.py
# KLAVA — Canvas drawing layer
# პასუხისმგებელია ტექსტზე, ქულებზე, დროზე და შედეგებზე

import tkinter as tk

PALE = "#cccccc"
DARK = "#000000"


class Canvas:
    """
    Canvas UI ფენა.
    ლოგიკა აქ არ ითვლება — მხოლოდ ვიზუალი.
    """

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()

        self.text_ids = []

        self.timer_display = None
        self.score_display = None
        self.result_display = None

    # ======================================================
    #   კლავიატურის ვიზუალური გასუფთავება
    # ======================================================
    def clear_keyboard(self):
        """
        ასუფთავებს კლავიატურის ყველა highlight-ს.
        გამოიყენება წინადადების შეცვლისას და reset-ზე.
        """
        for item in self.canvas.find_withtag("key"):
            self.canvas.itemconfig(item, fill="#eee")

    # ======================================================
    #   წინადადების დახატვა (ძველი დიზაინი)
    # ======================================================
    def draw_sentence(self, letters):
        """
        ხატავს წინადადებას ღია ფერით (PALE),
        ზუსტად ძველი Trainer-ის ლოგიკით.
        """
        self.text_ids.clear()

        y = 130
        spacing = min(70, max(40, self.width * 0.75 / len(letters)))
        total = spacing * len(letters)
        start_x = self.width / 2 - total / 2

        for i, ch in enumerate(letters):
            display = ch if ch != " " else " "
            tid = self.canvas.create_text(
                start_x + i * spacing,
                y,
                text=display,
                font=("Arial", 50, "bold"),
                fill=PALE,
            )
            self.text_ids.append(tid)

    def shade_letter(self, index):
        """სწორად აკრეფილი ასოს გამუქება"""
        self.canvas.itemconfig(self.text_ids[index], fill=DARK)

    # ======================================================
    #   ქულები + ტაიმერი
    # ======================================================
    def draw_score_timer(self):
        self.timer_display = self.canvas.create_text(
            120,
            self.height - 130,
            text="0",
            font=("Arial", 40, "bold"),
            fill="blue",
        )

        self.score_display = self.canvas.create_text(
            self.width - 120,
            self.height - 130,
            text="0",
            font=("Arial", 40, "bold"),
            fill="green",
        )

        self.result_display = self.canvas.create_text(
            self.width / 2,
            self.height - 70,
            text="",
            font=("Arial", 28, "bold"),
            fill="purple",
        )

    def update_score(self, score):
        self.canvas.itemconfig(self.score_display, text=str(score))

    def update_timer(self, seconds):
        self.canvas.itemconfig(self.timer_display, text=str(seconds))

    def show_result(self, text):
        self.canvas.itemconfig(self.result_display, text=text)

    def clear_sentence(self):
        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids.clear()
