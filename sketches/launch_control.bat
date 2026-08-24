@echo off
rem file: launch_control.bat
rem Launch the Minifig Pi Web Controller using a local Python HTTP server

set PORT=8000
echo [*] Starting local web server on http://localhost:%PORT%...
start /B python -m http.server %PORT% --directory "%~dp0" >nul 2>&1

echo [*] Opening Web Controller in your browser...
start "" "http://localhost:%PORT%/web_control.html"
