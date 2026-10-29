"""Generate reproducible KLAVA Windows branding without requiring a GUI renderer.

Run: python scripts/generate_brand_assets.py
Outputs are derived raster icons; editable SVG masters live in resources/branding.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resources" / "branding" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 1024
SCALE = SIZE / 512


def box(draw, coords, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        tuple(round(v * SCALE) for v in coords),
        radius=round(radius * SCALE),
        fill=fill,
        outline=outline,
        width=round(width * SCALE),
    )


def font(size):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, round(size * SCALE))
    raise RuntimeError("No supported bold TrueType font was found")


def render(full=False):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    for x, fill, letter in [(62, "#FFDA1E", "F"), (266, "#9DD3FA", "J")]:
        box(d, (x, 138, x + 184, 338), 34, fill, "#080B10", 14)
        box(d, (x + 16, 152, x + 167, 315), 25, None, "#45474A", 5)
        d.text((round((x + 92) * SCALE), round(236 * SCALE)),
               letter, anchor="mm", font=font(112), fill="#080B10")
    if full:
        colors = ["#FF7975", "#91D69C", "#FFC388", "#B596DF", "#7EC9F6", "#F37DA8"]
        for y in [84, 365]:
            for i, color in enumerate(colors):
                x = 77 + 60 * i
                box(d, (x, y, x + 48, y + 19), 8, color)
        d.arc(tuple(round(z * SCALE) for z in (216, 170, 308, 230)),
              190, 345, fill="#080B10", width=round(9 * SCALE))
        d.line([(round(284*SCALE), round(194*SCALE)),
                (round(304*SCALE), round(208*SCALE)),
                (round(301*SCALE), round(184*SCALE))],
               fill="#080B10", width=round(8*SCALE), joint="curve")
    return image


icon = render()
logo = render(full=True)
for size in (16, 24, 32, 48, 64, 128, 256, 512, 1024):
    icon.resize((size, size), Image.Resampling.LANCZOS).save(OUT / f"app-icon-{size}.png")
for size in (128, 256, 512, 1024):
    logo.resize((size, size), Image.Resampling.LANCZOS).save(OUT / f"logo-full-{size}.png")
icon.save(OUT / "KLAVA.ico", format="ICO", sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
icon.save(OUT / "KLAVA.png")
print(f"KLAVA branding generated in {OUT}")
