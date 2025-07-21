# ⚙️ Str8ZeROCLI Installer for Windows PowerShell
Write-Host "`n🚀 Installing Str8ZeROCLI..." -ForegroundColor Cyan

# 1. Define repo and paths
$repoUrl = "https://github.com/Str8ZeRO1/Str8ZeROCLI"
$installPath = "$env:USERPROFILE\Str8ZeROCLI"
$pythonScript = "$installPath\cli\main.py"

# 2. Clone the GitHub repo
if (!(Test-Path $installPath)) {
    git clone $repoUrl $installPath
} else {
    Write-Host "📁 Repo already exists at $installPath" -ForegroundColor Yellow
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
if (!(Get-Content $PROFILE | Select-String "str8zero-agent")) {
    Add-Content $PROFILE "`n$profileLine"
    Write-Host "🔗 CLI alias 'str8zero-agent' added to PowerShell profile" -ForegroundColor Green
} else {
    Write-Host "🔗 Alias already exists in profile" -ForegroundColor Yellow
}

# 5. Setup config & log folder
New-Item -ItemType Directory -Path "$installPath\config" -Force | Out-Null
New-Item -ItemType File -Path "$installPath\config\defaults.yaml" -Force | Out-Null
New-Item -ItemType Directory -Path "$installPath\logs" -Force | Out-Null
New-Item -ItemType File -Path "$installPath\logs\agent_history.json" -Force | Out-Null

# 6. Launch demo task
Write-Host "`n🎤 Running symbolic demo task..." -ForegroundColor Cyan
& $aliasPath "rebellion meets prophecy" --task vibe-gen --explain

Write-Host "`n✅ Str8ZeROCLI is ready. Use 'str8zero-agent' in any terminal window." -ForegroundColor Green