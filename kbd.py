import tkinter as tk
import time

SENTENCE_FILE = "sentences.txt"

KEYBOARD = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]

PALE = "#c8c8c8"
DARK = "#000000"


class Trainer:
    def __init__(self, root):
        self.root = root
        root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # SENTENCES
        self.sentences = self.load_sentences()
        self.sentence_idx = 0

        self.current_sentence = self.sentences[self.sentence_idx]
        self.letters = list(self.current_sentence)

        # STATE
        self.pos = 0
        self.score = 0
        self.running = True

        # TIMER
        self.timer_started = False
        self.start_time = None
        self.timer_id = None

        # UI DATA
        self.text_ids = []
        self.key_boxes = {}
        self.target = None

        self.timer_display = None
        self.score_display = None
        self.result_display = None

        # DRAW
        self.draw_sentence()
        self.draw_keyboard()
        self.draw_score_timer()
        self.draw_exit()

        self.set_target()

        root.bind("<Key>", self.on_key)

    # ----------------------------------------------------------
    # LOAD SENTENCES
    # ----------------------------------------------------------
    def load_sentences(self):
        try:
            with open(SENTENCE_FILE, "r", encoding="utf-8") as f:
                lines = [l.strip().upper() for l in f if l.strip()]
                return lines if lines else ["HELLO WORLD"]
        except:
            return ["HELLO WORLD"]

    # ----------------------------------------------------------
    # DRAW SENTENCE WITH GOOD SPACING
    # ----------------------------------------------------------
    def draw_sentence(self):
        width = self.canvas.winfo_screenwidth()
        y = 130

        # bigger spacing
        min_space = 40
        max_space = 70
        spacing = min(max_space, max(min_space, width * 0.75 / len(self.letters)))

        total_width = len(self.letters) * spacing
        start_x = width / 2 - total_width / 2

        for i, ch in enumerate(self.letters):
            display = ch if ch != " " else " "
            tid = self.canvas.create_text(
                start_x + i * spacing,
                y,
                text=display,
                font=("Arial", 50, "bold"),
                fill=PALE,
            )
            self.text_ids.append(tid)

    # ----------------------------------------------------------
    # DARKEN LETTER
    # ----------------------------------------------------------
    def shade(self, index):
        self.canvas.itemconfig(self.text_ids[index], fill=DARK)

    # ----------------------------------------------------------
    # EXIT BUTTON
    # ----------------------------------------------------------
    def draw_exit(self):
        width = self.canvas.winfo_screenwidth()
        btn = tk.Button(
            self.root,
            text="EXIT",
            font=("Arial", 22, "bold"),
            bg="red",
            fg="white",
            command=self.root.destroy,
        )
        btn.place(x=width - 150, y=20, width=120, height=50)

    # ----------------------------------------------------------
    # TIMER & SCORE
    # ----------------------------------------------------------
    def draw_score_timer(self):
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()

        self.timer_display = self.canvas.create_text(
            120, height - 130, text="0", font=("Arial", 40, "bold"), fill="blue"
        )

        self.score_display = self.canvas.create_text(
            width - 120,
            height - 130,
            text="0",
            font=("Arial", 40, "bold"),
            fill="green",
        )

        self.result_display = self.canvas.create_text(
            width / 2, height - 80, text="", font=("Arial", 28, "bold"), fill="purple"
        )

    def start_timer(self):
        if not self.timer_started or not self.running:
            return

        elapsed = int(time.time() - self.start_time)
        self.canvas.itemconfig(self.timer_display, text=str(elapsed))
        self.timer_id = self.root.after(1000, self.start_timer)

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=str(self.score))

    # ----------------------------------------------------------
    # KEYBOARD
    # ----------------------------------------------------------
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

    def draw_keyboard(self):
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()

        key_w = width / 12
        key_h = height / 8
        gap = key_w * 0.12
        y0 = height / 3

        # letters
        for row_i, row in enumerate(KEYBOARD):
            row_w = len(row) * (key_w + gap)
            x0 = (width - row_w) / 2

            for col_i, ch in enumerate(row):
                x1 = x0 + col_i * (key_w + gap)
                y1 = y0 + row_i * (key_h + gap)
                x2 = x1 + key_w
                y2 = y1 + key_h

                rect = self.round_rect(
                    x1, y1, x2, y2, r=18, fill="#e8e8e8", outline="#333", width=3
                )

                text = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text="",
                    font=("Arial", int(key_h * 0.4), "bold"),
                )

                self.key_boxes[ch] = (rect, text)

        # SPACE BAR
        space_w = key_w * 5.5
        x1 = (width - space_w) / 2
        x2 = x1 + space_w
        y1 = y0 + 3 * (key_h + gap)
        y2 = y1 + key_h

        rect = self.round_rect(
            x1, y1, x2, y2, r=18, fill="#e8e8e8", outline="#333", width=3
        )
        text = self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="",
            font=("Arial", int(key_h * 0.4), "bold"),
        )
        self.key_boxes[" "] = (rect, text)

    # ----------------------------------------------------------
    # SET NEXT TARGET
    # ----------------------------------------------------------
    def set_target(self):
        if self.pos >= len(self.letters):
            self.finish_sentence()
            return

        self.target = self.letters[self.pos]
        rect, txt = self.key_boxes[self.target]

        shown = "⎵" if self.target == " " else self.target

        self.canvas.itemconfig(rect, fill="yellow")
        self.canvas.itemconfig(txt, text=shown)

    # ----------------------------------------------------------
    # FINISH SENTENCE
    # ----------------------------------------------------------
    def finish_sentence(self):
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        elapsed = int(time.time() - self.start_time) if self.timer_started else 0

        self.canvas.itemconfig(
            self.result_display, text=f"დრო: {elapsed}   ქულები: {self.score}"
        )

        self.root.after(1200, self.load_next_sentence)

    def load_next_sentence(self):
        self.sentence_idx += 1

        if self.sentence_idx >= len(self.sentences):
            self.canvas.itemconfig(
                self.result_display, text="ყველა წინადადება დასრულდა!"
            )
            return

        # RESET EVERYTHING
        self.current_sentence = self.sentences[self.sentence_idx]
        self.letters = list(self.current_sentence)
        self.pos = 0
        self.running = True
        self.timer_started = False
        self.canvas.itemconfig(self.timer_display, text="0")

        # clear old letters
        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids = []

        self.canvas.itemconfig(self.result_display, text="")

        self.draw_sentence()
        self.set_target()

    # ----------------------------------------------------------
    # SAFE RESET FUNCTION — FIXES THE BUG
    # ----------------------------------------------------------
    def safe_reset(self, rect_id, txt_id, expected_color):
        current = self.canvas.itemcget(rect_id, "fill")

        # reset only if still red
        if current == "red":
            self.canvas.itemconfig(rect_id, fill=expected_color)
            self.canvas.itemconfig(txt_id, text="")

    # ----------------------------------------------------------
    # KEY HANDLER
    # ----------------------------------------------------------
    def on_key(self, event):
        if not self.running:
            return

        ch = event.char.upper() if event.char else ""
        if event.keysym == "space":
            ch = " "

        if ch not in self.key_boxes:
            return

        # START TIMER ON FIRST CORRECT
        if not self.timer_started and ch == self.letters[0]:
            self.timer_started = True
            self.start_time = time.time()
            self.start_timer()

        # WRONG KEY
        if ch != self.target:
            self.score -= 3
            self.update_score()

            rect, txt = self.key_boxes[ch]
            old_color = self.canvas.itemcget(rect, "fill")

            self.canvas.itemconfig(rect, fill="red")
            self.canvas.itemconfig(txt, text=ch if ch != " " else "⎵")

            # SAFE RESET → no more disappearing keyboard
            self.root.after(
                200, lambda r=rect, t=txt, oc=old_color: self.safe_reset(r, t, oc)
            )
            return

        # CORRECT KEY
        self.score += 1
        self.update_score()

        self.shade(self.pos)

        rect, txt = self.key_boxes[self.target]
        self.canvas.itemconfig(rect, fill="lightgreen")

        self.pos += 1

        self.root.after(
            180,
            lambda r=rect, t=txt: (
                self.canvas.itemconfig(r, fill="#e8e8e8"),
                self.canvas.itemconfig(t, text=""),
                self.set_target(),
            ),
        )


# RUN
root = tk.Tk()
Trainer(root)
root.mainloop()
