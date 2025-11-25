#!/bin/bash

cd /Users/parampatel/parampatel-dev

echo "=== Git Status ==="
git status

echo ""
echo "=== Remote Configuration ==="
git remote -v

echo ""
echo "=== Current Branch ==="
git branch

echo ""
echo "=== Recent Commits ==="
git log --oneline -3

echo ""
echo "=== Uncommitted Changes ==="
git status --short

echo ""
echo "=== Attempting to push ==="
echo "If you see an error above, here are common fixes:"
echo ""
echo "1. If 'no upstream branch': git push -u origin main"
echo "2. If authentication error: Check your GitHub credentials"
echo "3. If 'nothing to push': All changes are already pushed"
echo "4. If remote error: Verify remote URL is correct"

