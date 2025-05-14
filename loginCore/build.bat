@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 开始编译登录核心模块...

REM 指定输出目录和文件名
set "OUTPUT_DIR=..\UI"
set "OUTPUT_FILE=login.exe"

REM 使用Nuitka编译
python -m nuitka --standalone ^
  --onefile ^
  --follow-imports ^
  --include-package=requests ^
  --windows-console-mode=disable ^
  --output-dir=%OUTPUT_DIR% ^
  --output-filename=%OUTPUT_FILE% ^
  main.py

REM 删除临时文件夹
echo 清理临时文件...
if exist "%OUTPUT_DIR%/main.build" (
  rmdir /s /q "%OUTPUT_DIR%/main.build"
  echo 已删除 main.build 文件夹
)

if exist "%OUTPUT_DIR%/main.dist" (
  rmdir /s /q "%OUTPUT_DIR%/main.dist"
  echo 已删除 main.dist 文件夹
)

if exist "%OUTPUT_DIR%/main.onefile-build" (
  rmdir /s /q "%OUTPUT_DIR%/main.onefile-build"
  echo 已删除 main.onefile-build 文件夹
)

echo 登录核心模块编译完成！输出文件: %OUTPUT_DIR%\%OUTPUT_FILE%

pause