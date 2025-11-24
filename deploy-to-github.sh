#!/bin/bash
set -e

cd /Users/parampatel/parampatel-dev

echo "🔧 Setting correct remote repository..."
git remote set-url origin https://github.com/parampateldev/parampateldev.git

echo "📋 Current remote:"
git remote -v

echo ""
echo "📦 Staging all changes..."
git add -A

echo ""
echo "📝 Current status:"
git status --short

echo ""
echo "💾 Committing changes..."
git commit -m "Deploy portfolio to parampatel.dev: monospace font hero section, all website files" || echo "No changes to commit"

echo ""
echo "🚀 Pushing to github.com/parampateldev/parampateldev..."
git push -u origin main 2>&1 || git push -u origin master 2>&1 || git push 2>&1

echo ""
echo "✅ Pushed to GitHub! Your site should be live at parampatel.dev shortly."


