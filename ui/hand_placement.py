"""Load the approved welcome artwork. Never redraw or replace it programmatically."""
from functools import lru_cache

from PIL import Image, ImageTk


@lru_cache(maxsize=1)
def _approved_source() -> Image.Image | None:
    """Decode the bundled picture once; resizes reuse it instead of reopening the PNG."""
    from logic.resources import bundled_path

    path = bundled_path("resources/branding/welcome.png")
    if not path.is_file():
        return None
    with Image.open(path) as source:
        source = source.convert("RGBA")
    # Photo's first 48px depict a simulated Windows title bar, which the
    # real Tk window already provides; avoid a second fake title bar.
    if source.width == 1448 and source.height == 1086:
        source = source.crop((0, 48, 1448, 1086))
    return source


def welcome_image(width: int, height: int) -> ImageTk.PhotoImage | None:
    """Fit the approved picture inside the current canvas without distortion.

    The resource is optional until the approved binary is checked into GitHub.
    Source and PyInstaller builds share the same bundled resource path.
    """
    source = _approved_source()
    if source is None:
        return None
    image = Image.new("RGB", (max(1, width), max(1, height)), "#d9edff")
    fitted = source.copy()
    fitted.thumbnail(image.size, Image.Resampling.LANCZOS)
    x = (image.width - fitted.width) // 2
    y = (image.height - fitted.height) // 2
    image.paste(fitted, (x, y), fitted.getchannel("A"))
    return ImageTk.PhotoImage(image)
