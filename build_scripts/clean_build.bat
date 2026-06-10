@echo off

setlocal EnableExtensions



title PyTune Box - Clean Build Artifacts



REM Move to project root

cd /d "%~dp0\.."

echo Project root: %CD%

echo.



echo ============================================================

echo PyTune Box - Clean Build Folders

echo ============================================================

echo.



if exist "build" (

    echo Removing build\

    rd /s /q "build"

)



if exist "dist" (

    echo Removing dist\

    rd /s /q "dist"

)



if exist "PyTuneBox.spec" (

    echo Removing PyTuneBox.spec

    del /f /q "PyTuneBox.spec"

)



if exist "app\__pycache__" (

    echo Removing app\__pycache__

    rd /s /q "app\__pycache__"

)



if exist "tests\__pycache__" (

    echo Removing tests\__pycache__

    rd /s /q "tests\__pycache__"

)



if exist "__pycache__" (

    echo Removing __pycache__

    rd /s /q "__pycache__"

)



echo.

echo Build folders cleaned.

echo Source files, data\settings.json, and data\playlists were not deleted.

echo.

pause

exit /b 0

