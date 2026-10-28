"""Load the approved welcome artwork. Never redraw or replace it programmatically."""
from pathlib import Path

from PIL import Image, ImageTk


def welcome_image(width: int, height: int) -> ImageTk.PhotoImage | None:
    """Fit the approved picture inside the current canvas without distortion.

    The resource is optional until the approved binary is checked into GitHub.
    Source and PyInstaller builds share the same bundled resource path.
    """
    from logic.resources import bundled_path

    path = bundled_path("resources/branding/welcome.png")
    if not path.is_file():
        return None
    with Image.open(path) as source:
        source = source.convert("RGB")
        # Photo's first 48px depict a simulated Windows title bar, which the
        # real Tk window already provides; avoid a second fake title bar.
        if source.width == 1448 and source.height == 1086:
            source = source.crop((0, 48, 1448, 1086))
        image = Image.new("RGB", (max(1, width), max(1, height)), "#d9edff")
        fitted = source.copy()
        fitted.thumbnail(image.size, Image.Resampling.LANCZOS)
        x = (image.width - fitted.width) // 2
        y = (image.height - fitted.height) // 2
        image.paste(fitted, (x, y))
    return ImageTk.PhotoImage(image)
