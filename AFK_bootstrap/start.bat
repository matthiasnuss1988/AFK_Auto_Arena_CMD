@echo off
set "dat=test"
set "script="%~dp0%dat%.py""
python %script%

pause