@echo off
echo === Setting up Quarterly Review Cron Job ===
echo.
echo This script will create a cron job to run quarterly skill reviews
echo.

REM Create the review script
echo Creating review script...
(
echo #!/bin/bash
echo cd "$(dirname "$0")"
echo echo "Running Quarterly Skill Review..."
echo echo "Date: $(date)"
echo.
echo # Count skills
echo SKILL_COUNT=$(ls -1 skills/ 2^>/dev/null ^| wc -l)
echo echo "Total skills: $SKILL_COUNT"
echo.
echo # Check for test directories
echo WITH_TEST=$(find skills/ -name "test_cases.md" 2^>/dev/null ^| wc -l)
echo echo "Skills with tests: $WITH_TEST"
echo.
echo # Check for example directories  
echo WITH_EXAMPLE=$(find skills/ -name "real_world_examples.md" 2^>/dev/null ^| wc -l)
echo echo "Skills with examples: $WITH_EXAMPLE"
echo.
echo # Generate report
echo REPORT_FILE="QUARTERLY_REVIEW_$(date +%%Y%%m%%d).md"
echo echo "# Quarterly Review $(date +%%Y-%%m-%%d)" ^> "$REPORT_FILE"
echo echo "" ^>^> "$REPORT_FILE"
echo echo "## Summary" ^>^> "$REPORT_FILE"
echo echo "- Total skills: $SKILL_COUNT" ^>^> "$REPORT_FILE"
echo echo "- With tests: $WITH_TEST" ^>^> "$REPORT_FILE"
echo echo "- With examples: $WITH_EXAMPLE" ^>^> "$REPORT_FILE"
echo.
echo echo "Report saved: $REPORT_FILE"
) > quarterly_review.sh

echo.
echo To schedule this review, add to your crontab:
echo.
echo # Quarterly review (last day of quarter)
echo 0 9 31 3,6,9,12 * cd /path/to/repo ^&^& bash quarterly_review.sh
echo.
echo Or manually run: bash quarterly_review.sh
echo.
pause
