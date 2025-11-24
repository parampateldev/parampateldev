#!/bin/bash
set -e

cd /Users/parampatel/parampatel-dev

echo "=== Git Configuration ==="
echo "Remote URL:"
git remote get-url origin
echo ""
echo "Current branch:"
git branch --show-current
echo ""

echo "=== Checking authentication ==="
echo "Testing connection to GitHub..."
if git ls-remote origin HEAD &>/dev/null; then
    echo "✅ Authentication successful - credentials are cached"
else
    echo "❌ Authentication failed - will prompt for credentials"
fi
echo ""

echo "=== Staging and committing ==="
git add -A
git status --short
echo ""

echo "=== Committing ==="
git commit -m "Deploy portfolio to parampatel.dev: monospace font hero section" || echo "No changes to commit"
echo ""

echo "=== Pushing to GitHub ==="
echo "This should prompt for credentials if not cached..."
git push -u origin main 2>&1 || {
    echo ""
    echo "Push failed. Trying with explicit authentication..."
    echo "You may need to enter your GitHub credentials."
    git push https://github.com/parampateldev/parampateldev.git main
}

echo ""
echo "=== Done ==="

