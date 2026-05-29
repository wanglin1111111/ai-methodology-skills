@echo off
echo === Creating metadata.json files ===
cd /d %~dp0

for /d %%D in (skills\*) do (
    if not exist "%%D\metadata.json" (
        echo Creating: %%D\metadata.json
        echo {> "%%D\metadata.json"
        echo   "name": "%%~nD",>> "%%D\metadata.json"
        echo   "version": "1.0.0",>> "%%D\metadata.json"
        echo   "description": "AI skill: %%~nD",>> "%%D\metadata.json"
        echo   "author": "wanglin1111111",>> "%%D\metadata.json"
        echo   "tags": ["ai", "skill"],>> "%%D\metadata.json"
        echo   "category": "other",>> "%%D\metadata.json"
        echo   "stability": "stable",>> "%%D\metadata.json"
        echo   "entry": "SKILL.md",>> "%%D\metadata.json"
        echo   "created_at": "2026-05-29",>> "%%D\metadata.json"
        echo   "updated_at": "2026-05-29">> "%%D\metadata.json"
        echo }>> "%%D\metadata.json"
    ) else (
        echo Skipping: %%D\metadata.json (exists)
    )
)

echo === Done ===
pause
