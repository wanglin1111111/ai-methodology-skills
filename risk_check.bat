@echo off
echo === Risk Scan Report ===
echo.
echo [1/5] Checking skill count...
cd /d %~dp0
for /f %%a in ('dir /b skills\* 2^>nul ^| find /c /v ""') do set skillcount=%%a
echo Found %skillcount% skills

if %skillcount% gtr 70 (
    echo WARNING: High skill count may indicate over-segmentation
    echo Suggestion: Review for potential merges
)

echo.
echo [2/5] Checking version format (sample 10)...
set version_issues=0
for /d %%D in (skills\*) do (
    if exist "%%D\metadata.json" (
        findstr /C:"\"version\":" "%%D\metadata.json" >nul
        if errorlevel 1 (
            echo %%D: missing version field
            set /a version_issues+=1
        )
    ) else (
        echo %%D: missing metadata.json
        set /a version_issues+=1
    )
)
echo Version issues found: %version_issues%

echo.
echo [3/5] Checking for test directories...
set no_test=0
for /d %%D in (skills\*) do (
    if not exist "%%D\test" (
        set /a no_test+=1
    )
)
echo Skills without test/: %no_test%

echo.
echo [4/5] Checking for example directories...
set no_example=0
for /d %%D in (skills\*) do (
    if not exist "%%D\example" (
        set /a no_example+=1
    )
)
echo Skills without example/: %no_example%

echo.
echo [5/5] Checking SKILL.md files...
set no_skill_md=0
for /d %%D in (skills\*) do (
    if not exist "%%D\SKILL.md" (
        echo %%D: missing SKILL.md
        set /a no_skill_md+=1
    )
)
echo Skills without SKILL.md: %no_skill_md%

echo.
echo === Risk Summary ===
echo High risk: Test coverage (%no_test%/%skillcount% skills lack tests)
echo Medium risk: Example coverage (%no_example%/%skillcount% skills lack examples)
if %version_issues% gtr 0 echo Medium risk: Version issues (%version_issues% found)
if %no_skill_md% gtr 0 echo High risk: Missing SKILL.md (%no_skill_md% found)

echo.
echo === Recommendations ===
echo 1. Add test/ directories to all skills
echo 2. Add example/ directories to all skills
echo 3. Ensure all metadata.json have valid version fields
echo 4. Create cross-link validation script

echo.
pause
