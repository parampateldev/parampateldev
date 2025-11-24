#!/usr/bin/env python3
import subprocess
import webbrowser
import time
import os
import sys

PORT = 8000

# Change to parent directory so both website/ and projects/ are accessible
os.chdir('/Users/parampatel/parampatel-dev')

# Kill any existing server on port 8000
try:
    subprocess.run(['lsof', '-ti:8000'], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(['lsof', '-ti:8000'], stdout=subprocess.PIPE).stdout.decode().strip()
    subprocess.run(['kill', '-9', subprocess.run(['lsof', '-ti:8000'], stdout=subprocess.PIPE).stdout.decode().strip()], 
                   check=False, stderr=subprocess.DEVNULL)
except:
    pass

# Wait a moment for port to be released
time.sleep(1)

print("Starting live-reload server...")
print("Server will auto-reload when you make changes to files!")

# Start live-server with auto-reload
# live-server automatically watches for file changes and reloads the browser
process = subprocess.Popen(
    ['npx', '--yes', 'live-server', '--port=8000', '--open=/website/', '--watch=website'],
    cwd='/Users/parampatel/parampatel-dev'
)

# Wait a moment for server to start
time.sleep(3)

# Open browser
print("Opening browser...")
webbrowser.open(f'http://localhost:{PORT}/website/')

print("\n✅ Live-reload server is running!")
print("📝 Edit your files and they will auto-reload in the browser")
print("🛑 Press Ctrl+C to stop the server\n")

# Keep script running
try:
    process.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down server...")
    process.terminate()
    process.wait()
    sys.exit(0)

