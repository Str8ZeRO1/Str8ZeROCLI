#!/bin/bash
# Str8ZeROCLI Command Cockpit Launcher

echo -e "\n🚀 Launching Str8ZeRO Command Cockpit..."

# Check if PyQt5 is installed
if ! python -c "import PyQt5" &> /dev/null; then
    echo -e "\n⚠️ PyQt5 not found. Installing required packages..."
    pip install -r requirements.txt
fi

# Launch the cockpit
python app.py