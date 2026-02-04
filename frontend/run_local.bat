@echo off
cd /d "%~dp0"

echo Checking for local Node runtime...
if exist "..\node_runtime\node-v18.20.5-win-x64\node.exe" (
    echo Found local Node runtime.
    set "PATH=%~dp0..\node_runtime\node-v18.20.5-win-x64;%PATH%"
) else (
    echo Local Node runtime not found, assuming global installation.
)

echo Installing dependencies...
call npm install

echo Starting Frontend...
echo The frontend will be available at http://localhost:3000
npm run dev

pause
