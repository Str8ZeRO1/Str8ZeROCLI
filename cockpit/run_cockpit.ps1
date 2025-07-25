# Str8ZeROCLI Command Cockpit Launcher
Write-Host "`n🚀 Launching Str8ZeRO Command Cockpit..." -ForegroundColor Cyan

# Check if PyQt5 is installed
$pyqt5Installed = python -c "import PyQt5; print('PyQt5 installed')" 2>$null
if (-not $pyqt5Installed) {
    Write-Host "`n⚠️ PyQt5 not found. Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Launch the cockpit
python app.py