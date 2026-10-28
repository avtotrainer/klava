# Isolated CI only: create a non-admin Windows account and exercise the same installer.
$ErrorActionPreference = 'Stop'
if ($env:GITHUB_ACTIONS -ne 'true') { throw 'This account-creation test is CI-only' }
$name = 'klavatest' + [Guid]::NewGuid().ToString('N').Substring(0, 6)
$password = ConvertTo-SecureString ('Aa9!' + [Guid]::NewGuid().ToString('N')) -AsPlainText -Force
$testRoot = Join-Path $env:PUBLIC $name
New-Item -ItemType Directory -Path (Join-Path $testRoot 'dist') -Force | Out-Null
Copy-Item 'dist/KLAVA-User-Setup-x64.exe' (Join-Path $testRoot 'dist')
Copy-Item 'scripts/test_windows_installer.ps1' $testRoot
try {
    $user = New-LocalUser -Name $name -Password $password -AccountNeverExpires
    $usersGroup = Get-LocalGroup -SID 'S-1-5-32-545'
    Add-LocalGroupMember -Group $usersGroup -Member $user
    $credential = [PSCredential]::new("$env:COMPUTERNAME\$name", $password)
    # Public test payload is readable; give this disposable account its own log directory.
    & icacls $testRoot /grant "${name}:(OI)(CI)M" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Could not grant test-directory access' }
    $wrapper = Join-Path $testRoot 'run.ps1'
    @'
$ErrorActionPreference = 'Stop'
Start-Transcript -Path (Join-Path $PSScriptRoot 'standard-user.log')
try {
    Set-Location $PSScriptRoot
    $env:LOCALAPPDATA = [Environment]::GetFolderPath('LocalApplicationData', 'Create')
    $env:TEMP = Join-Path $env:LOCALAPPDATA 'Temp'
    $env:TMP = $env:TEMP
    New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
    & (Join-Path $PSScriptRoot 'test_windows_installer.ps1') -RequireStandardUser -Headless
    if (-not $?) { throw 'Installer verification failed' }
    Stop-Transcript
    exit 0
} catch {
    Write-Output $_
    Stop-Transcript
    exit 1
}
'@ | Set-Content $wrapper
    $powershell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
    $process = Start-Process -FilePath $powershell -Credential $credential -LoadUserProfile `
        -WorkingDirectory $testRoot -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`"" -PassThru
    if (-not $process.WaitForExit(180000)) {
        Stop-Process -Id $process.Id -Force
        throw 'Standard-user installer test exceeded 180 seconds'
    }
    $process.Refresh()
    Get-Content (Join-Path $testRoot 'standard-user.log')
    if ($process.ExitCode -ne 0) { throw "Standard-user test exit: $($process.ExitCode)" }
} finally {
    if (Get-LocalUser -Name $name -ErrorAction SilentlyContinue) { Remove-LocalUser -Name $name }
    # The ephemeral runner is destroyed after this job; do not delete user profiles here.
}
