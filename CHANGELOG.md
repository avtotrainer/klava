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

