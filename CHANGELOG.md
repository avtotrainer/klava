## [Unreleased]

### Fixed
- Reject exercise lines with characters the on-screen keyboard cannot teach (punctuation, digits, TAB, non-Latin letters) before kiosk mode starts; the error names the line and character. Previously such a line could never be completed and trapped the learner in fullscreen mode.
- Fit long exercise lines to the window by shrinking letter spacing and font together; the shipped 39-character lines no longer run off 1280–1600 px wide screens. The sentence re-flows when the window size changes.
- Redraw the on-screen keyboard when the window size changes, so windowed mode (`fullscreen = false`) keeps every key visible.
- Accept key presses on Windows while a Georgian (or other non-Latin) keyboard layout is active, using the physical letter-key position.
- Hide the SPACE key label together with the rest of the keyboard.
- Release the single-instance lock explicitly on Windows so an immediate relaunch works.

### Changed
- A second launch now says that KLAVA is already running instead of exiting silently.
- Unexpected startup and runtime errors are shown in a dialog and logged to `%LOCALAPPDATA%\KLAVA\error.log` (the windowed EXE has no console).
- The exercise editor shortcut starts Notepad by its full System32 path.

### Internal
- `TypingEngine`: optional `lock_duration` auto-release (default unchanged), bounded key history, monotonic clock.
- Shared exercise character rules for the trainer and `scripts/package_windows.py`; colour format validation for the keyboard model.
- Atomic save of the selected exercise; welcome artwork decoded once and rescaled after resizing settles.
- `requirements.txt` / `requirements-dev.txt`, Dependabot for pip and GitHub Actions, actions pinned to commit SHAs (except the release workflow), Ruff `B`, `ARG`, `S`, `BLE` rules.

## [0.3.2-beta.1] — 2026-10-30

### Fixed
- Prevent duplicate trainer windows with an OS-backed per-user lifetime lock; release automatically after exit or crash, while retaining the exercise-editor shortcut (PR #19).

### Changed
- EXE/application version 0.3.2-beta.1; MSI ProductVersion 0.3.2.
- Release publication requires an explicit version-specific commit marker or manual publish input; existing release tags are never overwritten.

## [0.3.1-beta.1] — 2026-10-29

### UI
- Replace initial welcome text with instructional QWERTY home-row hand-placement illustration; open window at 800×600 while retaining training fullscreen mode.

### Added
- Per-user `.klv` exercise library with persistent selection and lossless legacy `.txt` migration.
- Windows installer choice between current-user and all-users installation modes; portable two-file `.klv` payload.
- Editable KLAVA F/J brand SVGs, reproducible PNG/ICO generator, and integration with Windows executable/installer build.
- Current-user installer without administrator elevation, with Start-menu launch/editor shortcuts, optional desktop shortcut and uninstaller.
- Per-user installed exercises, preserved across reinstall/uninstall, with installer lifecycle CI checks.
- Windows x64 portable onefile build, exact two-file ZIP validation, and PR/manual Actions artifacts.
- Portable path, UTF-8 input, session reload, packaging and opt-in real Tk regression tests.
- Authorized daily 09:00 Asia/Tbilisi cross-resource audit through a scheduled ChatGPT task (first execution not yet verified).
- Read-only local Markdown link audit, regression tests, and scheduled GitHub Actions configuration (default-branch activation pending).
- Georgian technical handout for synchronization, external-access limitations, safety, and rollback.
- Draft project constitution and rules migration matrix for owner review.
- Focused behavioral regression tests and GitHub Actions validation in the project foundation branch.
- Project knowledge, resource registry, and draft operational ChatGPT instructions.

### Fixed
- Interpret escaped `\\n` in localized messages, scale full-screen cover text with the actual window, and display the KLAVA icon in the title bar/About dialog.\n\n### Changed
- Windows distribution is installer-only; portable ZIP packaging/upload removed from CI (existing installer scope choices retained).
- Frozen builds read editable `exercises.txt` beside the executable; source runs preserve configured exercises.
- Resource paths no longer depend on the current working directory; invalid exercise encoding gets a localized UTF-8 error.
- Documentation aligned with implemented code and documented learning requirements.

### Internal
- Governance proposal remains unratified; existing Project Instructions continue to apply until separately replaced.

---

## [0.3.1-alpha] — 2025-12-29

### Added
- Centralized configuration via `config.ini` (UI, training rules, keyboard parameters)
- Keyboard visual parameters (colors, radius) moved out of hardcoded values
- Dedicated SPACE key rendered as an independent UI element
- Foundation for resource-based strings and localization support
- Window title support (prepared for resource-based text)

### Changed
- Keyboard is now fully responsible for key visual states (idle / target / correct / wrong)
- TypingExercise delegates all visual state decisions to Keyboard
- Removal of special-case handling for SPACE in exercise logic
- UI behavior aligned strictly with separation of concerns (UI ≠ Logic)

### Fixed
- Restored correct SPACE key rendering and activation as a typing target
- Fixed SPACE highlight not activating despite being rendered
- Resolved keyboard color regression where non-active keys appeared uniform
- Fixed `configparser.DuplicateSectionError` caused by duplicated config sections

### Internal
- Refactored keyboard rendering pipeline for extensibility
- Normalized key registration through a single `key_boxes` source of truth
- Prepared internal structure for future engine and QualityGate integration

### Known Limitations
- TypingEngine metrics (accuracy, CPM) are not yet enforced
- QualityGate rules are defined but inactive
- UI strings are still partially hardcoded (resource migration pending)

---

## [0.3.0-alpha] — 2025-12-28

### Added
- Visual finger legend concept introduced (static prototype)
- Initial per-key highlight color logic groundwork

### Changed
- Keyboard layout adjusted for improved visual grouping
- Legend placement moved closer to keyboard area

### Fixed
- Corrected key highlight persistence after task completion

### Internal
- First separation of keyboard drawing logic from Trainer
- Cleanup of experimental UI code paths

---

## [0.2.0-alpha] — 2025-12-26

### Added
- Modular project structure (`logic/`, `ui/`, `exercises/`)
- On-screen keyboard component
- Sentence-based typing exercise

### Changed
- Trainer introduced as UI/Logic connector
- Application flow reorganized around exercise lifecycle

### Fixed
- Multiple AttributeError issues caused by early class coupling
- Import path inconsistencies during refactor

### Internal
- Removal of duplicated logic between UI and Trainer
- Initial enforcement of separation of concerns

---

## [0.1.1-alpha] — 2025-12-24

### Fixed
- Prevented premature program exit during active exercise
- Corrected key normalization for SPACE handling

### Internal
- Minor cleanup after first functional prototype
- Stabilized event handling order

---

## [0.1.0-alpha] — 2025-12-23

### Added
- Initial working typing trainer prototype
- Fullscreen Tkinter window with keyboard input handling
- Basic sentence rendering on screen

### Known Limitations
- No separation between UI and logic
- Hardcoded values and layout
- No progress validation

---

## Notes
- Versions prior to 1.0.0 are considered **unstable by definition**
- Architectural stability is prioritized over feature velocity
- Educational correctness overrides visual experimentation

