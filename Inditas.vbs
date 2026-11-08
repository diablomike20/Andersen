' Andersen Launcher - inditas konzolablak nelkul
Option Explicit

Dim fso, shell, base, script
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

base = fso.GetParentFolderName(WScript.ScriptFullName)
script = base & "\andersen_launcher.py"
shell.CurrentDirectory = base

On Error Resume Next
shell.Run "pythonw.exe """ & script & """", 0, False
If Err.Number <> 0 Then
    Err.Clear
    shell.Run "pyw.exe -3 """ & script & """", 0, False
End If
On Error GoTo 0
