import tkinter as tk
import random


TARGET_TEXT = "HELLO WORLD"

KEYBOARD = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]

# >>> SPACE KEY ADDED <<<
SPECIAL_KEYS = ["SPACE"]  # მარტო space გვჭირდება ახლა


class KeyboardTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("კლავიატურის ტრენაჟორი")
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.progress_index = 0
        self.text_letters = list(TARGET_TEXT)

        self.text_display_id = None
        self.key_boxes = {}  # ასო → (rect_id, text_id)
        self.target_letter = None

        self.draw_text_area()
        self.draw_keyboard()
        self.set_next_target()

        root.bind("<Key>", self.on_key_press)

    # --- TEXT DISPLAY ---
    def draw_text_area(self):
        width = self.canvas.winfo_screenwidth()
        self.text_display_id = self.canvas.create_text(
            width / 2, 120, text="", font=("Arial", 60, "bold"), fill="black"
        )

    def update_text_display(self):
        current = "".join(self.text_letters[: self.progress_index])
        self.canvas.itemconfig(self.text_display_id, text=current)

    # --- Rounded Rectangle ---
    def round_rect(self, x1, y1, x2, y2, r=20, **kw):
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

    # --- Keyboard Drawing ---
    def draw_keyboard(self):
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()

        key_w = width / 12
        key_h = height / 8
        gap = key_w * 0.12
        radius = 18
        start_y = height / 3

        # --- ჩვეულებრივი კლავიშები ---
        for row_i, row in enumerate(KEYBOARD):
            row_width = len(row) * (key_w + gap)
            start_x = (width - row_width) / 2

            for col_i, letter in enumerate(row):
                x1 = start_x + col_i * (key_w + gap)
                y1 = start_y + row_i * (key_h + gap)
                x2 = x1 + key_w
                y2 = y1 + key_h

                rect_id = self.round_rect(
                    x1, y1, x2, y2, r=radius, fill="#e8e8e8", outline="#333", width=3
                )
                text_id = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text="",
                    font=("Arial", int(key_h * 0.4), "bold"),
                )

                self.key_boxes[letter] = (rect_id, text_id)

        # --- SPACE BAR (დიდი კლავიში) ---
        space_width = key_w * 5.5  # რეალურ პროპორციასთან ახლო
        space_x1 = (width - space_width) / 2
        space_x2 = space_x1 + space_width
        space_y1 = start_y + 3 * (key_h + gap)
        space_y2 = space_y1 + key_h

        rect_id = self.round_rect(
            space_x1,
            space_y1,
            space_x2,
            space_y2,
            r=radius,
            fill="#e8e8e8",
            outline="#333",
            width=3,
        )
        text_id = self.canvas.create_text(
            (space_x1 + space_x2) / 2,
            (space_y1 + space_y2) / 2,
            text="",
            font=("Arial", int(key_h * 0.4), "bold"),
        )

        # >>> SPACE KEY ADDED <<<
        self.key_boxes[" "] = (rect_id, text_id)

    # --- Target Letter Selection ---
    def set_next_target(self):
        if self.progress_index >= len(self.text_letters):
            self.canvas.create_text(
                self.canvas.winfo_screenwidth() / 2,
                250,
                text="მოგილოცავ! დასრულებულია!",
                font=("Arial", 60, "bold"),
                fill="green",
            )
            return

        self.target_letter = self.text_letters[self.progress_index]

        # skip visual for space if needed
        rect_id, text_id = self.key_boxes[self.target_letter]
        self.canvas.itemconfig(rect_id, fill="yellow")
        self.canvas.itemconfig(
            text_id, text="⎵" if self.target_letter == " " else self.target_letter
        )

    # --- Key Press Handling ---
    def on_key_press(self, event):
        pressed = event.char.upper() if event.char else ""

        # SPACE special case
        if event.keysym == "space":
            pressed = " "

        # no active target
        if self.target_letter is None:
            return

        # --- mistake ---
        if pressed != self.target_letter:
            if pressed in self.key_boxes:
                rect_id, text_id = self.key_boxes[pressed]
                old_color = self.canvas.itemcget(rect_id, "fill")

                self.canvas.itemconfig(rect_id, fill="red")
                self.canvas.itemconfig(text_id, text=pressed if pressed != " " else "⎵")

                def reset():
                    self.canvas.itemconfig(rect_id, fill=old_color)
                    self.canvas.itemconfig(text_id, text="")

                self.root.after(200, reset)
            return

        # --- correct key ---
        rect_id, text_id = self.key_boxes[self.target_letter]
        self.canvas.itemconfig(rect_id, fill="lightgreen")

        self.progress_index += 1
        self.update_text_display()

        def clear_and_next():
            self.canvas.itemconfig(rect_id, fill="#e8e8e8")
            self.canvas.itemconfig(text_id, text="")
            self.set_next_target()

        self.root.after(300, clear_and_next)


root = tk.Tk()
trainer = KeyboardTrainer(root)
root.mainloop()
