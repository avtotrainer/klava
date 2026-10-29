# KLAVA brand assets

Source vectors: `icon-simplified.svg` for application/installer and `logo-full.svg` for documentation/marketing. These files are reconstructions of the selected reference design, not exact vectorizations of the supplied raster sample.

Generated files (not committed): `resources/branding/generated/KLAVA.ico`, `KLAVA.png`, `logo-full.png`, and size-specific PNGs. Generate them with `python scripts/generate_brand_assets.py` after installing `Pillow` and `CairoSVG`. The Windows CI generates them before PyInstaller and Inno Setup. Do not include assets as additional files in the portable two-file ZIP.

Windows: `KLAVA.ico` is compiled into the EXE by PyInstaller; Inno Setup inherits that icon and uses it for shortcuts. `resources/branding/generated/` is build output, not runtime user data. The SVGs remain the editable masters.
