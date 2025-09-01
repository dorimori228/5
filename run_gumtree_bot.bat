@echo off
title Gumtree Auto Lister Bot
color 0A

echo.
echo ========================================
echo    Gumtree Auto Lister Bot
echo ========================================
echo.
echo Starting the improved Gumtree bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "run_improved_bot.py" (
    echo ERROR: run_improved_bot.py not found
    echo Please make sure all files are in the same directory
    pause
    exit /b 1
)

if not exist "gumtree_bot.py" (
    echo ERROR: gumtree_bot.py not found
    echo Please make sure all files are in the same directory
    pause
    exit /b 1
)

if not exist "listing_config.json" (
    echo WARNING: listing_config.json not found
    echo Creating a sample configuration file...
    echo.
    echo {> listing_config.json
    echo     "title": "Sample Item Title",>> listing_config.json
    echo     "description": "This is a sample description for your item. Please edit this file with your actual listing details.",>> listing_config.json
    echo     "price": "50",>> listing_config.json
    echo     "category_search": "artificial grass",>> listing_config.json
    echo     "image_path": "path/to/your/image.jpg">> listing_config.json
    echo }>> listing_config.json
    echo.
    echo Sample configuration created. Please edit listing_config.json with your details.
    echo.
    pause
)

REM Check if Chrome is installed
where chrome >nul 2>&1
if errorlevel 1 (
    where "C:\Program Files\Google\Chrome\Application\chrome.exe" >nul 2>&1
    if errorlevel 1 (
        where "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" >nul 2>&1
        if errorlevel 1 (
            echo WARNING: Chrome browser not found in standard locations
            echo The bot will try to use ChromeDriver anyway
            echo.
        )
    )
)

REM Install required packages if needed
echo Checking Python dependencies...
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install selenium
    if errorlevel 1 (
        echo ERROR: Failed to install selenium
        echo Please install it manually: pip install selenium
        pause
        exit /b 1
    )
)

echo.
echo All checks passed! Starting the bot...
echo.
echo ========================================
echo.

REM Run the bot
python run_improved_bot.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo Bot encountered an error
    echo ========================================
    echo.
) else (
    echo.
    echo ========================================
    echo Bot completed successfully
    echo ========================================
    echo.
)

echo Press any key to exit...
pause >nul
