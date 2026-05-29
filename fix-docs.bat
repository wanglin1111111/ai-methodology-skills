@echo off
echo === Fixing document quality issues ===
cd /d %~dp0

set fixed=0
for /d %%D in (skills\*) do (
    set "skillMd=%%D\SKILL.md"
    if exist "!skillMd!" (
        echo Checking: %%D
        
        REM Check if file starts with ---
        findstr /B "---" "!skillMd!" >nul
        if errorlevel 1 (
            echo   Adding YAML frontmatter to %%D
            (
                echo ---
                echo name: %%~nD
                echo version: 1.0.0
                echo description: "AI skill: %%~nD"
                echo stability: stable
                echo ---
                echo.
                type "!skillMd!"
            ) > "!skillMd!.tmp"
            move /y "!skillMd!.tmp" "!skillMd!" >nul
            set /a fixed+=1
        )
    )
)

echo Fixed %fixed% skill documents
echo === Done ===
