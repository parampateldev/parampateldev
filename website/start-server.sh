#!/bin/bash
# Change to parent directory so both website/ and projects/ are accessible
cd "$(dirname "$0")/.."
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 1
echo "Starting live-reload server with auto-refresh..."
npx --yes live-server --port=8000 --open=/website/ --watch=website &
sleep 3
open http://localhost:8000/website/
echo "✅ Live-reload server running! Changes will auto-update in browser."
wait

