@echo off
setlocal EnableExtensions

title PyTune Box - Windows EXE Build

REM Move to project root (parent of build_scripts)
cd /d "%~dp0\.."
echo Project root: %CD%
echo.

echo ============================================================
echo PyTune Box - Windows EXE Build
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not available in PATH.
    echo Please install Python 3.10 or newer and try again.
    echo.
    pause
    exit /b 1
)

echo Python found.
python --version
echo.

REM Check / install PyInstaller via requirements.txt
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing project requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements.
        echo.
        pause
        exit /b 1
    )
) else (
    echo PyInstaller is available.
)

echo.
echo Cleaning old build output...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "PyTuneBox.spec" del /f /q "PyTuneBox.spec"

echo.
echo Starting PyInstaller build...
echo.

set "WORKPATH=%TEMP%\PyTuneBox-build"

if exist "assets\icons\app.ico" (
    echo Using icon: assets\icons\app.ico
    pyinstaller --noconfirm --clean --windowed --noupx --workpath "%WORKPATH%" --distpath "dist" --name "PyTuneBox" --add-data "data;data" --add-data "assets;assets" --icon "assets\icons\app.ico" main.py
) else (
    echo No app.ico found. Building without custom icon.
    pyinstaller --noconfirm --clean --windowed --noupx --workpath "%WORKPATH%" --distpath "dist" --name "PyTuneBox" --add-data "data;data" --add-data "assets;assets" main.py
)

if errorlevel 1 (
    echo.
    echo Build failed. Please check the error messages above.
    echo.
    pause
    exit /b 1
)

if not exist "dist\PyTuneBox\PyTuneBox.exe" (
    echo.
    echo Build failed. Please check the error messages above.
    echo Expected file not found: dist\PyTuneBox\PyTuneBox.exe
    echo.
    pause
    exit /b 1
)

echo.
echo Build completed successfully.
echo Output folder: dist\PyTuneBox
echo Executable: dist\PyTuneBox\PyTuneBox.exe
echo.
pause
exit /b 0
