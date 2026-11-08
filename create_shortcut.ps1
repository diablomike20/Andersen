# Andersen Launcher asztali parancsikon letrehozasa
$ErrorActionPreference = "Stop"

$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Andersen.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = Join-Path $env:WINDIR "System32\wscript.exe"
$shortcut.Arguments = '"' + (Join-Path $base "Inditas.vbs") + '"'
$shortcut.WorkingDirectory = $base
$shortcut.IconLocation = Join-Path $base "assets\andersen-icon.ico"
$shortcut.Description = "Andersen - A tortenet muhelye"
$shortcut.Save()

Write-Output "Parancsikon letrehozva: $shortcutPath"
