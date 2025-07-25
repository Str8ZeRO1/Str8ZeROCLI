# Simple script to fix branches
Write-Host "`n🔄 Fixing branches..." -ForegroundColor Yellow

# Push local master changes first
Write-Host "Pushing master branch..." -ForegroundColor Cyan
git checkout master
git push

# Force pull main branch
Write-Host "Pulling main branch..." -ForegroundColor Cyan
git fetch origin main
git checkout main || git checkout -b main
git reset --hard origin/main
git pull origin main

# Merge master into main
Write-Host "Merging master into main..." -ForegroundColor Cyan
git merge master --allow-unrelated-histories

# Push changes
Write-Host "Pushing changes..." -ForegroundColor Cyan
git push origin main

Write-Host "`n✅ Branches fixed." -ForegroundColor Green