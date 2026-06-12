param(
    [switch]$Console,
    [switch]$StopOnly
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
$keyhacExe = Join-Path $repoRoot "keyhac.exe"
$stateClientExe = "D:\C2D\Desktop\Code\Python\automation\state_center\target\release\state-client.exe"

if (-not (Test-Path -LiteralPath $keyhacExe)) {
    throw "keyhac.exe not found: $keyhacExe"
}

function Stop-KeyhacProcesses {
    $processes = Get-Process -Name "keyhac" -ErrorAction SilentlyContinue
    foreach ($process in $processes) {
        try {
            Stop-Process -Id $process.Id -Force -ErrorAction Stop
        } catch {
            if ($StopOnly) {
                Write-Warning "Existing keyhac process '$($process.Id)' cannot be stopped from this PowerShell session. Stop it from an elevated shell if needed."
                return $true
            }

            Write-Warning "Existing keyhac process '$($process.Id)' cannot be stopped from this PowerShell session. Reusing the running instance."
            return $true
        }
    }

    if ($processes) {
        Start-Sleep -Milliseconds 300
    }

    return $false
}

function Start-KeyhacStateWatch {
    param(
        [int]$ProcessId
    )

    if ($ProcessId -le 0 -or -not (Test-Path -LiteralPath $stateClientExe)) {
        return
    }

    Start-Process -FilePath $stateClientExe -ArgumentList @(
        "watch-process",
        "--source", "keyhac",
        [string]$ProcessId,
        "3500",
        "1200"
    ) -WindowStyle Hidden
}

$reusedExistingProcess = Stop-KeyhacProcesses

if ($StopOnly) {
    exit 0
}

if ($reusedExistingProcess) {
    $existing = Get-Process -Name "keyhac" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($existing) {
        Start-KeyhacStateWatch -ProcessId $existing.Id
    }
    exit 0
}

if ($Console) {
    Push-Location -LiteralPath $repoRoot
    try {
        & $keyhacExe
    } finally {
        Pop-Location
    }
} else {
    $process = Start-Process -FilePath $keyhacExe -WorkingDirectory $repoRoot -WindowStyle Hidden -PassThru
    if ($process) {
        Start-KeyhacStateWatch -ProcessId $process.Id
    }
}
