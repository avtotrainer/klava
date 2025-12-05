import tkinter as tk
import time

SENTENCE_FILE = "sentences.txt"

KEYBOARD = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]

PALE = "#cccccc"
DARK = "#000000"


class Trainer:
    def __init__(self, root):
        self.root = root

        # ---------------------------
        #   FULLSCREEN / KIOSK MODE
        # ---------------------------
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.config(cursor="none")  # hide mouse until exercise ends
        root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.block_system_keys()

        # Canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()

        # ---------------------------
        #   SENTENCES
        # ---------------------------
        self.sentences = self.load_sentences()
        self.sentence_idx = 0

        self.current_sentence = self.sentences[self.sentence_idx]
        self.letters = list(self.current_sentence)

        # ---------------------------
        #   GAME STATE
        # ---------------------------
        self.pos = 0
        self.score = 0
        self.running = True

        self.timer_started = False
        self.start_time = None
        self.timer_id = None

        # UI objects
        self.text_ids = []
        self.key_boxes = {}
        self.target = None

        self.timer_display = None
        self.score_display = None
        self.result_display = None

        self.allow_exit = False

        # Draw UI
        self.draw_sentence()
        self.draw_keyboard_all_letters()
        self.draw_score_timer()
        self.draw_exit()

        self.set_target()

        # Key handler
        root.bind("<Key>", self.on_key)

        # Teacher secret exit
        root.bind("<Control-Shift-X>", self.force_exit)

    # ==========================================================
    #   SYSTEM KEY BLOCKS
    # ==========================================================
    def block_system_keys(self):
        def block(event):
            return "break"

        keys = [
            "<Alt-F4>",
            "<Alt-Tab>",
            "<Escape>",
            "<Control-q>",
            "<Control-w>",
            "<Super_L>",
            "<Super_R>",
            "<F11>",
        ]
        for k in keys:
            self.root.bind(k, block)

    # ==========================================================
    #   LOAD SENTENCES
    # ==========================================================
    def load_sentences(self):
        try:
            with open(SENTENCE_FILE, "r", encoding="utf-8") as f:
                lines = [ln.strip().upper() for ln in f if ln.strip()]
                return lines if lines else ["HELLO WORLD"]
        except:
            return ["HELLO WORLD"]

    # ==========================================================
    #   DRAW SENTENCE (PALE LETTERS)
    # ==========================================================
    def draw_sentence(self):
        y = 130
        spacing = min(70, max(40, self.width * 0.75 / len(self.letters)))
        total = spacing * len(self.letters)
        start_x = self.width / 2 - total / 2

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

    def shade(self, idx):
        self.canvas.itemconfig(self.text_ids[idx], fill=DARK)

    # ==========================================================
    #   KEYBOARD DRAWING WITH ALL PALE LETTERS
    # ==========================================================
    def round_rect(self, x1, y1, x2, y2, r=15, **kw):
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

    def draw_keyboard_all_letters(self):
        key_w = self.width / 12
        key_h = self.height / 8
        gap = key_w * 0.12
        y0 = self.height / 3

        for row_i, row in enumerate(KEYBOARD):
            row_w = len(row) * (key_w + gap)
            x0 = self.width / 2 - row_w / 2

            for col_i, ch in enumerate(row):
                x1 = x0 + col_i * (key_w + gap)
                y1 = y0 + row_i * (key_h + gap)
                x2 = x1 + key_w
                y2 = y1 + key_h

                rect = self.round_rect(
                    x1, y1, x2, y2, fill="#eeeeee", outline="#444", width=2
                )
                txt = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=ch,
                    font=("Arial", int(key_h * 0.35), "bold"),
                    fill=PALE,
                )
                self.key_boxes[ch] = (rect, txt)

        # SPACE BAR
        space_w = key_w * 6
        x1 = self.width / 2 - space_w / 2
        x2 = x1 + space_w
        y1 = y0 + 3 * (key_h + gap)
        y2 = y1 + key_h

        rect = self.round_rect(x1, y1, x2, y2, fill="#eeeeee", outline="#444", width=2)
        txt = self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="SPACE",
            font=("Arial", int(key_h * 0.3), "bold"),
            fill=PALE,
        )
        self.key_boxes[" "] = (rect, txt)

    # ==========================================================
    #   SCORE + TIMER
    # ==========================================================
    def draw_score_timer(self):
        self.timer_display = self.canvas.create_text(
            120, self.height - 130, text="0", font=("Arial", 40, "bold"), fill="blue"
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

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=str(self.score))

    def start_timer(self):
        if not self.timer_started or not self.running:
            return
        elapsed = int(time.time() - self.start_time)
        self.canvas.itemconfig(self.timer_display, text=str(elapsed))
        self.timer_id = self.root.after(1000, self.start_timer)

    # ==========================================================
    #   EXIT BUTTON
    # ==========================================================
    def draw_exit(self):
        self.exit_button = tk.Button(
            self.root,
            text="EXIT",
            font=("Arial", 22, "bold"),
            bg="red",
            fg="white",
            command=self.safe_exit,
        )
        self.exit_button.place_forget()

    def safe_exit(self):
        if self.allow_exit:
            self.root.config(cursor="arrow")
            self.root.destroy()

    def force_exit(self, event):
        self.root.config(cursor="arrow")
        self.root.destroy()

    # ==========================================================
    #   TARGET LETTER
    # ==========================================================
    def set_target(self):
        if self.pos >= len(self.letters):
            self.finish_sentence()
            return

        self.target = self.letters[self.pos]
        rect, txt = self.key_boxes[self.target]

        shown = self.target if self.target != " " else "SPACE"

        self.canvas.itemconfig(rect, fill="yellow")
        self.canvas.itemconfig(txt, fill=DARK, text=shown)

    # ==========================================================
    #   SENTENCE FINISHED
    # ==========================================================
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
            self.allow_exit = True

            self.root.config(cursor="arrow")

            self.exit_button.place(x=self.width - 150, y=20, width=120, height=50)
            self.canvas.itemconfig(self.result_display, text="დავალება დასრულდა!")
            return

        # load new sentence
        self.current_sentence = self.sentences[self.sentence_idx]
        self.letters = list(self.current_sentence)

        self.pos = 0
        self.running = True
        self.timer_started = False

        self.canvas.itemconfig(self.timer_display, text="0")
        self.canvas.itemconfig(self.result_display, text="")

        for tid in self.text_ids:
            self.canvas.delete(tid)
        self.text_ids = []

        self.draw_sentence()
        self.set_target()

    # ==========================================================
    #   KEY HANDLER – WORKS EVEN ON GEORGIAN LAYOUT
    # ==========================================================
    def on_key(self, event):
        if not self.running:
            return

        ch = event.keysym.upper()  # language independent

        # space fix
        if ch == "SPACE":
            ch = " "

        if ch not in self.key_boxes:
            return

        # TIMER START
        if not self.timer_started and ch == self.letters[0]:
            self.timer_started = True
            self.start_time = time.time()
            self.start_timer()

        # WRONG
        if ch != self.target:
            self.score -= 3
            self.update_score()

            rect, txt = self.key_boxes[ch]
            self.canvas.itemconfig(rect, fill="red")
            self.canvas.itemconfig(txt, fill=DARK)

            self.root.after(
                250,
                lambda r=rect, t=txt: (
                    self.canvas.itemconfig(r, fill="#eeeeee"),
                    self.canvas.itemconfig(t, fill=PALE),
                ),
            )
            return

        # CORRECT
        self.score += 1
        self.update_score()
        self.shade(self.pos)

        rect, txt = self.key_boxes[self.target]
        self.canvas.itemconfig(rect, fill="lightgreen")
        self.canvas.itemconfig(txt, fill=DARK)

        self.pos += 1

        self.root.after(
            180,
            lambda r=rect, t=txt: (
                self.canvas.itemconfig(r, fill="#eeeeee"),
                self.canvas.itemconfig(t, fill=PALE),
                self.set_target(),
            ),
        )


# ==========================================================
#   RUN
# ==========================================================
if __name__ == "__main__":
    root = tk.Tk()
    Trainer(root)
    root.mainloop()
