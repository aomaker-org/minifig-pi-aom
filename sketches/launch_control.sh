#!/bin/sh
# file: launch_control.sh
# Launch the Minifig Pi Web Controller using a local Python HTTP server

DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8000

cleanup() {
    echo ""
    echo "[*] Stopping local web server..."
    kill $SERVER_PID 2>/dev/null
    exit
}

# Trap exit signals to clean up the python server
trap cleanup EXIT INT TERM

echo "[*] Starting local web server on http://localhost:$PORT..."
python3 -m http.server $PORT --directory "$DIR" >/dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to bind
sleep 1

echo "[*] Opening Web Controller in your browser..."
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:$PORT/web_control.html"
elif command -v open >/dev/null 2>&1; then
    open "http://localhost:$PORT/web_control.html"
else
    echo "[!] Could not auto-launch browser. Please visit http://localhost:$PORT/web_control.html manually."
fi

# Keep script running to keep server alive
echo "[*] Web server running (PID: $SERVER_PID). Press Ctrl+C to stop."
wait $SERVER_PID
