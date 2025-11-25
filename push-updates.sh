#!/bin/bash
cd /Users/parampatel/parampatel-dev

echo "=== Checking git status ==="
git status

echo ""
echo "=== Staging all changes ==="
git add -A

echo ""
echo "=== Committing changes ==="
git commit -m "Update portfolio: fix navbar visibility, improve transitions, better section spacing"

echo ""
echo "=== Pushing to GitHub ==="
git push origin main

echo ""
echo "=== Push complete! ==="
echo "Check your repo at: https://github.com/parampateldev/parampateldev"
echo "Your site should update at parampatel.dev within 1-2 minutes"

