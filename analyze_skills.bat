@echo off
echo === Skill Merge Analysis ===
cd /d %~dp0

echo.
echo [1/4] Analyzing ai-era-* series...
echo Found ai-era-* skills:
for /d %%D in (skills\ai-era-*) do (
    echo   - %%~nD
)

echo.
echo [2/4] Analyzing ai-startup-* series...
echo Found ai-startup-* skills:
for /d %%D in (skills\ai-startup-*) do (
    echo   - %%~nD
)

echo.
echo [3/4] Analyzing personal-* series...
echo Found personal-* skills:
for /d %%D in (skills\personal-*) do (
    echo   - %%~nD
)

echo.
echo [4/4] Analyzing ai-* skills (total count)...
set aicount=0
for /d %%D in (skills\ai-*) do (
    set /a aicount+=1
)
echo Total ai-* skills: %aicount%

echo.
echo === Analysis Complete ===
pause
