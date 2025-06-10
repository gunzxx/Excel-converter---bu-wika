Set objShell = CreateObject("WScript.Shell")

' ' Ganti path di bawah dengan folder proyek Git kamu
' repoPath = "C:\Users\NamaKamu\Documents\projectku"

' ' Masuk ke folder repo
' objShell.CurrentDirectory = repoPath

' Jalankan git pull di terminal
command = "cmd /c git pull && pause"

objShell.Run command, 1, True
