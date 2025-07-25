# Str8ZeROCLI Profile Setup Script
Write-Host "`n🚀 Setting up Str8ZeROCLI profile..." -ForegroundColor Cyan

# 1. Define paths
$installPath = "$env:USERPROFILE\Str8ZeROCLI"
$profilePath = "$installPath\profiles"
$pythonScript = "$installPath\cli\main.py"
$aliasPath = "$env:USERPROFILE\str8zero-agent.ps1"

# 2. Create profile directory if it doesn't exist
if (!(Test-Path $profilePath)) {
    New-Item -ItemType Directory -Path $profilePath -Force | Out-Null
    Write-Host "📁 Created profiles directory" -ForegroundColor Green
}

# 3. Create default profile if it doesn't exist
$defaultProfilePath = "$profilePath\default.yaml"
if (!(Test-Path $defaultProfilePath)) {
    @"
# Str8ZeROCLI Default Profile
name: Default
description: Default profile for Str8ZeROCLI
preferences:
  theme: dark
  auto_commit: true
  telemetry: minimal
  default_task: app-gen
  default_platform: all
  default_agent: Aider
  api_keys:
    use_env: true
"@ | Set-Content $defaultProfilePath
    Write-Host "📄 Created default profile" -ForegroundColor Green
}

# 4. Create development profile
$devProfilePath = "$profilePath\development.yaml"
@"
# Str8ZeROCLI Development Profile
name: Development
description: Profile optimized for code development
preferences:
  theme: dark
  auto_commit: true
  telemetry: minimal
  default_task: app-gen
  default_platform: all
  default_agent: Aider
  code_style:
    language: auto
    indent: 4
    line_length: 88
  api_keys:
    use_env: true
"@ | Set-Content $devProfilePath
Write-Host "📄 Created development profile" -ForegroundColor Green

# 5. Create creative profile
$creativeProfilePath = "$profilePath\creative.yaml"
@"
# Str8ZeROCLI Creative Profile
name: Creative
description: Profile optimized for creative tasks
preferences:
  theme: dark
  auto_commit: false
  telemetry: minimal
  default_task: vibe-gen
  default_platform: all
  default_agent: Gemini CLI
  api_keys:
    use_env: true
"@ | Set-Content $creativeProfilePath
Write-Host "📄 Created creative profile" -ForegroundColor Green

# 6. Create deployment profile
$deployProfilePath = "$profilePath\deployment.yaml"
@"
# Str8ZeROCLI Deployment Profile
name: Deployment
description: Profile optimized for deployment tasks
preferences:
  theme: dark
  auto_commit: true
  telemetry: detailed
  default_task: deploy
  default_platform: all
  default_agent: Claude Code
  api_keys:
    use_env: true
"@ | Set-Content $deployProfilePath
Write-Host "📄 Created deployment profile" -ForegroundColor Green

# 7. Update main script alias to include profile support
@"
param(
    [Parameter(Position=0)]
    [string]`$prompt,
    
    [Parameter(ValueFromRemainingArguments=`$true)]
    [string[]]`$remainingArgs
)

# Check if --profile is specified
`$profileName = "default"
`$argList = @()

for (`$i = 0; `$i -lt `$remainingArgs.Count; `$i++) {
    if (`$remainingArgs[`$i] -eq "--profile" -and `$i -lt `$remainingArgs.Count - 1) {
        `$profileName = `$remainingArgs[`$i+1]
        `$i++  # Skip the next argument
    } else {
        `$argList += `$remainingArgs[`$i]
    }
}

# Add profile parameter
`$argList += "--profile"
`$argList += `$profileName

# Run the script with all parameters
if (`$prompt) {
    python "$pythonScript" "`$prompt" @argList
} else {
    python "$pythonScript" @argList
}
"@ | Set-Content $aliasPath

# 8. Update PowerShell profile if needed
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

Write-Host "`n✅ Str8ZeROCLI profiles are ready!" -ForegroundColor Green
Write-Host "   You can now use profiles with: str8zero-agent \"your prompt\" --profile development" -ForegroundColor Yellow
Write-Host "   Available profiles: default, development, creative, deployment" -ForegroundColor Yellow