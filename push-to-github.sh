#!/bin/bash

cd /Users/parampatel/parampatel-dev

echo "=== Checking for changes ==="
git status

echo ""
echo "=== Staging all changes ==="
git add -A

echo ""
echo "=== Committing changes ==="
git commit -m "Update portfolio: navbar always visible, improved transitions"

echo ""
echo "=== Pushing to GitHub (this will prompt for password) ==="
git push origin main

echo ""
echo "=== Push complete! ==="
echo "Check your GitHub Actions at: https://github.com/parampateldev/parampateldev/actions"
echo "You should see 'pages build and deployment' workflow running"
