@echo off
echo === Adding example framework to skills ===
cd /d %~dp0

set added=0
for /d %%D in (skills\*) do (
    if not exist "%%D\example" (
        mkdir "%%D\example"
        (
            echo # Example for %%~nD
echo.
echo ## Example 1: Basic Usage
echo.
echo ### Scenario
echo [Describe the scenario]
echo.
echo ### Input
echo ```
echo [Example input]
echo ```
echo.
echo ### Output
echo ```
echo [Expected output]
echo ```
echo.
echo ## Example 2: Advanced Usage
echo.
echo ### Scenario
echo [Describe advanced scenario]
echo.
echo ### Input
echo ```
echo [Advanced example input]
echo ```
echo.
echo ### Output
echo ```
echo [Expected output]
echo ```
echo.
echo ## Running the Example
echo.
echo ```bash
echo # Follow the steps in SKILL.md
echo ```
        ) > "%%D\example\README.md"
        set /a added+=1
        echo Added example framework to: %%D
    )
)

echo.
echo Added example framework to %added% skills
echo === Done ===
pause
