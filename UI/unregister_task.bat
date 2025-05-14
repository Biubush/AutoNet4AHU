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

echo Unregistering scheduled task: AHU_Campus_Network_Auto_Login

:: Delete the task
schtasks /delete /tn "AHU_Campus_Network_Auto_Login" /f

if %errorlevel% equ 0 (
    echo Task successfully unregistered.
    echo Task name: AHU_Campus_Network_Auto_Login
    exit /b 0
) else (
    echo Failed to unregister task. Error code: %errorlevel%
    echo Note: This may occur if the task does not exist.
    exit /b 1
) 