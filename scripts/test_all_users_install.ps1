# Disposable GitHub Actions runner only. Test the elevated all-users path.
$ErrorActionPreference = 'Stop'
if ($env:GITHUB_ACTIONS -ne 'true') { throw 'Machine-wide installation test is CI-only' }
$setup = (Resolve-Path 'dist/KLAVA-Setup-x64.exe').Path
$uninstallKey = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\KLAVA.CurrentUser_is1'
if (Test-Path $uninstallKey) { throw 'Refusing to replace an existing machine installation' }
$arguments = '/ALLUSERS /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-'
$process = Start-Process -FilePath $setup -ArgumentList $arguments -PassThru -Wait
if ($process.ExitCode -ne 0) { throw "Machine-wide setup failed: $($process.ExitCode)" }
if (-not (Test-Path $uninstallKey)) { throw 'Machine-wide uninstall registration missing' }
$entry = Get-ItemProperty $uninstallKey
$app = $entry.InstallLocation.TrimEnd('\\')
Write-Output "Machine-wide InstallLocation: $app"
if (-not ($app.StartsWith($env:ProgramFiles, [StringComparison]::OrdinalIgnoreCase) -or $app.StartsWith(${env:ProgramFiles(x86)}, [StringComparison]::OrdinalIgnoreCase))) { throw "Machine install outside Program Files: $app" }
$exe = Join-Path $app 'KLAVA.exe'
if (-not (Test-Path $exe)) { throw "Machine-wide EXE missing from $app" }
if (-not (Test-Path (Join-Path $app 'default-exercises.klv'))) { throw 'Machine-wide seed missing' }
$uninstaller = Join-Path $app 'unins000.exe'
$p = Start-Process -FilePath $uninstaller -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART' -Wait -PassThru
if ($p.ExitCode -ne 0) { throw "Machine-wide uninstall failed: $($p.ExitCode)" }
if (Test-Path $exe) { throw 'Machine-wide EXE remains after uninstall' }
if (Test-Path $uninstallKey) { throw 'Machine-wide uninstall key remains' }
Write-Output 'PASS: all-users Program Files installation, registration and uninstall.'
