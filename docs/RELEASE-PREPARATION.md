# KLAVA — Beta release status

**Published:** 2026-10-29, `v0.3.1-beta.1` (public GitHub Pre-release).

**Verified:** https://github.com/avtotrainer/klava/releases/tag/v0.3.1-beta.1

- EXE: https://github.com/avtotrainer/klava/releases/download/v0.3.1-beta.1/KLAVA-Setup-x64.exe
- MSI: https://github.com/avtotrainer/klava/releases/download/v0.3.1-beta.1/KLAVA-x64.msi
- SHA256: https://github.com/avtotrainer/klava/releases/download/v0.3.1-beta.1/SHA256SUMS.txt
- GitHub Actions build and publication verified: https://github.com/avtotrainer/klava/actions/runs/40791969804
- Main source integration: https://github.com/avtotrainer/klava/pull/18
- Release source commit: `51a3ec940b0ea1541000b1cbb231c61da1120c7e`.

The automated beta workflow published this approved release on push to main that changed its workflow file. Its publishing job only runs for that push event, and refuses to overwrite an existing tag. For **future releases**, review and redesign the release trigger/inputs and explicit authorization; don't assume there is a general release automation already enabled.

**Tester acceptance still needed:** physical Windows visual check of new startup artwork, real restricted account installation, MSI upgrades between versions, GPO/Intune deployment, and code signing. Store no identifiable student data in reports.

---

# KLAVA — beta release preparation / handoff

**State:** Prepared in a review branch, not published. Public Release needs separate owner approval and merges into `main`.

## Source of truth

- Repository: https://github.com/avtotrainer/klava
- Proposed candidate: `v0.3.1-beta.1`
- Windows release workflow: `.github/workflows/prepare-beta-release.yml`
- Canonical binaries: `KLAVA-Setup-x64.exe`, `KLAVA-x64.msi` plus `SHA256SUMS.txt`
- Release notes: embedded in the guarded workflow, Georgian tester instructions here.
- User-submitted `resources/branding/welcome.png` is included in the frozen executable.
- The EXE package is per-user/all-users choice; MSI package is per-machine and requires administrator access.
- EXE and MSI are different Windows Installer ecosystems. Detection of existing EXE/MSI installations is best-effort. Do not test cross-format replacements on machines with irreplaceable settings.

## Exact release flow

1. Review PR dependency order from the currently open stacked PRs (#8, #10, #11, #12, #13, #14, #15, #16, #17) and merge **only after explicit authorization**; inspect actual PR base/mergeability before merging.
2. Merge and verify the release workflow on `main` after approval.
3. In repository Settings > Environments, configure `klava-release` with **required reviewers** and restrict deployments to `main`. The workflow references this environment but its protection rules are **NOT configured or verified** here. Without these settings, `publish=true` could publish immediately once the workflow exists on `main`. Do not enable publishing until protection is confirmed.
4. Manual workflow run with `version=v0.3.1-beta.1` and `publish=false`: builds both artifacts, compiles Python, checks Ruff/pytest, exercises real Tk, checks links, installs/uninstalls EXE+MSI, checks SHA256. Downloads available from the run; no public Release.
5. Review results, compare SHA256 and get explicit permission for a **public** pre-release.
6. Workflow run from `main`, `publish=true`; the protected `klava-release` environment reviewer approves. Workflow refuses to overwrite an existing tag.
7. Verify release URL, attached assets, tag, hashes and installation on actual tester computers. Post Slack invite only with authorization and verified KLAVA workspace.

## Testers / feedback

- Share one **Pre-release** link, not ephemeral workflow artifact links.
- For manual testing record OS version, installer format, install scope, screenshot, repro steps, expected/actual, and sanitised logs.
- Prefer a Slack channel `#klava-testing` only if owner explicitly approves channel creation.
- Confirm no student names, login credentials, personal exercise text or other personal data is shared.
- Automated physical non-admin Windows acceptance, MSI upgrades between versions, GPO/Intune deployment, digital signing and Windows SmartScreen reputation remain unverified.

## Important version caveat

EXE installer shows `0.3.1-beta.1`. MSI Windows Installer's `ProductVersion` must be numeric (`0.3.1`), so Add/Remove Programs may display `0.3.1` even when the matching distribution tag is `v0.3.1-beta.1`. This difference is intentional and should be explained to testers.

## Rollback

No public Release or deployment has been made by this preparation. If candidate testing fails, do not publish; fix in the review branch and regenerate candidate artifacts. Never reuse an existing public release tag for changed binaries. User exercises remain in their own `%LOCALAPPDATA%\KLAVA` directories.
