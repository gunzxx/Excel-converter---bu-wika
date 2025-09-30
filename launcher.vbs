Set fso = CreateObject("Scripting.FileSystemObject")
desktopPath = CreateObject("WScript.Shell").SpecialFolders("Desktop")
currentFile = WScript.ScriptFullName
destinationFile = desktopPath & "\" & fso.GetFileName(currentFile)

If Not fso.FileExists(destinationFile) Then
    fso.CopyFile currentFile, destinationFile
End If


Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd.exe /k python app.py", 1, False
' WScript.Sleep 3000
' objShell.Run "http://127.0.0.1:5000", 1, False

' Set WshShell = CreateObject("WScript.Shell")
' WshShell.Run "cmd /c start http://127.0.0.1:5000", 0, False
' WshShell.Run "cmd /k cd /d 'D:\Semester-7\Projek Bu Wika 2' && set FLASK_APP=app.py && python -m flask run", 1, False
