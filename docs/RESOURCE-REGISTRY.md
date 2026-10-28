# KLAVA — Resource Registry

**Verified:** 2026-10-27
**Environment:** PR #2 and PR #3 are merged into `main`; review branch `ci/verify-failure-alert` prepares an opt-in automated failure-path test.
**Scope:** registry of canonical owners and verified connected resources; not evidence of full two-way synchronization.

| Title | Canonical path / URL | Mirror | Language | Version | Visibility | Sync state | Last verified |
|---|---|---|---|---|---|---|---|
| KLAVA source and governance | https://github.com/avtotrainer/klava | None | Georgian/English | `main` | Public | canonical-only | 2026-10-27 |
| Constitution (approved and merged) | [CONSTITUTION.md](../CONSTITUTION.md) | None | Georgian | 1.0-rc1 | Public | canonical-only | 2026-10-27 |
| Product requirements | [PROJECT-SPECIFICATION.md](PROJECT-SPECIFICATION.md) | None | Georgian | `main` | Public | canonical-only | 2026-10-27 |
| Development policy | [DEVELOPMENT.md](DEVELOPMENT.md) | None | Georgian | Working branch | Public | canonical-only | 2026-10-27 |
| AI Project Instructions (reference draft) | [CHATGPT-PROJECT-INSTRUCTIONS.md](CHATGPT-PROJECT-INSTRUCTIONS.md) | ChatGPT Project Settings (not accessible for readback) | English | 1.2 | Public (GitHub); Project visibility unknown | unknown | 2026-10-27 |
| Synchronization runbook | [KLAVA-SYNC-RUNBOOK.md](KLAVA-SYNC-RUNBOOK.md) | None | Georgian | 1.0 | Public | canonical-only | 2026-10-27 |
| Teaching resources | https://drive.google.com/drive/folders/1TH7yghuaJYTEw4_qS0p_lYdoLOWLGw4G | None | Georgian | Empty root at verification | Access restricted/unspecified | canonical-only | 2026-10-27 |
| Slack coordination | https://aklava.slack.com | [#new-channel](https://app.slack.com/client/T0CC5794W2X/C0CBW35EM0F) | Georgian | Workspace and channel read verified again; Project Source linking separately fails with MCP error | Workspace/channel readable; other visibility unknown | unknown | 2026-10-27 |
| Windows Portable / Installer handout | [WINDOWS-PORTABLE.md](WINDOWS-PORTABLE.md) | None | Georgian | 1.2 (per-user installer branch) | Public repository | canonical-only | 2026-10-28 |

| KLAVA visual identity | [resources/branding/](../resources/branding/README.md) | None | English | 1.0 (review branch) | Public on merge | canonical-only | 2026-10-28 |

| Windows MSI school installer | [WINDOWS-MSI.md](WINDOWS-MSI.md) | None | Georgian docs / English build metadata | PR #13 draft | Public on merge | canonical-only | 2026-10-29 |
| User KLV exercise library | [logic/exercise_library.py](../logic/exercise_library.py) | User-specific `%LOCALAPPDATA%/KLAVA` (runtime data, not synced) | English code / Georgian UI | PR #12 | Public code / private local exercises | canonical-only | 2026-10-28 |

## Sync modes and boundaries

- **canonical-only:** source exists, with no authorized or required mirror.
- **in-sync:** every named, independently read mirror matches the canonical revision.
- **repo-ahead / docs-ahead:** one known side has newer independent edits.
- **conflict:** both sides have independent overlapping edits; stop automatic overwrite.
- **unknown:** connected source/version/visibility cannot be verified.

### Verified capabilities

1. GitHub: repository read/write on approved working branch; PR checks for pytest/Ruff/syntax.
2. Google Drive: access to KLAVA root verified and currently empty. No fabricated or empty mirror files created.
3. Slack: with the KLAVA-linked account selected, the connector successfully read workspace `T0CC5794W2X` and channel `C0CBW35EM0F` (`#new-channel`). This fixes the earlier wrong-account read failure; **baseline status message was posted to #all-klava on 2026-10-27**. Adding the channel as a ChatGPT Project Source is separately reported to fail with `Error calling MCP tools` and has not been verified successful.
4. ChatGPT: existing daily synchronization-audit task confirmed enabled at **09:00 Asia/Tbilisi** and updated on 2026-10-27 to inspect verified KLAVA Slack `#all-klava` and post only **new material** changes, CI failures or blockers after deduplication. This is a scheduled assistant check, **not** real-time GitHub event delivery or a continuous data pipeline. First scheduled audit on 2026-10-27 confirmed successful read access to GitHub, KLAVA Drive root and the correct KLAVA Slack channel; no scheduled Slack alert was warranted by the baseline comparison. ChatGPT Project Instructions/Knowledge cannot be synced by GitHub commits.
5. GitHub Actions: PR checks and `main` checks pass. Daily `schedule` at **05:00 UTC** is now present on default branch. Incoming Webhook secret is configured by owner; [manual Slack delivery run 40569813642](https://github.com/avtotrainer/klava/actions/runs/40569813642) succeeded and the exact message was read in KLAVA `#all-klava`. Workflow-run notification after an **actual failed validation** remains untested. Actions does not access Google Drive.

### Allowed actions

On an approved task, inspect versions → update canonical artifact → update necessary permitted links/indexes/registry/mirrors → verify readback. Keep changes in a review branch and do not auto-merge into `main`. Do not overwrite independent Drive edits. No unattended Drive write sync is established; scheduled Slack notification rules exist, but delivery of a new-change alert by a scheduled run has not yet been tested.

### Blockers and next actions

- Slack: KLAVA account verified; `#new-channel` and `#all-klava` read successfully. Initial authorized synchronization status message posted to [#all-klava](https://aklava.slack.com/archives/C0CCB8KTNGJ/p1793065796262659) on 2026-10-27. ChatGPT Project Sources attachment remains unresolved. Daily ChatGPT audit includes conditional Slack notifications, but an actual new-change alert from that schedule is not yet verified.
- Service-to-service Drive sync: no existing documents/mirrors in the verified empty KLAVA folder; do not set up broad write credentials before a real sync target is defined. No tokens should be posted in chat.
- GitHub CI failure → Slack: [notification workflow](../.github/workflows/notify-slack.yml) is **active on `main`**; manual delivery was verified in Slack. Actual failed-CI event handling remains unverified. New opt-in `workflow_dispatch` test (review branch only) will deliberately fail a separate check **without changing application code**, after user-approved merge and manual triggering.
- ChatGPT Project Instructions/Knowledge: confirm separately, as readback/edit through GitHub is unavailable.
- PR #2 and PR #3 were merged; their work is on `main`. Do not confuse the controlled failure test PR with automatic permission to merge.
