@echo off

setlocal EnableExtensions



title PyTune Box - Create Release ZIP



REM Move to project root

cd /d "%~dp0\.."

echo Project root: %CD%

echo.



echo ============================================================

echo PyTune Box - Create Release ZIP

echo ============================================================

echo.



if not exist "dist\PyTuneBox\PyTuneBox.exe" (

    echo Please run build_windows_exe.bat first.

    echo Expected file not found: dist\PyTuneBox\PyTuneBox.exe

    echo.

    pause

    exit /b 1

)



set "RELEASE_NAME=PyTuneBox-v0.1.0-beta"

set "RELEASE_DIR=releases\%RELEASE_NAME%"

set "RELEASE_ZIP=releases\%RELEASE_NAME%.zip"



if not exist "releases" mkdir "releases"



if exist "%RELEASE_DIR%" rd /s /q "%RELEASE_DIR%"

mkdir "%RELEASE_DIR%"



echo Copying packaged application...

xcopy "dist\PyTuneBox\*" "%RELEASE_DIR%\" /E /I /Y >nul



echo Copying release documents...

copy /Y "README.md" "%RELEASE_DIR%\" >nul

copy /Y "RELEASE_NOTES.md" "%RELEASE_DIR%\" >nul

copy /Y "PACKAGING_GUIDE.md" "%RELEASE_DIR%\" >nul

copy /Y "VERSION.txt" "%RELEASE_DIR%\" >nul

copy /Y "TESTING_CHECKLIST.md" "%RELEASE_DIR%\" >nul



if exist "%RELEASE_ZIP%" del /f /q "%RELEASE_ZIP%"



echo Creating ZIP archive...

powershell -NoProfile -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%RELEASE_ZIP%' -Force"



if errorlevel 1 (

    echo.

    echo Failed to create release ZIP.

    echo.

    pause

    exit /b 1

)



if not exist "%RELEASE_ZIP%" (

    echo.

    echo Failed to create release ZIP.

    echo.

    pause

    exit /b 1

)



echo.

echo Release package created successfully.

echo Release folder: %RELEASE_DIR%

echo Release ZIP: %RELEASE_ZIP%

echo.

pause

exit /b 0

