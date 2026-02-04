@echo off
echo Starting AI Code Reviewer...

echo Starting Backend...
start "AI Code Reviewer - Backend" cmd /c "cd backend && run_local.bat"

echo Starting Frontend...
start "AI Code Reviewer - Frontend" cmd /c "cd frontend && run_local.bat"

echo Application starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Please wait for both windows to initialize.
pause
