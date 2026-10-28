# KLAVA — Resource Registry

**Verified:** 2026-10-28
**Environment:** PR #2, #3, #4 and #6 are merged into `main`; PR #5, #7 and #8 remain open. `main` at audit: `95aa336da47fe4f7cf7de07c96661fb459901539`.
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

## Latest cross-resource audit — 2026-10-28 (Asia/Tbilisi)

- **GitHub:** `main` remains at `95aa336`; [PR #6](https://github.com/avtotrainer/klava/pull/6) merged with the [handoff](HANDOFF-CHAT-TRANSITION.md). [PR #5](https://github.com/avtotrainer/klava/pull/5) remains open (behavioral guard). [PR #7](https://github.com/avtotrainer/klava/pull/7) adds Windows Portable two-file ZIP; its [Windows Portable run 40576170722](https://github.com/avtotrainer/klava/actions/runs/40576170722) passed. [PR #8](https://github.com/avtotrainer/klava/pull/8) adds a per-user Windows installer; latest [Windows Portable run 40630222556](https://github.com/avtotrainer/klava/actions/runs/40630222556) **failed** specifically at `Verify install and uninstall as a real standard user`. Earlier steps including portable ZIP, real Tk widget test, installer build and elevated-context installer lifecycle checks passed. Root cause of standard-user failure is **not yet verified**; previous attempts [40629884019](https://github.com/avtotrainer/klava/actions/runs/40629884019) and [40629647008](https://github.com/avtotrainer/klava/actions/runs/40629647008) also failed at that step. Latest `Validate KLAVA` for PR #8 [40630222548](https://github.com/avtotrainer/klava/actions/runs/40630222548) passed. The notification workflow skips normal successful `Validate KLAVA` runs and does not cover the separate Windows Portable failure in PR #8.
- **Drive:** [KLAVA teaching resource folder](https://drive.google.com/drive/folders/1TH7yghuaJYTEw4_qS0p_lYdoLOWLGw4G) was readable and had zero direct children. No document-level mirror comparison is possible. No unattended Drive write sync is configured.
- **Slack:** correct KLAVA workspace `T0CC5794W2X`, `#all-klava` `C0CCB8KTNGJ` read. Last message was the previously verified intentional `Validate KLAVA` failure alert from 2026-10-27 23:48 +04. At the time of this audit no message about PR #7/#8 or Windows Portable failures was present. Teacher Collaboration Lab connection was not used.
- **Reference verification:** registry local links are known GitHub paths; external destination availability and ChatGPT Project Source attachment remain outside automated local-link tests. No independent Drive edits or cross-platform conflicts observed. All GitHub-only entries remain `canonical-only`; Project Instructions/Slack Project Source remain `unknown`.

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
5. GitHub Actions: PR checks and `main` checks pass. Daily `schedule` at **05:00 UTC** is now present on default branch. Incoming Webhook secret is configured by owner; [manual Slack delivery run 40569813642](https://github.com/avtotrainer/klava/actions/runs/40569813642) succeeded and the exact message was read in KLAVA `#all-klava`. Automated `workflow_run` notification was **verified end-to-end** after intentionally failed validation [40572292357](https://github.com/avtotrainer/klava/actions/runs/40572292357): notification [40572342910](https://github.com/avtotrainer/klava/actions/runs/40572342910) succeeded and the exact failure message was read in `#all-klava`. Actions does not access Google Drive.

### Allowed actions

On an approved task, inspect versions → update canonical artifact → update necessary permitted links/indexes/registry/mirrors → verify readback. Keep changes in a review branch and do not auto-merge into `main`. Do not overwrite independent Drive edits. No unattended Drive write sync is established; scheduled Slack notification rules exist, but delivery of a new-change alert by a scheduled run has not yet been tested.

### Blockers and next actions

- Slack: KLAVA account verified; `#new-channel` and `#all-klava` read successfully. Initial authorized synchronization status message posted to [#all-klava](https://aklava.slack.com/archives/C0CCB8KTNGJ/p1793065796262659) on 2026-10-27. ChatGPT Project Sources attachment remains unresolved. Daily ChatGPT audit includes conditional Slack notifications, but an actual new-change alert from that schedule is not yet verified.
- Service-to-service Drive sync: no existing documents/mirrors in the verified empty KLAVA folder; do not set up broad write credentials before a real sync target is defined. No tokens should be posted in chat.
- GitHub CI failure → Slack: [notification workflow](../.github/workflows/notify-slack.yml) is **active on `main`**; manual delivery was verified in Slack. The opt-in `workflow_dispatch` failure-path test was merged in PR #4 and successfully exercised. Its intentional failure is not a product defect; no repeat is required.
- ChatGPT Project Instructions/Knowledge: confirm separately, as readback/edit through GitHub is unavailable.
- PR #2, #3, #4 and #6 were merged; their work is on `main`. PR #5, #7 and #8 are open; never merge without explicit owner approval.
