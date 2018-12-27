@echo off
color 07
:START
dir /s /b main.exe>tmpFile
set /p MainPath=<tmpFile
del tmpFile
IF /I "%MainPath%" NEQ "" CALL "%MainPath%" && GOTO EXIT
choice /M "Project not build, do you want to build it then launch it ? "
IF ERRORLEVEL==1 GOTO BUILDING
IF ERRORLEVEL==2 GOTO EXIT 
:BUILDING
setup.bat
GOTO START
:EXIT
pause