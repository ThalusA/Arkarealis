@echo off
color 07
IF EXIST build (
    set MainPath = dir /s /b main.exe
    "%MainPath%"
) ELSE (
    choice /M "Project not build, do you want to build it then launch it ? "
    IF ERRORLEVEL 1 GOTO BUILDING
    IF ERRORLEVEL 2 GOTO EXIT 
)
:BUILDING
start setup.bat
:EXIT 
pause