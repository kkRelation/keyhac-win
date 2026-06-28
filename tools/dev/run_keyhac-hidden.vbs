Option Explicit

Dim shell, scriptPath, command, windowStyle, psWindowStyle, forwardedArgs, i
Dim wmi, startup, process, processId

Set shell = CreateObject("WScript.Shell")
scriptPath = "D:\C2D\Desktop\Code\Python\automation\craftware\keyhac-win\tools\dev\run_keyhac.ps1"

If InStr(1, LCase(WScript.FullName), "cscript.exe", vbTextCompare) > 0 Then
    forwardedArgs = ""
    For i = 0 To WScript.Arguments.Count - 1
        forwardedArgs = forwardedArgs & " """ & Replace(WScript.Arguments(i), """", "\""") & """"
    Next
    shell.Run "wscript.exe //B """ & WScript.ScriptFullName & """" & forwardedArgs, 0, False
    WScript.Quit 0
End If

' Default to hidden. Pass "show" as the first argument to run visibly.
windowStyle = 0
If WScript.Arguments.Count > 0 Then
    If LCase(WScript.Arguments(0)) = "show" Then
        windowStyle = 1
    End If
End If

If windowStyle = 0 Then
    psWindowStyle = "Hidden"
Else
    psWindowStyle = "Normal"
End If

forwardedArgs = ""
For i = 0 To WScript.Arguments.Count - 1
    forwardedArgs = forwardedArgs & " """ & Replace(WScript.Arguments(i), """", "\""") & """"
Next

command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle " & _
          psWindowStyle & _
          " -File """ & scriptPath & """" & forwardedArgs

If windowStyle = 0 Then
    Set wmi = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
    Set startup = wmi.Get("Win32_ProcessStartup").SpawnInstance_
    startup.ShowWindow = 0
    Set process = wmi.Get("Win32_Process")
    process.Create command, Null, startup, processId
Else
    shell.Run command, windowStyle, False
End If
