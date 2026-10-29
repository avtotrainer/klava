# Disposable GitHub Windows runner only: actual install, upgrade and uninstall.
param([switch]$RequireStandardUser, [switch]$Headless)
$ErrorActionPreference = 'Stop'
if ($RequireStandardUser) {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'Test must run without administrator rights'
    }
    Write-Output 'Confirmed: test process is a standard user without administrator rights.'
}
$setup = (Resolve-Path 'dist/KLAVA-Setup-x64.exe').Path
$app = Join-Path $env:LOCALAPPDATA 'Programs/KLAVA'
$data = Join-Path $env:LOCALAPPDATA 'KLAVA/exercises.klv'
$menu = Join-Path ([Environment]::GetFolderPath('Programs')) 'KLAVA'
if (Test-Path $app) { throw 'Refusing to test over an existing installation' }
$existingDataHash = if (Test-Path $data) { (Get-FileHash $data).Hash } else { $null }

function Invoke-Setup {
    $process = Start-Process -FilePath $setup -ArgumentList '/CURRENTUSER /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-' -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "Installer exit: $($process.ExitCode)" }
}

function Test-Launch {
    $exe = Join-Path $app 'KLAVA.exe'
    $process = Start-Process -FilePath $exe -WorkingDirectory $env:TEMP -PassThru
    try {
        $found = $false
        for ($i = 0; $i -lt 60; $i++) {
            Start-Sleep -Seconds 1
            $window = $null
            if (-not $Headless) {
                $window = Get-Process | Where-Object { $_.Path -eq $exe -and $_.MainWindowTitle -like 'KLAVA*' }
            }
            if ($window -or ($Headless -and (Test-Path $data) -and -not $process.HasExited)) { $found = $true; break }
            if ($process.HasExited) { throw 'Installed EXE exited before opening its window' }
        }
        if (-not $found) { throw 'Installed KLAVA window did not appear' }
        # PyInstaller onefile has a bootloader process and an application process.
        # A second launch must exit, while the first application's window survives.
        $duplicate = Start-Process -FilePath $exe -WorkingDirectory $env:TEMP -PassThru
        try {
            if (-not $duplicate.WaitForExit(30000)) { throw 'Duplicate KLAVA did not exit' }
            if ($duplicate.ExitCode -ne 0) { throw 'Duplicate launch failed unexpectedly' }
            $process.Refresh()
            if ($process.HasExited) { throw 'Duplicate launch stopped the original KLAVA' }
            if (-not $Headless) {
                $windows = @(Get-Process | Where-Object { $_.Path -eq $exe -and $_.MainWindowTitle -like 'KLAVA*' })
                if ($windows.Count -ne 1) { throw 'Expected exactly one KLAVA window' }
            }
        } finally {
            if (-not $duplicate.HasExited) { taskkill /PID $duplicate.Id /T /F }
        }
    } finally {
        taskkill /PID $process.Id /T /F
    }
}

Invoke-Setup
if (-not (Test-Path (Join-Path $app 'KLAVA.exe'))) { throw 'EXE not installed in the user profile' }
if (-not (Test-Path (Join-Path $app 'default-exercises.klv'))) { throw 'Missing installed seed' }
if ($existingDataHash) {
    if ((Get-FileHash $data).Hash -ne $existingDataHash) { throw 'Installer modified pre-existing exercises' }
} elseif (Test-Path $data) {
    throw 'Installer must not create exercise data'
}
$uninstallKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\KLAVA.CurrentUser_is1'
if (-not (Test-Path $uninstallKey)) { throw 'Missing per-user uninstall registration' }
if (Test-Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\KLAVA.CurrentUser_is1') {
    throw 'Unexpected machine-wide uninstall registration'
}
$shell = New-Object -ComObject WScript.Shell
foreach ($name in @('KLAVA', 'Edit exercises')) {
    $link = Join-Path $menu "$name.lnk"
    if (-not (Test-Path $link)) { throw "Missing shortcut: $name" }
    $shortcut = $shell.CreateShortcut($link)
    if ($shortcut.TargetPath -ne (Join-Path $app 'KLAVA.exe')) { throw "Wrong shortcut target: $name" }
    if ($name -eq 'Edit exercises' -and $shortcut.Arguments -ne '--edit-exercises') { throw 'Missing editor argument' }
}
Test-Launch
if (-not (Test-Path $data)) { throw 'First launch did not create user exercises' }
if ((Get-FileHash $data).Hash -ne (Get-FileHash (Join-Path $app 'default-exercises.klv')).Hash) { throw 'Seed mismatch' }
[IO.File]::WriteAllText($data, "A B`nB A`n", [Text.UTF8Encoding]::new($false))
$editedHash = (Get-FileHash $data).Hash
Invoke-Setup
Test-Launch
if ((Get-FileHash $data).Hash -ne $editedHash) { throw 'Reinstall overwrote exercises' }
$uninstaller = Join-Path $app 'unins000.exe'
$process = Start-Process -FilePath $uninstaller -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART' -Wait -PassThru
if ($process.ExitCode -ne 0) { throw "Uninstaller exit: $($process.ExitCode)" }
for ($i = 0; $i -lt 20 -and (Test-Path (Join-Path $app 'KLAVA.exe')); $i++) { Start-Sleep -Seconds 1 }
if (Test-Path (Join-Path $app 'KLAVA.exe')) { throw 'Uninstall left the application executable' }
if (Test-Path $uninstallKey) { throw 'Uninstall left HKCU registration' }
if (Test-Path (Join-Path $menu 'KLAVA.lnk')) { throw 'Uninstall left the Start shortcut' }
if ((Get-FileHash $data).Hash -ne $editedHash) { throw 'Uninstall removed or changed user exercises' }
Write-Output 'PASS: per-user profile install; both shortcuts; first-run seed; installed EXE launch; reinstall preserves edits; uninstall preserves user exercises.'
