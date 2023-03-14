@echo off
setlocal enableDelayedExpansion

for /f "tokens=2 USEBACKQ" %%f in (`tasklist /NH /FI "WINDOWTITLE eq AFK ARENA*"`) do (
		taskkill /F /fi "pid eq %%f" /T 2>nul
		)

title AFK ARENA
REM kills running script 
set "dat=Teams_via_Hotkeys"
set "script="%~dp0%dat%.vbs""
for /f "usebackq tokens=3" %%s in (
    `WMIC process where "name='cscript.exe'" get commandline^,processid ^| findstr /i /c:"%%vbs%%"`
) do (
    taskkill /f /fi "pid eq %%s">nul
)
for /f "usebackq tokens=3" %%u in (
    `WMIC process where "name='wscript.exe'" get commandline^,processid ^| findstr /i /c:"%%vbs%%"`
) do (
    taskkill /f /fi "pid eq %%u">nul
)
call cscript %script%