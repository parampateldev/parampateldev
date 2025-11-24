#!/bin/bash
# Script to push all changes to GitHub for parampatel.dev

cd "$(dirname "$0")"

echo "🔄 Checking git status..."
git status

echo ""
echo "📦 Staging all changes..."
git add -A

echo ""
echo "💾 Committing changes..."
git commit -m "Update portfolio: monospace font for hero name, live-reload server scripts, and dependency documentation"

echo ""
echo "🚀 Pushing to GitHub (this will update parampatel.dev)..."
git push

echo ""
echo "✅ Done! Changes should be live on parampatel.dev shortly."

