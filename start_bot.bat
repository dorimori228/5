@echo off
title Gumtree Bot Launcher
color 0B

echo.
echo  ██████╗ ██╗   ██╗███╗   ███╗████████╗██████╗ ██╗███████╗███████╗
echo ██╔════╝ ██║   ██║████╗ ████║╚══██╔══╝██╔══██╗██║██╔════╝██╔════╝
echo ██║  ███╗██║   ██║██╔████╔██║   ██║   ██████╔╝██║█████╗  █████╗  
echo ██║   ██║██║   ██║██║╚██╔╝██║   ██║   ██╔══██╗██║██╔══╝  ██╔══╝  
echo ╚██████╔╝╚██████╔╝██║ ╚═╝ ██║   ██║   ██║  ██║██║███████╗███████╗
echo  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
echo.
echo                    Auto Lister Bot v2.0
echo.
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "gumtree_bot.py" (
    echo ERROR: Please run this from the bot directory
    echo Make sure gumtree_bot.py is in the same folder
    pause
    exit /b 1
)

echo Choose an option:
echo.
echo 1. Run Gumtree Bot (Main)
echo 2. Test Cookie Persistence
echo 3. Test Anti-Detection
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Gumtree Bot...
    call run_gumtree_bot.bat
) else if "%choice%"=="2" (
    echo.
    echo Starting Cookie Test...
    python test_cookie_fixes.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting Anti-Detection Test...
    python test_anti_detection.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)
