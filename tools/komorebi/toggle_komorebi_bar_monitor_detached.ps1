param(
    [Parameter(Mandatory = $true)]
    [int]$Monitor
)

$ErrorActionPreference = "Stop"

$ExePath = "D:\C2D\Desktop\Code\Python\automation\kanata_config\tools\komorebi-bar-toggle\target\release\komorebi-bar-toggle.exe"
if (Test-Path -LiteralPath $ExePath) {
    Start-Process -FilePath $ExePath -ArgumentList @($Monitor) -WindowStyle Hidden
    exit 0
}

$ScriptPath = Join-Path $PSScriptRoot "toggle_komorebi_bar_monitor.py"
$Pythonw = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
if (-not $Pythonw) {
    $Pythonw = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $Pythonw) {
    throw "pythonw/python not found in PATH"
}

Start-Process -FilePath $Pythonw -ArgumentList @($ScriptPath, $Monitor) -WindowStyle Hidden
