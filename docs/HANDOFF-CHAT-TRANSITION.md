# KLAVA — Chat transition handoff (2026-10-27)

## Verified source of truth
- Repository: https://github.com/avtotrainer/klava; `main` currently at `d051322f7b3fd1b1456667de2c6017be8364936f`.
- [PR #2](https://github.com/avtotrainer/klava/pull/2) merged project foundation/constitution, tests and validation workflow. [PR #3](https://github.com/avtotrainer/klava/pull/3) merged manual Slack delivery test. [PR #4](https://github.com/avtotrainer/klava/pull/4) merged the isolated failure-verification job.
- Previously used foundation and behavioral-guard branches were deleted after merger. The owner's local `main` was synchronized after PR #2 but should be refreshed again for later merges.
- Local checks: Python compileall passed, pytest 18 passed, Ruff passed, local Markdown links checked for 12 files. Link audit does not check HTTP/Slack/Drive URLs.

## Automation: GitHub to KLAVA Slack
- Slack coordination workspace: https://aklava.slack.com ; notification channel `#all-klava` at https://aklava.slack.com/archives/C0CCB8KTNGJ .
- Another connected Slack account belongs to a different teacher workspace. Choose and read back the KLAVA account before interacting. ChatGPT Project Source attachment of the Slack channel had `channel_not_found`; the direct Slack connector still worked.
- The owner created a minimal Slack App with Incoming Webhooks enabled, directed to `#all-klava`, and stored its webhook URL as a GitHub Actions repository secret. Do not expose or copy the secret value into documentation.
- `.github/workflows/notify-slack.yml`: on failure of `Validate KLAVA`, sends automated Slack alert with a link to the failing run. Manual `workflow_dispatch` verifies delivery. Normal successful validation should skip the notification.
- **Manual delivery proven:** [run 40569813642](https://github.com/avtotrainer/klava/actions/runs/40569813642) succeeded; corresponding `KLAVA | Test alert delivery` observed in `#all-klava`.
- **Automated failure alert proven end-to-end:** user manually selected the optional failure-verification input in the `Validate KLAVA` workflow. [Intentionally failed run 40572292357](https://github.com/avtotrainer/klava/actions/runs/40572292357) produced [successful automatic notification run 40572342910](https://github.com/avtotrainer/klava/actions/runs/40572342910); Slack readback showed `KLAVA | CI failure` linking to the same validation run. That deliberate failed run was **not** an application regression.
- `.github/workflows/validate.yml`: PR, main push, manual and daily scheduled validation. Optional manual input `verify_failure_notification` defaults to `false`; enabling it deliberately fails a separate test job for notification validation without changing application code. No further deliberate red runs are needed.

## Daily audit, Drive and boundaries
- ChatGPT daily KLAVA resource audit is enabled at 09:00 Asia/Tbilisi, task `6adff74f56d88191bd6603cf9ee6b8ec`. First run 2026-10-27 ~09:01 completed. The audit checks GitHub, KLAVA Drive and the correct Slack workspace; reports material changes conditionally with deduplication; no Slack message when nothing changes. This is scheduled checking, not continuous two-way mirroring.
- Teaching resource folder: https://drive.google.com/drive/folders/1TH7yghuaJYTEw4_qS0p_lYdoLOWLGw4G . Verified empty on 2026-10-27. No file mirrors or unattended Drive write synchronization were configured. GitHub owns code/governance/technical procedures, Drive owns pedagogy/worksheets/media, Slack owns alerts/coordination. Preserve independent edits and report conflicts.
- ChatGPT Project Instructions/Knowledge do not update automatically when GitHub changes. Existing resource registry/runbook may contain historical statements from before the PR merges. A follow-up reviewed documentation change should reconcile them.
- Never automatically merge into `main`, delete branches, publish newly public materials, change access or pedagogical policy without required approval. Slack messaging was authorized for this project's verified notification channel only.

## KLAVA product and immediate development task
- Core aim: typing orientation for Georgian-speaking children aged 7–12 using uppercase Latin letters. Existing Tkinter app and `Trainer` session controller must remain functional. Constitution principles: Quality > Quantity, MIN_LINES=2, adaptive steps 100→50→20→4, accuracy ≥97%, CPM ≥180, 3 consecutive successes. These are specified learning rules, **not all implemented**. Do not invent formula/timing or modify thresholds without approval.
- [PR #5](https://github.com/avtotrainer/klava/pull/5) **OPEN, not merged**: branch `fix/behavioral-guard-reset-history`, CI [40571834963](https://github.com/avtotrainer/klava/actions/runs/40571834963) passed. Fix in `logic/engine.py::TypingEngine.reset_error_state()` clears stale `_key_history` so a new attempt does not instantly re-lock. Regression in `tests/test_typing_engine.py`, CHANGELOG entry. Merge requires owner's explicit approval.
- Architectural gap from code inspection: `trainer.py::Trainer.on_key` calls `exercises/typing.py::TypingExercise.on_key`, which processes keys directly. `logic/engine.py::TypingEngine` is not yet integrated into the active exercise, so its behavioral guard cannot currently affect the GUI. Next functional task: inspect `trainer.py`, `exercises/typing.py`, `logic/engine.py`, `ui/keyboard.py`, `ui/canvas.py`; make minimally invasive guarded-engine integration with regression tests and appropriate GUI checks. Preserve correct/incorrect key behavior, uppercase normalization and SPACE; avoid undocumented lock/reset behavior or rearchitecting `Trainer`.
- Source `docs/PROJECT-SPECIFICATION.md` lists unimplemented accuracy/CPM/success/adaptation/progress items. Separate verified behavior from target requirements.

## Previous lessons
- Git pager: `git --no-pager log -5 --oneline`, `git --no-pager branch -vv`; Git branch safety check and `git pull --ff-only` worked for local fast-forward. Avoid copying shell prompt glyphs as commands.
- An unrelated schoolbell script was mistakenly invoked in the KLAVA directory: it is not a KLAVA file.
- Direct GitHub connector cannot always dispatch Actions or delete remote branches; browser/local Git actions were needed. Read back all reported changes and avoid pretending an operation succeeded.
- Keep future discussions focused on **actual program behavior**. The owner explicitly asked to stop extending reorganization and start KLAVA feature/bug-fix development.

## Resume instruction
Read this handoff, PR #5, current `main`, CI and `docs/RESOURCE-REGISTRY.md` before proceeding. Complete real scoped engineering work and keep PRs reviewable. This document is the durable handoff for a chat the owner intends to delete.
