# Disposable GitHub Windows runner only: actual install, upgrade and uninstall.
$ErrorActionPreference = 'Stop'
$setup = (Resolve-Path 'dist/KLAVA-Setup-x64.exe').Path
$app = Join-Path $env:ProgramFiles 'KLAVA'
$data = Join-Path $env:LOCALAPPDATA 'KLAVA/exercises.txt'
$menu = Join-Path ([Environment]::GetFolderPath('CommonPrograms')) 'KLAVA'
if (Test-Path $app) { throw 'Refusing to test over an existing installation' }
if (Test-Path (Split-Path $data)) { throw 'Refusing to test over existing user data' }

function Invoke-Setup {
    $process = Start-Process -FilePath $setup -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-' -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "Installer exit: $($process.ExitCode)" }
}

function Test-Launch {
    $exe = Join-Path $app 'KLAVA.exe'
    $process = Start-Process -FilePath $exe -WorkingDirectory $env:RUNNER_TEMP -PassThru
    try {
        $found = $false
        for ($i = 0; $i -lt 60; $i++) {
            Start-Sleep -Seconds 1
            $window = Get-Process | Where-Object { $_.Path -eq $exe -and $_.MainWindowTitle -like 'KLAVA*' }
            if ($window) { $found = $true; break }
            if ($process.HasExited) { throw 'Installed EXE exited before opening its window' }
        }
        if (-not $found) { throw 'Installed KLAVA window did not appear' }
    } finally {
        taskkill /PID $process.Id /T /F
    }
}

Invoke-Setup
if (-not (Test-Path (Join-Path $app 'KLAVA.exe'))) { throw 'EXE not installed in Program Files' }
if (-not (Test-Path (Join-Path $app 'default-exercises.txt'))) { throw 'Missing installed seed' }
if (Test-Path $data) { throw 'Elevated installer must not create user data' }
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
if ((Get-FileHash $data).Hash -ne (Get-FileHash (Join-Path $app 'default-exercises.txt')).Hash) { throw 'Seed mismatch' }
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
if (Test-Path (Join-Path $menu 'KLAVA.lnk')) { throw 'Uninstall left the Start shortcut' }
if ((Get-FileHash $data).Hash -ne $editedHash) { throw 'Uninstall removed or changed user exercises' }
Write-Output 'PASS: Program Files install; both shortcuts; first-run seed; installed EXE launch; reinstall preserves edits; uninstall preserves user exercises.'
