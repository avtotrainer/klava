# Isolated CI only: create a non-admin Windows account and exercise the same installer.
$ErrorActionPreference = 'Stop'
if ($env:GITHUB_ACTIONS -ne 'true') { throw 'This account-creation test is CI-only' }
$name = 'klavatest' + [Guid]::NewGuid().ToString('N').Substring(0, 6)
$password = ConvertTo-SecureString ('Aa9!' + [Guid]::NewGuid().ToString('N')) -AsPlainText -Force
$testRoot = Join-Path $env:PUBLIC $name
New-Item -ItemType Directory -Path (Join-Path $testRoot 'dist') -Force | Out-Null
Copy-Item 'dist/KLAVA-Setup-x64.exe' (Join-Path $testRoot 'dist')
Copy-Item 'scripts/test_windows_installer.ps1' $testRoot
try {
    $user = New-LocalUser -Name $name -Password $password -AccountNeverExpires
    $usersGroup = Get-LocalGroup -SID 'S-1-5-32-545'
    Add-LocalGroupMember -Group $usersGroup -Member $user
    # Public test payload is readable; give this disposable account its own log directory.
    & icacls $testRoot /grant "${name}:(OI)(CI)M" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Could not grant test-directory access' }
    $wrapper = Join-Path $testRoot 'run.ps1'
    @'
$ErrorActionPreference = 'Stop'
Start-Transcript -Path (Join-Path $PSScriptRoot 'standard-user.log')
'wrapper-start' | Set-Content (Join-Path $PSScriptRoot 'progress.txt')
try {
    Set-Location $PSScriptRoot
    $knownLocal = [Environment]::GetFolderPath('LocalApplicationData', 'Create')
    if ([string]::IsNullOrWhiteSpace($knownLocal)) {
        # A fresh CI account may lack a loaded user profile in a credentialed process.
        # Keep its test data in an isolated ACL-protected directory rather than
        # inheriting the administrator's LOCALAPPDATA value.
        $knownLocal = Join-Path $PSScriptRoot 'isolated-localappdata'
    }
    $env:LOCALAPPDATA = $knownLocal
    New-Item -ItemType Directory -Path $env:LOCALAPPDATA -Force | Out-Null
    'localappdata-ready' | Set-Content (Join-Path $PSScriptRoot 'progress.txt')
    $env:TEMP = Join-Path $env:LOCALAPPDATA 'Temp'
    $env:TMP = $env:TEMP
    New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
    'running-installer-check' | Set-Content (Join-Path $PSScriptRoot 'progress.txt')
    & (Join-Path $PSScriptRoot 'test_windows_installer.ps1') -RequireStandardUser -Headless
    if (-not $?) { throw 'Installer verification failed' }
    'completed-successfully' | Set-Content (Join-Path $PSScriptRoot 'progress.txt')
    Stop-Transcript
    exit 0
} catch {
    ('failed: ' + $_) | Set-Content (Join-Path $PSScriptRoot 'progress.txt')
    Write-Output $_
    Stop-Transcript
    exit 1
}
'@ | Set-Content $wrapper
    # Avoid Task Scheduler: hosted runners may deny batch-logon to fresh users.
    # Start-Process with explicit credentials must run with the user's own token.
    $powershell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
    Write-Output 'Launching installer verification under temporary standard-user credentials.'
    $proc = Start-Process -FilePath $powershell -Credential ([PSCredential]::new(
        "$env:COMPUTERNAME\$name", $password
    )) -WorkingDirectory $testRoot -ArgumentList @(
        '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
        '-File', "`"$wrapper`""
    ) -PassThru -WindowStyle Hidden
    if (-not $proc.WaitForExit(120000)) {
        if (-not $proc.HasExited) { $proc.Kill() }
        throw 'Direct standard-user process did not complete within 120 seconds'
    }
    Write-Output "Standard-user verification exited with $($proc.ExitCode)"
    if (Test-Path (Join-Path $testRoot 'progress.txt')) {
        Get-Content (Join-Path $testRoot 'progress.txt')
    }
    if (Test-Path (Join-Path $testRoot 'standard-user.log')) {
        Get-Content (Join-Path $testRoot 'standard-user.log')
    }
    if ($proc.ExitCode -ne 0) {
        throw "Direct standard-user verification failed: exit $($proc.ExitCode)"
    }
} finally {
    if (Get-LocalUser -Name $name -ErrorAction SilentlyContinue) { Remove-LocalUser -Name $name }
    # The ephemeral runner is destroyed after this job; do not delete user profiles here.
}
