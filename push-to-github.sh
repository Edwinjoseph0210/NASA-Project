#!/bin/bash

# 🚀 Push to GitHub Script
# This script helps you push your Air Quality Monitor project to GitHub

echo "🌍 Air Quality Monitor - GitHub Push Script"
echo "==========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "⚠️  IMPORTANT: Before proceeding, make sure you have:"
echo "   1. Created a repository on GitHub"
echo "   2. Removed all API keys from code"
echo "   3. Reviewed files to commit"
echo ""
read -p "Have you completed the above steps? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Aborted. Please complete the steps first."
    exit 1
fi

echo ""
echo "📝 Checking for sensitive data..."

# Check for potential API keys in dashboard-tempo.html
if grep -q "4f48fce9355b2d578b9cddf8c969494f88292c50c8180568f48794fb09af0555" dashboard-tempo.html 2>/dev/null; then
    echo "⚠️  WARNING: Found hardcoded API key in dashboard-tempo.html"
    echo "   Please replace it with a placeholder before pushing!"
    read -p "Do you want to continue anyway? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ] && [ "$continue_anyway" != "Y" ]; then
        echo "❌ Aborted. Please remove the API key first."
        exit 1
    fi
fi

echo ""
echo "📋 Files to be committed:"
git status --short

echo ""
read -p "Do these files look correct? (y/n): " files_ok

if [ "$files_ok" != "y" ] && [ "$files_ok" != "Y" ]; then
    echo "❌ Aborted. Please review your files."
    exit 1
fi

echo ""
echo "➕ Adding files to Git..."
git add .

echo ""
read -p "Enter commit message: " commit_message

if [ -z "$commit_message" ]; then
    commit_message="Initial commit: Air Quality Monitor"
fi

echo ""
echo "💾 Creating commit..."
git commit -m "$commit_message"

echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Error: Repository URL is required"
    exit 1
fi

echo ""
echo "🔗 Adding remote repository..."
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin "$repo_url"

echo ""
echo "🌿 Checking branch name..."
current_branch=$(git branch --show-current)

if [ -z "$current_branch" ]; then
    echo "Creating main branch..."
    git branch -M main
    current_branch="main"
fi

echo "Current branch: $current_branch"

echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin "$current_branch"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your project is now on GitHub!"
    echo ""
    echo "🎉 Repository URL: ${repo_url%.git}"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Visit your repository on GitHub"
    echo "   2. Add a description and topics"
    echo "   3. Review the README.md"
    echo "   4. Share your project!"
else
    echo ""
    echo "❌ Error: Failed to push to GitHub"
    echo ""
    echo "Common issues:"
    echo "   - Authentication failed: Use personal access token"
    echo "   - Repository doesn't exist: Create it on GitHub first"
    echo "   - Branch mismatch: Check your default branch name"
    echo ""
    echo "See GITHUB_SETUP.md for troubleshooting help"
fi
