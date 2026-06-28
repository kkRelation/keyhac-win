param(
    [switch]$Console,
    [switch]$StopOnly
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ahkExe = "C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"
$scriptPath = Join-Path $scriptDir "KeyhacAhk.ahk"
$stateClientExe = "D:\C2D\Desktop\Code\Python\automation\state_center\target\release\state-client.exe"

if (-not (Test-Path -LiteralPath $ahkExe)) {
    throw "AutoHotkey v2 executable not found: $ahkExe"
}

if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "AHK script not found: $scriptPath"
}

function Stop-KeyhacAhkProcesses {
    $processes = Get-CimInstance Win32_Process -Filter "Name = 'AutoHotkey64.exe' OR Name = 'AutoHotkeyU64.exe' OR Name = 'AutoHotkey.exe'" |
        Where-Object { $_.CommandLine -like "*KeyhacAhk.ahk*" }

    foreach ($process in $processes) {
        try {
            Stop-Process -Id $process.ProcessId -Force -ErrorAction Stop
        } catch {
            if ($StopOnly) {
                Write-Warning "Existing AHK process '$($process.ProcessId)' cannot be stopped from this PowerShell session. Stop it from an elevated shell if needed."
                return $true
            }

            Write-Warning "Existing AHK process '$($process.ProcessId)' cannot be stopped from this PowerShell session. Reusing the running instance."
            return $true
        }
    }

    if ($processes) {
        Start-Sleep -Milliseconds 300
    }

    return $false
}

function Get-KeyhacAhkProcess {
    Get-CimInstance Win32_Process -Filter "Name = 'AutoHotkey64.exe' OR Name = 'AutoHotkeyU64.exe' OR Name = 'AutoHotkey.exe'" |
        Where-Object { $_.CommandLine -like "*KeyhacAhk.ahk*" } |
        Select-Object -First 1
}

function Start-KeyhacAhkStateWatch {
    param(
        [int]$ProcessId
    )

    if ($ProcessId -le 0 -or -not (Test-Path -LiteralPath $stateClientExe)) {
        return
    }

    Start-Process -FilePath $stateClientExe -ArgumentList @(
        "watch-process",
        "--source", "ahk",
        [string]$ProcessId,
        "3500",
        "1200"
    ) -WindowStyle Hidden
}

$reusedExistingProcess = Stop-KeyhacAhkProcesses

if ($StopOnly) {
    exit 0
}

if ($reusedExistingProcess) {
    $existing = Get-KeyhacAhkProcess
    if ($existing) {
        Start-KeyhacAhkStateWatch -ProcessId $existing.ProcessId
    }
    exit 0
}

if ($Console) {
    & $ahkExe $scriptPath
} else {
    $process = Start-Process -FilePath $ahkExe -ArgumentList @($scriptPath) -WorkingDirectory $scriptDir -WindowStyle Hidden -PassThru
    if ($process) {
        Start-KeyhacAhkStateWatch -ProcessId $process.Id
    }
}
