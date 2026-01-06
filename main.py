# main.py
# KLAVA — Entry point

import tkinter as tk

from trainer import Trainer

__version__ = "0.4.0-alfa"

if __name__ == "__main__":
    root = tk.Tk()
    Trainer(root)
    root.mainloop()
