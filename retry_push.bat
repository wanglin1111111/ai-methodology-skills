@echo off
echo === Git Push Retry Script ===
echo.
echo This script will retry push up to 5 times
echo.

cd /d "%~dp0"

set /a count=1
:retry
echo Attempt %count%/5...

git push origin main

if %errorlevel% == 0 (
    echo.
    echo SUCCESS! Push completed.
    goto :end
)

if %count% == 5 (
    echo.
    echo FAILED after 5 attempts.
    echo Please check network connection and retry manually.
    goto :end
)

echo Failed. Retrying in 30 seconds...
timeout /t 30 /nobreak >nul

set /a count+=1
goto :retry

:end
echo.
pause
