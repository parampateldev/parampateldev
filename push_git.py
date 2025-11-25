#!/usr/bin/env python3
import subprocess
import os
import sys

os.chdir('/Users/parampatel/parampatel-dev')

print("=== Staging changes ===")
result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n=== Committing ===")
result = subprocess.run(['git', 'commit', '-m', 'Update portfolio: navbar always visible, improved transitions'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Return code:", result.returncode)

print("\n=== Pushing to GitHub ===")
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print("STDOUT:", result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("\n✅ Push successful!")
else:
    print("\n❌ Push failed. Check error above.")

