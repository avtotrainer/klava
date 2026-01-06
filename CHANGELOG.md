## [0.3.1-alpha] — 2025-12-29

### Added
- Finger-based color coding for all letter keys (left/right hand separation)
- SVG-style finger legend with subtle nail indicator for educational clarity
- Visual alignment of finger legend with corresponding keyboard key groups

### Fixed
- Restored correct SPACE key behavior and visual highlighting
- Fixed key color reset regression after incorrect input
- Removed invalid Tkinter drawing parameters causing runtime crashes
- Resolved type inconsistencies in keyboard state and highlight handling

### Internal
- Refactored keyboard rendering pipeline
- Isolated legend drawing logic from core keyboard layout code
- Improved internal state consistency for key highlight lifecycle

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
