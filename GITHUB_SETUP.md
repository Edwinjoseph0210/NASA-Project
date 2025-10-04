# 🚀 GitHub Setup Guide

This guide will help you upload your Air Quality Monitor project to GitHub.

## 📋 Prerequisites

- Git installed on your computer
- GitHub account created
- Repository created on GitHub

---

## 🔧 Step-by-Step Setup

### 1. Initialize Git Repository (if not already done)

```bash
cd /Users/apple/Downloads/NASA

# Initialize git repository
git init

# Check git status
git status
```

### 2. Configure Git (First Time Only)

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### 3. Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific files/folders
git add README.md
git add dashboard-tempo.html
git add backend/
git add frontend/

# Check what will be committed
git status
```

### 4. Create Initial Commit

```bash
# Commit with a message
git commit -m "Initial commit: Air Quality Monitor with NASA TEMPO and Ambee API integration"

# Verify commit
git log
```

### 5. Connect to GitHub Repository

Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` with your actual values:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git

# Verify remote
git remote -v
```

### 6. Push to GitHub

```bash
# Push to main branch
git push -u origin main

# If your default branch is 'master', use:
# git push -u origin master
```

If you get an error about the branch name, rename it:

```bash
# Rename branch to main
git branch -M main

# Then push
git push -u origin main
```

---

## 🔐 Handling Sensitive Data

### Important: Remove Sensitive Information

Before pushing, make sure to:

1. **Remove API keys from code**
   - Edit `dashboard-tempo.html` and replace the Ambee API key with a placeholder
   - Use environment variables instead

2. **Check .env file**
   - Ensure `.env` is in `.gitignore`
   - Only commit `.env.example` with placeholder values

3. **Review files**
   ```bash
   # Search for potential secrets
   grep -r "api_key" .
   grep -r "password" .
   grep -r "secret" .
   ```

### Update dashboard-tempo.html

Replace the hardcoded API key:

```javascript
// Before (DON'T COMMIT THIS)
const AMBEE_API_KEY = '4f48fce9355b2d578b9cddf8c969494f88292c50c8180568f48794fb09af0555';

// After (SAFE TO COMMIT)
const AMBEE_API_KEY = process.env.AMBEE_API_KEY || 'your-api-key-here';
```

---

## 📦 What Gets Uploaded

Based on `.gitignore`, these files/folders will be **included**:

✅ **Source Code**
- `dashboard-tempo.html`
- `dashboard.html`
- `dashboard-modern.html`
- `backend/` (Python code)
- `frontend/` (React/Next.js code)

✅ **Configuration**
- `docker-compose.yml`
- `Dockerfile.backend`
- `Dockerfile.frontend`
- `requirements.txt`
- `package.json`
- `.env.example` (template only)

✅ **Documentation**
- `README.md`
- `API_DOCUMENTATION.md`
- `DEPLOYMENT.md`
- All other `.md` files

✅ **Scripts**
- `start.sh`
- `start-tempo.sh`
- `start-kerala.sh`

❌ **Excluded** (in .gitignore)
- `venv/`, `node_modules/`
- `.env` (contains secrets)
- `__pycache__/`
- `.DS_Store`
- Database files
- Log files

---

## 🌿 Branch Strategy (Optional)

### Create Development Branch

```bash
# Create and switch to dev branch
git checkout -b dev

# Make changes, then commit
git add .
git commit -m "Add new feature"

# Push dev branch
git push origin dev
```

### Merge to Main

```bash
# Switch to main
git checkout main

# Merge dev into main
git merge dev

# Push to GitHub
git push origin main
```

---

## 🔄 Regular Updates

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Update: Add animated particles to dashboard"

# Push to GitHub
git push origin main
```

---

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add: Ambee API integration for real-time data"
git commit -m "Fix: Map initialization timing issue"
git commit -m "Update: Improve dashboard animations"
git commit -m "Docs: Update README with setup instructions"

# Bad examples (avoid these)
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### Commit Types

- `Add:` - New features
- `Fix:` - Bug fixes
- `Update:` - Improvements to existing features
- `Docs:` - Documentation changes
- `Style:` - Code formatting, no logic changes
- `Refactor:` - Code restructuring
- `Test:` - Adding or updating tests

---

## 🛠️ Troubleshooting

### Issue: Large files rejected

```bash
# Error: file is too large
# Solution: Add to .gitignore or use Git LFS

# Add large file to .gitignore
echo "large-file.zip" >> .gitignore

# Or use Git LFS
git lfs install
git lfs track "*.zip"
```

### Issue: Authentication failed

```bash
# Use personal access token instead of password
# 1. Go to GitHub Settings > Developer settings > Personal access tokens
# 2. Generate new token
# 3. Use token as password when pushing
```

### Issue: Merge conflicts

```bash
# Pull latest changes first
git pull origin main

# Resolve conflicts in files
# Then commit
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### Issue: Accidentally committed secrets

```bash
# Remove file from git history
git rm --cached .env
git commit -m "Remove .env from tracking"

# Change all exposed secrets immediately!
# Then push
git push origin main
```

---

## 📊 GitHub Repository Settings

### After Pushing

1. **Add Repository Description**
   - Go to your GitHub repo
   - Click "Edit" next to About
   - Add: "Real-time air quality monitoring dashboard with NASA TEMPO and Ambee API"
   - Add topics: `air-quality`, `nasa-tempo`, `ambee-api`, `fastapi`, `leaflet`, `dashboard`

2. **Enable GitHub Pages** (Optional)
   - Settings > Pages
   - Source: Deploy from branch
   - Branch: main, folder: / (root)
   - Your dashboard will be live at: `https://username.github.io/repo-name/dashboard-tempo.html`

3. **Add Topics/Tags**
   ```
   air-quality, nasa, tempo, satellite-data, ambee-api, 
   fastapi, python, javascript, leaflet, maps, 
   environmental-monitoring, pollution, dashboard
   ```

4. **Set Repository Visibility**
   - Public: Anyone can see
   - Private: Only you and collaborators

---

## 🎯 Quick Reference

```bash
# Common Git commands
git status              # Check status
git add .               # Stage all changes
git commit -m "msg"     # Commit changes
git push                # Push to GitHub
git pull                # Pull from GitHub
git log                 # View commit history
git branch              # List branches
git checkout -b name    # Create new branch

# Undo changes
git checkout -- file    # Discard changes in file
git reset HEAD file     # Unstage file
git reset --soft HEAD~1 # Undo last commit (keep changes)
git reset --hard HEAD~1 # Undo last commit (discard changes)
```

---

## ✅ Final Checklist

Before pushing to GitHub:

- [ ] `.gitignore` file is present
- [ ] `.env` is in `.gitignore`
- [ ] API keys are removed or replaced with placeholders
- [ ] `README.md` is complete and accurate
- [ ] All sensitive data is excluded
- [ ] Code is tested and working
- [ ] Commit messages are clear
- [ ] Repository description is added
- [ ] License file is included (if applicable)

---

## 🎉 You're Done!

Your project is now on GitHub! Share the link:

```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

### Next Steps

1. Add a LICENSE file
2. Create GitHub Issues for future features
3. Set up GitHub Actions for CI/CD (optional)
4. Add screenshots to README
5. Create a demo video

---

## 📧 Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/docs/gittutorial
- GitHub Support: https://support.github.com

Happy coding! 🚀
