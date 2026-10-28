"""Create an instructional welcome illustration: standard QWERTY home-row fingers.

The fingertip markers are teaching aids, not a keyboard event/input handler.
"""
from PIL import Image, ImageDraw, ImageFont, ImageTk


def _font(size: int, bold: bool = False):
    path = ("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def welcome_image(width: int, height: int) -> ImageTk.PhotoImage:
    """Rasterize an 800x540 reference image scaled to the available canvas."""
    w, h = 800, 540
    image = Image.new("RGB", (w, h), "#eef6ff")
    draw = ImageDraw.Draw(image)
    for i in range(0, h, 4):
        t = i / h
        draw.rectangle((0, i, w, i + 4), fill=(round(235 - 15*t), round(246 - 12*t), 255))
    draw.rounded_rectangle((65, 45, 735, 485), radius=34, fill="#ffffff", outline="#c7dff6", width=3)
    draw.text((400, 77), "KLAVA", font=_font(42, True), fill="#1b4e86", anchor="mm")
    draw.text((400, 117), "HOME ROW  •  A S D F       J K L ;", font=_font(19, True),
              fill="#35658e", anchor="mm")
    # Keys are drawn in standard QWERTY order. The eight home-row positions
    # are emphasized using the standard left-to-right finger mapping.
    rows = [
        ("QWERTYUIOP", 104, 196),
        ("ASDFGHJKL;", 121, 251),
        ("ZXCVBNM,./", 150, 306),
    ]
    finger_colors = ["#db6c75", "#e59e48", "#f2cd5f", "#65ae91",
                     "#65ae91", "#f2cd5f", "#e59e48", "#db6c75"]
    home = {"A": 0, "S": 1, "D": 2, "F": 3, "J": 4, "K": 5, "L": 6, ";": 7}
    key_centers = {}
    for letters, x0, y0 in rows:
        for index, letter in enumerate(letters):
            x = x0 + index * 55
            y = y0
            active = y0 == 251 and letter in home
            fill = finger_colors[home[letter]] if active else "#293b56"
            draw.rounded_rectangle((x, y, x + 48, y + 46), radius=8,
                                   fill=fill, outline="#1e2f48", width=2)
            draw.text((x + 24, y + 23), letter, fill="#ffffff" if not active else "#142b41",
                      font=_font(22, True), anchor="mm")
            if active:
                key_centers[letter] = (x + 24, y + 23)
    draw.rounded_rectangle((280, 362, 520, 391), radius=10,
                           fill="#293b56", outline="#1e2f48", width=2)
    # Each fingertip is placed on its assigned home key, not hovering above
    # neighboring keys. Wrist and palm curves remain below the key rows.
    for group, wrist_x in (("ASDF", 238), ("JKL;", 565)):
        centers = [key_centers[ch] for ch in group]
        for idx, (cx, cy) in enumerate(centers):
            finger_y = 423 + (idx % 2) * 7
            draw.line((cx, cy + 18, cx + (wrist_x - cx) * .19, 334,
                       cx + (wrist_x - cx) * .38, finger_y),
                      fill="#d89f7d", width=17, joint="curve")
            draw.ellipse((cx - 9, cy + 11, cx + 9, cy + 30),
                         fill="#f2c4a7", outline="#bf896f", width=2)
        draw.ellipse((wrist_x - 48, 397, wrist_x + 55, 457),
                     fill="#e8b291", outline="#c58b72", width=2)
    draw.text((400, 472), "LEFT HAND: A S D F     |     RIGHT HAND: J K L ;",
              fill="#234f80", font=_font(14, True), anchor="mm")
    resized = image.resize((max(1, width), max(1, height)), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized)
