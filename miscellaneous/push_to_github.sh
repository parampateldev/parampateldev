#!/bin/bash

# Script to initialize git repos and push all projects to GitHub
# Run this from /Users/parampatel/parampatel-dev/

echo "🚀 Starting GitHub repository creation and push process..."

# List of all projects
projects=(
    "quantum-ml-optimizer"
    "carbon-credits-ai" 
    "ai-trading-bot"
    "defi-yield-optimizer"
    "ai-code-review"
    "smart-contract-scanner"
    "iot-edge-platform"
    "fraud-detection-system"
    "agriculture-ai"
    "energy-optimization"
    "robotics-automation"
    "space-exploration"
    "metaverse-platform"
)

# GitHub username
GITHUB_USER="parampateldev"

for project in "${projects[@]}"; do
    echo ""
    echo "📁 Processing project: $project"
    
    if [ -d "$project" ]; then
        cd "$project"
        
        # Initialize git repository
        git init
        
        # Add all files
        git add .
        
        # Create initial commit
        git commit -m "Initial commit: $project - Advanced platform with AI/ML capabilities
        
        Features:
        - Backend API with Flask
        - Frontend with dark theme UI
        - Comprehensive functionality
        - Professional documentation
        
        Tech Stack: Python, Flask, HTML, CSS, JavaScript
        Author: Param Patel 2025"
        
        # Create GitHub repository (this will require GitHub CLI or manual creation)
        echo "📝 Note: You'll need to manually create the repository on GitHub:"
        echo "   Repository name: $project"
        echo "   Description: Advanced $project platform with AI/ML capabilities"
        echo "   Visibility: Private"
        echo ""
        echo "Then run these commands in the $project directory:"
        echo "   git remote add origin https://github.com/$GITHUB_USER/$project.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo ""
        
        cd ..
    else
        echo "❌ Project directory $project not found"
    fi
done

echo ""
echo "✅ Git repositories initialized for all projects!"
echo ""
echo "🔗 Next steps:"
echo "1. Create repositories on GitHub.com for each project"
echo "2. Run the git remote and push commands for each project"
echo "3. All projects will be available at: https://github.com/$GITHUB_USER/[project-name]"
echo ""
echo "📋 Project list:"
for project in "${projects[@]}"; do
    echo "   - $project"
done

