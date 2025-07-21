# ⚙️ Enhanced Str8ZeROCLI Installer for Windows PowerShell
Write-Host "`n🚀 Installing Enhanced Str8ZeROCLI..." -ForegroundColor Cyan

# 1. Define repo and paths
$repoUrl = "https://github.com/Str8ZeRO1/Str8ZeROCLI"
$installPath = "$env:USERPROFILE\Str8ZeROCLI"
$pythonScript = "$installPath\cli\main.py"

# 2. Clone the GitHub repo
if (!(Test-Path $installPath)) {
    git clone $repoUrl $installPath
} else {
    Write-Host "📁 Repo already exists at $installPath" -ForegroundColor Yellow
    # Update the repo
    Set-Location $installPath
    git pull
}

# 3. Install Python dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Magenta
pip install -r "$installPath\requirements.txt"

# 4. Create symbolic command alias
$aliasPath = "$env:USERPROFILE\str8zero-agent.ps1"
@"
python `"$pythonScript`" @args
"@ | Set-Content $aliasPath

# Add alias to profile
$profileLine = "Set-Alias str8zero-agent `"$aliasPath`""
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force | Out-Null
}
if (!(Get-Content $PROFILE | Select-String "str8zero-agent")) {
    Add-Content $PROFILE "`n$profileLine"
    Write-Host "🔗 CLI alias 'str8zero-agent' added to PowerShell profile" -ForegroundColor Green
} else {
    Write-Host "🔗 Alias already exists in profile" -ForegroundColor Yellow
}

# 5. Setup config & log folder
New-Item -ItemType Directory -Path "$installPath\config" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\logs" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\agents" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\generated_apps" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\cli\data" -Force | Out-Null

# 6. Create default config if it doesn't exist
$configPath = "$installPath\config\defaults.yaml"
if (!(Test-Path $configPath)) {
    Copy-Item "$installPath\config\defaults.yaml" $configPath -ErrorAction SilentlyContinue
}

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

# 8. Launch demo task
Write-Host "`n🎤 Running symbolic demo task..." -ForegroundColor Cyan
& $aliasPath "rebellion meets prophecy" --task vibe-gen --explain

Write-Host "`n✅ Enhanced Str8ZeROCLI is ready. Use 'str8zero-agent' in any terminal window." -ForegroundColor Green
Write-Host "   You may need to restart your PowerShell session for the alias to take effect." -ForegroundColor Yellow
Write-Host "   To create a custom agent, run: str8zero-agent --create-agent \"My Agent\"" -ForegroundColor Yellow