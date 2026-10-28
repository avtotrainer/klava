# KLAVA welcome screen image

**Approved visual reference:** generated in KLAVA conversation, 2026-10-29. The exact binary is supplied in the conversation as a downloadable PNG, but it has **not been committed** to this branch.

Required asset path: `resources/branding/welcome.png`. UI uses Pillow to crop the embedded mock window title strip and scale/letterbox to the current 800×600 window without stretching. `KLAVA.spec` already includes all `resources/` recursively, so both MSI and EXE will bundle the image once committed.

Do not replace this picture with the previous programmatic `ui.hand_placement` illustration. If the PNG is absent, the app displays a minimal `KLAVA` fallback instead of a fabricated image. Do not consider this task visually complete until the exact PNG is in GitHub and a new CI installer is built and checked.
