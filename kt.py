import tkinter as tk
import random


KEYBOARD = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]


class KeyboardTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("კლავიატურის ტრენაჟორი")
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.key_boxes = {}  # letter → (rect_id, text_id)
        self.target_letter = None

        self.draw_keyboard()
        self.new_task()

        root.bind("<Key>", self.on_key_press)

    # --- მომრგვალებული მართკუთხედის დახაზვა ---
    def round_rect(self, x1, y1, x2, y2, r=20, **kwargs):
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

    # --- კლავიატურის ესკიზი ---
    def draw_keyboard(self):
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()

        key_w = width / 12
        key_h = height / 8
        gap = key_w * 0.12  # კლავიშებს შორის დაშორება
        radius = 18  # კუთხეების მომრგვალება

        start_y = height / 3

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

                # ტექსტი თავიდან ცარიელია
                text_id = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text="",
                    font=("Arial", int(key_h * 0.40), "bold"),
                    fill="black",
                )

                self.key_boxes[letter] = (rect_id, text_id)

    # --- ახალი ასოს ამოცანა ---
    def new_task(self):
        # წინა ასო გასუფთავდეს
        if self.target_letter:
            rect_id, text_id = self.key_boxes[self.target_letter]
            self.canvas.itemconfig(text_id, text="")
            self.canvas.itemconfig(rect_id, fill="#e8e8e8")

        self.target_letter = random.choice([l for row in KEYBOARD for l in row])

        rect_id, text_id = self.key_boxes[self.target_letter]
        self.canvas.itemconfig(rect_id, fill="yellow")
        self.canvas.itemconfig(text_id, text=self.target_letter)

    # --- ღილაკის დაჭერის დამუშავება ---
    def on_key_press(self, event):
        pressed = event.char.upper()

        # შეცდომით დაჭერილიც უნდა აინთოს წითლად
        if pressed in self.key_boxes and pressed != self.target_letter:
            rect_id, text_id = self.key_boxes[pressed]
            old_color = self.canvas.itemcget(rect_id, "fill")

            self.canvas.itemconfig(rect_id, fill="red")
            self.root.after(
                200, lambda: self.canvas.itemconfig(rect_id, fill=old_color)
            )

        # სწორი პასუხი
        if pressed == self.target_letter:
            rect_id, text_id = self.key_boxes[self.target_letter]
            self.canvas.itemconfig(rect_id, fill="lightgreen")

            self.root.after(300, self.new_task)


# --- პროგრამის გაშვება ---
root = tk.Tk()
trainer = KeyboardTrainer(root)
root.mainloop()
