@echo off
echo === Adding test framework to skills ===
cd /d %~dp0

set added=0
for /d %%D in (skills\*) do (
    if not exist "%%D\test" (
        mkdir "%%D\test"
        (
            echo # Test for %%~nD
echo.
echo ## Setup
echo.
echo ```bash
echo # Install dependencies if needed
echo ```
echo.
echo ## Test Cases
echo.
echo ### Test 1: Basic functionality
echo ```
echo Input: [test input]
echo Expected: [expected output]
echo ```
echo.
echo ### Test 2: Edge case
echo ```
echo Input: [edge case input]
echo Expected: [expected output]
echo ```
echo.
echo ## Running Tests
echo.
echo ```bash
echo # Run all tests
echo ./run_tests.sh
echo ```
        ) > "%%D\test\README.md"
        set /a added+=1
        echo Added test framework to: %%D
    )
)

echo.
echo Added test framework to %added% skills
echo === Done ===
pause
