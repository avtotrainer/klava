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

    def clear(self):
        """
        ეკრანის გაწმენდა.

        ეს არის სტაბილური API, რომელსაც Trainer და Exercises იყენებენ.
        """
        self.canvas.delete("all")

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

    # ======================================================
    #   წინადადება
    # ======================================================
    def draw_sentence(self, letters):
        """
        ხატავს წინადადებას ღია ფერით (PALE).

        შენიშვნა:
        - ძველი ტექსტი აქ არ იშლება
        - წაშლა ხდება Trainer-იდან clear_sentence()-ით
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
            )
            self.text_ids.append(tid)

    def clear_sentence(self):
        """
        შლის ეკრანზე არსებულ ყველა ასოს.
        """
        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids.clear()

    def shade_letter(self, index: int):
        """
        სწორად აკრეფილი ასოს გამუქება.

        დაცვა:
        - არასწორი index არ აგდებს პროგრამას
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
        """
        ქულის განახლება.

        დაცვა:
        - თუ score_display ჯერ არ არსებობს — არაფერს ვაკეთებთ
        """
        if self.score_display is None:
            return
        self.canvas.itemconfig(self.score_display, text=str(score))

    def update_timer(self, seconds):
        """
        ტაიმერის განახლება წამებში.

        დაცვა:
        - თუ timer_display ჯერ არ არსებობს — არაფერს ვაკეთებთ
        """
        if self.timer_display is None:
            return
        self.canvas.itemconfig(self.timer_display, text=str(seconds))

    def show_result(self, text):
        """
        საბოლოო შედეგის ჩვენება.

        დაცვა:
        - თუ result_display ჯერ არ არსებობს — არაფერს ვაკეთებთ
        """
        if self.result_display is None:
            return
        self.canvas.itemconfig(self.result_display, text=text)
