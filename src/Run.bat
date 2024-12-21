@echo off
set script=main.py

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not found in the PATH. Please ensure Python is installed and added to the system PATH.
    pause
    exit /b
)


echo Running %script%...
python %script%
if %errorlevel% neq 0 (
    echo An error occurred while running %script%.
    pause
    exit /b
)

echo Script %script% finished successfully.
pause
