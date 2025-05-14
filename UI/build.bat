@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 开始编译UI模块...

REM 指定输出目录和文件名
set "OUTPUT_DIR=..\dist"
set "OUTPUT_NAME=AutoNet4AHU"
set "MAIN_DIR=.."

REM 使用Nuitka编译
python -m nuitka --standalone ^
  --windows-console-mode=disable ^
  --enable-plugin=pyside6 ^
  --output-filename="AutoNet4AHU.exe" ^
  --windows-company-name="biubush" ^
  --windows-product-name="AutoNet4AHU" ^
  --windows-file-description="This Campus Network Auto-Login Program is specifically designed for students and staff at Anhui University (AHU) to automatically log in to the campus network. It aims to streamline the process of accessing the internet by eliminating the need for manual login each time the network connection changes." ^
  --windows-icon-from-ico=icon.ico ^
  --copyright="Copyright 2025 biubush" ^
  --output-dir=%OUTPUT_DIR% ui.py

REM 移动并重命名ui.dist文件夹
echo 正在移动并重命名编译后的文件夹...
if exist "%OUTPUT_DIR%\ui.dist" (
  if exist "%MAIN_DIR%\%OUTPUT_NAME%" (
    rmdir /s /q "%MAIN_DIR%\%OUTPUT_NAME%"
    echo 已删除旧的 %OUTPUT_NAME% 文件夹
  )
  move "%OUTPUT_DIR%\ui.dist" "%MAIN_DIR%\%OUTPUT_NAME%"
  echo 已将 ui.dist 移动并重命名为 %OUTPUT_NAME%
)

REM 复制所需文件到输出文件夹
echo 正在复制所需文件...
xcopy "task_template.xml" "%MAIN_DIR%\%OUTPUT_NAME%\" /y
xcopy "register_task.bat" "%MAIN_DIR%\%OUTPUT_NAME%\" /y
xcopy "unregister_task.bat" "%MAIN_DIR%\%OUTPUT_NAME%\" /y
xcopy "login.exe" "%MAIN_DIR%\%OUTPUT_NAME%\" /y
xcopy "ahu_eportal.vbs" "%MAIN_DIR%\%OUTPUT_NAME%\" /y

REM 创建ZIP压缩包
echo 正在创建ZIP压缩包...
cd %MAIN_DIR%
powershell -command "Compress-Archive -Path '%OUTPUT_NAME%' -DestinationPath '%OUTPUT_NAME%.zip' -Force"
echo 已创建 %OUTPUT_NAME%.zip

REM 清理整个dist文件夹
echo 正在清理dist文件夹...
if exist "dist" (
  rmdir /s /q "dist"
  echo 已删除 dist 文件夹
)

echo UI模块编译完成！

pause 