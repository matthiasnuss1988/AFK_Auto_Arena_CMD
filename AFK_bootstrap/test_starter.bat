@echo off
powershell -Command "Start-Process cmd -ArgumentList '/c python \"%~dp0test.py\" & pause' -Verb RunAs"
