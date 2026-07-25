# Simple one-click script to set up git and push to GitHub
# Usage: .\push_to_github.ps1 <your-github-repo-url>
# Example: .\push_to_github.ps1 https://github.com/yourname/crisisops-novaretail.git

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

Write-Host "🚀 Pushing CrisisOps NovaRetail to GitHub..." -ForegroundColor Green

# Initialize git
Write-Host "1️⃣ Initializing git..." -ForegroundColor Cyan
git init
git add .
git commit -m "CrisisOps NovaRetail AI - ready for Streamlit Cloud"

# Set main branch
Write-Host "2️⃣ Setting branch to main..." -ForegroundColor Cyan
git branch -M main

# Add remote and push
Write-Host "3️⃣ Pushing to GitHub ($RepoUrl)..." -ForegroundColor Cyan
git remote add origin $RepoUrl
git push -u origin main

Write-Host "✅ Done! Your repo is now on GitHub." -ForegroundColor Green
Write-Host "Next: Go to https://share.streamlit.io and create a new app" -ForegroundColor Yellow
