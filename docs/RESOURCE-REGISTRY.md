# KLAVA — Resource Registry

**Verified:** 2026-10-27
**Environment:** GitHub working branch `chore/project-foundation`; PR #2 remains Draft, `main` unchanged.
**Scope:** registry of canonical owners and verified connected resources; not evidence of full two-way synchronization.

| Title | Canonical path / URL | Mirror | Language | Version | Visibility | Sync state | Last verified |
|---|---|---|---|---|---|---|---|
| KLAVA source and governance | https://github.com/avtotrainer/klava | None | Georgian/English | `chore/project-foundation` | Public | canonical-only | 2026-10-27 |
| Constitution (approved for adoption, not merged) | [CONSTITUTION.md](../CONSTITUTION.md) | None | Georgian | 1.0-rc1 | Public | canonical-only | 2026-10-27 |
| Product requirements | [PROJECT-SPECIFICATION.md](PROJECT-SPECIFICATION.md) | None | Georgian | Working branch | Public | canonical-only | 2026-10-27 |
| Development policy | [DEVELOPMENT.md](DEVELOPMENT.md) | None | Georgian | Working branch | Public | canonical-only | 2026-10-27 |
| AI Project Instructions (reference draft) | [CHATGPT-PROJECT-INSTRUCTIONS.md](CHATGPT-PROJECT-INSTRUCTIONS.md) | ChatGPT Project Settings (not accessible for readback) | English | 1.2 | Public (GitHub); Project visibility unknown | unknown | 2026-10-27 |
| Synchronization runbook | [KLAVA-SYNC-RUNBOOK.md](KLAVA-SYNC-RUNBOOK.md) | None | Georgian | 1.0 | Public | canonical-only | 2026-10-27 |
| Teaching resources | https://drive.google.com/drive/folders/1TH7yghuaJYTEw4_qS0p_lYdoLOWLGw4G | None | Georgian | Empty root at verification | Access restricted/unspecified | canonical-only | 2026-10-27 |
| Slack coordination | https://aklava.slack.com | [#new-channel](https://app.slack.com/client/T0CC5794W2X/C0CBW35EM0F) | Georgian | Workspace and channel read verified again; Project Source linking separately fails with MCP error | Workspace/channel readable; other visibility unknown | unknown | 2026-10-27 |

## Sync modes and boundaries

- **canonical-only:** source exists, with no authorized or required mirror.
- **in-sync:** every named, independently read mirror matches the canonical revision.
- **repo-ahead / docs-ahead:** one known side has newer independent edits.
- **conflict:** both sides have independent overlapping edits; stop automatic overwrite.
- **unknown:** connected source/version/visibility cannot be verified.

### Verified capabilities

1. GitHub: repository read/write on approved working branch; PR checks for pytest/Ruff/syntax.
2. Google Drive: access to KLAVA root verified and currently empty. No fabricated or empty mirror files created.
3. Slack: with the KLAVA-linked account selected, the connector successfully read workspace `T0CC5794W2X` and channel `C0CBW35EM0F` (`#new-channel`). This fixes the earlier wrong-account read failure; **no Slack messages have been sent**. Adding the channel as a ChatGPT Project Source is separately reported to fail with `Error calling MCP tools` and has not been verified successful.
4. ChatGPT: daily synchronization-audit task enabled at **09:00 Asia/Tbilisi**. It is a separate scheduled assistant check, **not** a continuous data pipeline. ChatGPT Project Instructions/Knowledge cannot be synced by GitHub commits.
5. GitHub Actions: PR checks execute on the working branch; daily `schedule` at **05:00 UTC** runs **only after the workflow is on the default branch**, requiring approval to merge PR #2. Checks cannot directly read Google Drive/Slack without separate credentials.

### Allowed actions

On an approved task, inspect versions → update canonical artifact → update necessary permitted links/indexes/registry/mirrors → verify readback. Keep changes in a review branch and do not auto-merge into `main`. Do not overwrite independent Drive edits. No unattended write sync to Drive or Slack is established.

### Blockers and next actions

- Slack: workspace `T0CC5794W2X` and `#new-channel` are accessible through the KLAVA-linked account; `#all-klava` (`C0CCB8KTNGJ`) also appears in the same workspace. Project Sources linking is separately unresolved. Before notification automation, confirm the notification destination and authorized posting scope.
- Service-to-service Drive sync: choose restricted Google authorization and real source/destination requirements before activating; no tokens should be posted in chat.
- ChatGPT Project Instructions/Knowledge: confirm separately, as readback/edit through GitHub is unavailable.
- PR #2: reviewed constitution is awaiting merge approval; do not present its files as already in `main`.
