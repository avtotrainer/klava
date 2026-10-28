$ErrorActionPreference = 'Stop'
$msi = (Resolve-Path 'dist/KLAVA-x64.msi').Path
$destination = Join-Path $env:ProgramFiles 'KLAVA MSI'
$exe = Join-Path $destination 'KLAVA.exe'
$klv = Join-Path $destination 'default-exercises.klv'
$log = Join-Path $env:RUNNER_TEMP 'klava-msi-install.log'
$removeLog = Join-Path $env:RUNNER_TEMP 'klava-msi-remove.log'
if (Test-Path $destination) { throw "MSI destination already exists: $destination" }
function Invoke-Msi([string[]]$Arguments) {
    $p = Start-Process -FilePath msiexec.exe -ArgumentList $Arguments -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw "msiexec exit code $($p.ExitCode); arguments: $Arguments" }
}
try {
    Invoke-Msi @('/i', "`"$msi`"", '/qn', '/norestart', '/L*v', "`"$log`"")
    if (!(Test-Path $exe) -or !(Test-Path $klv)) { throw 'Expected MSI payload is missing' }
    Write-Output 'Verified MSI installation and both payload files.'
} finally {
    Invoke-Msi @('/x', "`"$msi`"", '/qn', '/norestart', '/L*v', "`"$removeLog`"")
}
if ((Test-Path $exe) -or (Test-Path $klv)) { throw 'MSI uninstall left application payload behind' }
Write-Output 'Verified MSI uninstall.'
