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
    $env:LOCALAPPDATA = [Environment]::GetFolderPath('LocalApplicationData', 'Create')
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
    $powershell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
    # Task Scheduler creates the logged-on user's environment instead of inheriting
    # runneradmin's USERPROFILE variables through Start-Process -Credential.
    $action = New-ScheduledTaskAction -Execute $powershell -WorkingDirectory $testRoot `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`""
    $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 3)
    Register-ScheduledTask -TaskName $name -Action $action -Settings $settings `
        -User "$env:COMPUTERNAME\$name" -Password ([Net.NetworkCredential]::new('', $password).Password) `
        -RunLevel Limited | Out-Null
    $started = Get-Date
    Start-ScheduledTask -TaskName $name
    $finished = $false
    for ($i = 0; $i -lt 180; $i++) {
        Start-Sleep -Seconds 1
        $info = Get-ScheduledTaskInfo -TaskName $name
        $state = (Get-ScheduledTask -TaskName $name).State
        if ($info.LastRunTime -ge $started.AddSeconds(-2) -and $state -ne 'Running') {
            $finished = $true
            break
        }
    }
    Write-Output "Task state: $((Get-ScheduledTask -TaskName $name).State); result: $($info.LastTaskResult); started: $($info.LastRunTime)"
    if (Test-Path (Join-Path $testRoot 'progress.txt')) { Get-Content (Join-Path $testRoot 'progress.txt') }
    if (Test-Path (Join-Path $testRoot 'standard-user.log')) {
        Get-Content (Join-Path $testRoot 'standard-user.log')
    }
    if (-not $finished) { throw 'Standard-user task did not finish: see task state, progress marker and transcript above' }
    if ($info.LastTaskResult -ne 0) { throw "Standard-user test exit: $($info.LastTaskResult)" }
} finally {
    if (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue) {
        Stop-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
        Unregister-ScheduledTask -TaskName $name -Confirm:$false
    }
    if (Get-LocalUser -Name $name -ErrorAction SilentlyContinue) { Remove-LocalUser -Name $name }
    # The ephemeral runner is destroyed after this job; do not delete user profiles here.
}
