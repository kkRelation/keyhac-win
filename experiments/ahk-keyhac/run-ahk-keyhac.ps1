param(
    [switch]$Console,
    [switch]$StopOnly
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ahkExe = "C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"
$scriptPath = Join-Path $scriptDir "KeyhacAhk.ahk"

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

$reusedExistingProcess = Stop-KeyhacAhkProcesses

if ($StopOnly) {
    exit 0
}

if ($reusedExistingProcess) {
    exit 0
}

if ($Console) {
    & $ahkExe $scriptPath
} else {
    Start-Process -FilePath $ahkExe -ArgumentList @($scriptPath) -WorkingDirectory $scriptDir -WindowStyle Hidden
}
