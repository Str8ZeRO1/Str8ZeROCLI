# Str8ZeROCLI Update Script
Write-Host "`n🔄 Updating Str8ZeROCLI installation..." -ForegroundColor Cyan

# 1. Define paths
$installPath = "$env:USERPROFILE\Str8ZeROCLI"
$pythonScript = "$installPath\cli\main.py"

# 2. Check if installation exists
if (!(Test-Path $installPath)) {
    Write-Host "❌ Str8ZeROCLI is not installed. Please run setup-str8zero.ps1 first." -ForegroundColor Red
    exit 1
}

# 3. Update from GitHub
Set-Location $installPath
Write-Host "`n📥 Pulling latest changes from GitHub..." -ForegroundColor Magenta
git pull

# 4. Install/update dependencies
Write-Host "`n📦 Updating dependencies..." -ForegroundColor Magenta
pip install -r "$installPath\requirements.txt"

# 5. Create required directories
Write-Host "`n📁 Creating required directories..." -ForegroundColor Magenta
New-Item -ItemType Directory -Path "$installPath\agents" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\cli\data" -Force | Out-Null

# 6. Update alias if needed
$aliasPath = "$env:USERPROFILE\str8zero-agent.ps1"
@"
python `"$pythonScript`" @args
"@ | Set-Content $aliasPath

# 7. Setup API keys (optional)
$envPath = "$installPath\.env"
if (!(Test-Path $envPath)) {
    @"
# Str8ZeROCLI API Keys
# Uncomment and add your API keys below

# OPENAI_API_KEY=your_openai_api_key
# GEMINI_API_KEY=your_gemini_api_key
# CLAUDE_API_KEY=your_claude_api_key
"@ | Set-Content $envPath
    Write-Host "`n📝 Created .env file for API keys at $envPath" -ForegroundColor Yellow
    Write-Host "   Edit this file to add your API keys for full functionality" -ForegroundColor Yellow
}

# 8. Test the installation
Write-Host "`n🧪 Testing the installation..." -ForegroundColor Cyan
& $aliasPath --list-agents

Write-Host "`n✅ Str8ZeROCLI has been updated successfully!" -ForegroundColor Green
Write-Host "   New features available:" -ForegroundColor Yellow
Write-Host "   - Real agent integration (requires API keys)" -ForegroundColor Yellow
Write-Host "   - Advanced mood detection" -ForegroundColor Yellow
Write-Host "   - Custom agent support (--create-agent, --list-agents)" -ForegroundColor Yellow