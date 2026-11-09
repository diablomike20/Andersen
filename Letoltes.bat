@echo off
chcp 65001 >nul
title Andersen - telepito letoltese
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Letoltes.ps1"
echo.
pause
