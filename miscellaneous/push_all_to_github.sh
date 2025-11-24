#!/bin/bash

# Script to create GitHub repositories and push all projects
# GitHub username: parampateldev

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

echo "📋 Processing ${#projects[@]} projects..."

for project in "${projects[@]}"; do
    echo ""
    echo "📁 Processing project: $project"
    
    if [ -d "$project" ]; then
        cd "$project"
        
        # Create GitHub repository using GitHub CLI
        echo "🔗 Creating GitHub repository: $project"
        gh repo create "$project" \
            --private \
            --description "Advanced $project platform with AI/ML capabilities - Professional full-stack application with backend API, frontend UI, and comprehensive functionality" \
            --source=. \
            --remote=origin \
            --push
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully created and pushed: https://github.com/$GITHUB_USER/$project"
        else
            echo "❌ Failed to create repository for $project"
        fi
        
        cd ..
    else
        echo "❌ Project directory $project not found"
    fi
done

echo ""
echo "🎉 GitHub repository creation and push process completed!"
echo ""
echo "📊 Summary:"
echo "   - Total projects processed: ${#projects[@]}"
echo "   - All repositories are private"
echo "   - All projects pushed to: https://github.com/$GITHUB_USER/"
echo ""
echo "🔗 Your repositories:"
for project in "${projects[@]}"; do
    echo "   - https://github.com/$GITHUB_USER/$project"
done

