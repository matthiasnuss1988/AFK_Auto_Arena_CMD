Set WshShell = CreateObject("WScript.Shell")
dim  Player,restartCounter, restartCondition,periodicRestart, teamTime, min, sec, numberOfTeams, autokampf, modusValue,scriptTime
min=60
sec=1000
numberOfTeams=5
autokampf="false"
modusValue=6
scriptTime=9999
periodicRestart=120
restartCounter=0
restartCondition=0

strTitle = "Stage Time"
strMsg = strMsg & "Examples:     Easy  |  Medium  |  Hard" & vbCR
strMsg = strMsg & "" & vbCR
strMsg = strMsg & "King's Tower:	5  |      7.5     |  12.5" & vbCR
strMsg = strMsg & "Campaign:	5  |      15      |  20" & vbCR
strMsg = strMsg & "Fraction Tower:	2  |       3       |  5" & vbCR
strMsg = strMsg & "" & vbCR
strMsg = strMsg & "Enter Time in Minutes" & vbCR

strFlag = False

Do While strFlag = False
	teamTime = InputBox(strMsg,strTitle,3)
	If IsNumeric(user) then
			strFlag = True
	else
			strFlag = False
	End If
Loop
scriptTime=scriptTime*min
userHours=Int(teamTime/min)
userMin=Int(teamTime-userHours*min)
userSec=Int((teamtime-userHours*min-userMin)*min)
cycles=Int(scriptTime/(numberOfTeams*(teamTime+0.5))+0.99)
REM each script takes 0.5min
REM 4 Team a 12.5 Min is 50 min
startPlayer()
for i=1 to cycles
	for j=1 to numberOfTeams
		WshShell.AppActivate "BlueStacks App Player"
		WshShell.SendKeys "h"
		Wscript.sleep 2*sec
		WshShell.SendKeys "x"
		Wscript.sleep 2*sec
		WshShell.SendKeys "y"
		Wscript.sleep 2*sec
		WshShell.SendKeys "1"
		Wscript.sleep 2*sec
		WshShell.SendKeys "t"
		Wscript.sleep 2*sec
		WshShell.SendKeys(j)
		Wscript.sleep 2*sec
		WshShell.SendKeys "k"
		Wscript.sleep 2*sec
		WshShell.SendKeys "v"
		WScript.echo("")
		WScript.echo(vbTab&"______________________TEAM " & j &"______________________")
		Wscript.sleep 2*sec
		WshShell.SendKeys "a"
		Wscript.sleep 2*sec
		WshShell.SendKeys "v"
		WScript.echo("")
		WScript.echo(vbTab&"Team " & j & " fights the stage for " & userHours & " h : " & userMin & " min : " & userSec & " sec")
		WScript.echo("")
		remaining=teamTime*min
		Do while remaining>0
			remainingHours=Int(remaining/min^2)
			remainingMin=Int(remaining/min-remainingHours*min)
			remainingSec=Int(remaining-remainingHours*min^2-remainingMin*min)
			If remaining = teamTime*min Then
				WScript.echo(vbTab&"Remaining:"& vbTab & remainingHours & " h : " & remainingMin & " min : " & remainingSec & " sec")
			else
				If teamTime<=1 Then
					If remaining Mod 10=0 Then
					WScript.echo(vbTab&vbTab&vbTab & remainingHours & " h : " & remainingMin & " min : " & remainingSec & " sec")
					end if
				else
					If remaining Mod min=0 Then
					WScript.echo(vbTab&vbTab&vbTab & remainingHours & " h : " & remainingMin & " min : " & remainingSec & " sec")
					End If
				End If
			End If
			WScript.sleep 1*sec
			remaining= remaining-1
		Loop
		WshShell.SendKeys "v"
		WScript.sleep 2*sec
		WshShell.SendKeys "v"
		WScript.sleep 150
		WshShell.SendKeys "p"
		WScript.sleep 2*sec
		WshShell.SendKeys "e"
		WScript.sleep 2*sec
	next
	runTime=i*numberOfTeams*(teamTime+0.5)
	WScript.echo("")
	' WScript.echo(vbTab&"Actual runtime: " & runTime & " min")
	' WScript.echo(vbTab&"teamTime " & teamTime & " i " & i & " cycles " & cycles & " Neustart nach " & periodicRestart	&" min")
	runHours=Int(runTime/min)
	runMin=Int(runTime-runHours*min)
	runSec=Int((runTime-runHours*min-runMin)*min)
	WScript.echo("")
	WScript.echo(vbTab&"Runtime: " & runHours & " h : " & runMin & " min : " & runSec & " sec")
	restartCondition=Fix(runTime/periodicRestart)
	' WScript.echo("I arrive here")
	If restartCondition<>restartCounter Then
		WScript.echo(vbTab&"Restart Condition: " & restartCondition & " fullfilled")
		restartCounter=restartCounter+1
		WScript.echo(vbTab&"The Payer performs timeout close")
		WScript.echo("")
		Player.Terminate
		autokampf="false"
		startPlayer()
	End if	
next
Sub startPlayer()
		strPathPlayer = """C:\Program Files\BlueStacks_nxt\HD-Player.exe"""
		strAttr1 = " --instance P64"
		strAttr2 = " --cmd launchApp"
		strAttr3 = " --package com.lilithgame.hgame.gp"
		strArguments =  strPathPlayer & strAttr2 & strAttr3
		Set Player = WshShell.Exec(strArguments)
		WshShell.Run strArguments
		' WriteLogger(strPathPlayer & strAttr1 & strAttr2 & strAttr3 & chr(34)& strAttr4 & chr(34))
		'Checked is fight mode'
		If autokampf = "true" Then
			WshShell.AppActivate "BlueStacks App Player 1"
			WScript.echo(vbTab&"___________________<AFK ARENA>____________________")
			WScript.echo("")
			WScript.echo(vbTab&"Bluestacks is activated")
			WScript.sleep 2*sec
		else
			WScript.echo(vbTab&"___________________<AFK ARENA>____________________")
			WScript.echo("")
			WScript.echo(vbTab&"...Initialize...")
			WScript.echo("")
			WScript.sleep 0.5*sec*min
			modusPlayer()
		End If
End Sub
Sub modusPlayer()
	WshShell.AppActivate "BlueStacks App Player 1"
	WScript.echo(vbTab&"Bluestacks is activated")
	' WshShell.SendKeys "+(^T)"
	' WScript.sleep 2*sec
	Select case modusValue 
		case 1 'Feldzug'
			WshShell.SendKeys "h"
			WScript.sleep 2*sec
			WshShell.SendKeys "x"
			WScript.sleep 2*sec
			WshShell.SendKeys "y"
			WScript.sleep 2*sec
		case 2 'Königsturm'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
		case 3 'Himmlisches Heiligtum'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "h"
			WScript.sleep 2*sec
		case 4 'Turm des Lichtes'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "l"
			WScript.sleep 2*sec
		case 5 'Die Brutale Zitadelle'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "b"
			WScript.sleep 2*sec
		case 6 'Höllische Festung'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "y"
			WScript.sleep 2*sec
		case 7 'Die Verlassene Nekropolis'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "4"
			WScript.sleep 2*sec
		case 8 'Der Weltenbaum'
			WshShell.SendKeys "a"
			WScript.sleep 2*sec
			WshShell.SendKeys "e"
			WScript.sleep 2*sec
			WshShell.SendKeys "1"
			WScript.sleep 2*sec
	End Select
End Sub


