Option Explicit

' Get the current script path
Function GetScriptPath()
    Dim objFSO, objFile
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(WScript.ScriptFullName)
    GetScriptPath = objFSO.GetParentFolderName(objFile)
End Function

' Get current path
Dim currentPath
currentPath = GetScriptPath()

' Create WScript Shell object
Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

' Build command
Dim command
command = """" & currentPath & "\login.exe"""""

' Run command with window hidden (0)
WshShell.Run command, 0, False

' Clean up
Set WshShell = Nothing 