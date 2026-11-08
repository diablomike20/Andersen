@echo off
rem Andersen Launcher - hibakereso inditas (lathato konzollal)
cd /d "%~dp0"
python "andersen_launcher.py"
if errorlevel 1 pause
