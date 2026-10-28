# KLAVA welcome image

The owner uploaded the approved artwork to `resources/branding/welcome.png` on the review branch. The uploaded file is a 1024×1024 RGBA PNG (alpha/transparency).

The startup UI composites it over the light-blue backdrop, preserving transparent edges and aspect ratio in the 800×600 initial window. No generated keyboard illustration is used. The image is included automatically by `KLAVA.spec`, which bundles `resources/` for both EXE and MSI packaging.

Manual visual acceptance of the newly packaged startup window remains to be confirmed on Windows. Do not treat the PNG itself as a working Start control; the real Start menu remains the application's navigation mechanism.
