param(
    [switch]$Console,
    [ValidateSet("kanata", "keyhac", "whkd")]
    [string]$Backend = "kanata",
    [switch]$StartHidden
)

$ErrorActionPreference = "Stop"

$candidates = @(
    "D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\release\d-c2ddesktopcoderuststoolskomorebi-shortcuts-tauri.exe",
    "D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-tauri\src-tauri\target\debug\d-c2ddesktopcoderuststoolskomorebi-shortcuts-tauri.exe",
    "D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-slint\target\release\komorebi-shortcuts-slint.exe",
    "D:\C2D\Desktop\Code\Rust\sTools\komorebi-shortcuts-slint\target\debug\komorebi-shortcuts-slint.exe"
)

$shortcutExe = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

function Get-PythonExecutable {
    $pythonw = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
    if ($pythonw) {
        return $pythonw
    }

    return (Get-Command python -ErrorAction SilentlyContinue).Source
}

function Start-ShortcutPythonFallback {
    $pythonExe = Get-PythonExecutable
    if (-not $pythonExe) {
        throw "No komorebi shortcuts executable found, and python/pythonw is not available. Checked: $($candidates -join '; ')"
    }

    $fallbackScript = "D:\C2D\Desktop\Code\Python\automation\komorebi_config\show_komorebi_shortcuts.py"
    if (-not (Test-Path -LiteralPath $fallbackScript)) {
        throw "No komorebi shortcuts executable found, and fallback script is missing: $fallbackScript"
    }

    $arguments = @($fallbackScript, "--backend", $Backend)
    if ($StartHidden) {
        $arguments += "--start-hidden"
    }

    if ($Console) {
        & $pythonExe @arguments
    } else {
        Start-Process -FilePath $pythonExe -ArgumentList $arguments -WindowStyle Hidden
    }
}

if (-not $shortcutExe) {
    Start-ShortcutPythonFallback
    exit 0
}

if ($Console) {
    & $shortcutExe
} else {
    Start-Process -FilePath $shortcutExe -WindowStyle Hidden
}
