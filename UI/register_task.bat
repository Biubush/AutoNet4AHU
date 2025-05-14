@echo off
setlocal enabledelayedexpansion

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    
    :: Self-elevate the script
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo Administrator privileges confirmed.

:: Get the directory of the current script
set "SCRIPT_DIR=%~dp0"
set "XML_FILE=%SCRIPT_DIR%ahu_eportal_task.xml"

echo Registering scheduled task from: %XML_FILE%

:: Register the task using the XML file
schtasks /create /xml "%XML_FILE%" /tn "AHU_Campus_Network_Auto_Login"

if %errorlevel% equ 0 (
    echo Task successfully registered.
    echo Task name: AHU_Campus_Network_Auto_Login
    echo Task will be triggered when connecting to any network.
    exit /b 0
) else (
    echo Failed to register task. Error code: %errorlevel%
    exit /b 1
) 