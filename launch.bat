@echo off
color 07
:START
dir /s /b main.exe>tmpFile
set /p MainPath=<tmpFile
del tmpFile
IF /I "%MainPath%" NEQ "" ( CALL "%MainPath%" && GOTO EXIT )
choice /M "Project not build, do you want to build it then launch it ? "
IF %ERRORLEVEL% EQU 1 GOTO BUILDING
IF %ERRORLEVEL% EQU 2 GOTO EXIT 
:BUILDING
CALL setup.bat
GOTO START
:EXIT
pause