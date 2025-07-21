#!/bin/bash
# ⚙️ Enhanced Str8ZeROCLI Installer for Linux/macOS

echo -e "\n🚀 Installing Enhanced Str8ZeROCLI..."

# 1. Define repo and paths
REPO_URL="https://github.com/Str8ZeRO1/Str8ZeROCLI"
INSTALL_PATH="$HOME/Str8ZeROCLI"
PYTHON_SCRIPT="$INSTALL_PATH/cli/main.py"

# 2. Clone the GitHub repo
if [ ! -d "$INSTALL_PATH" ]; then
    git clone $REPO_URL $INSTALL_PATH
else
    echo "📁 Repo already exists at $INSTALL_PATH"
    # Update the repo
    cd $INSTALL_PATH
    git pull
fi

# 3. Install Python dependencies
echo -e "\n📦 Installing dependencies..."
pip install -r "$INSTALL_PATH/requirements.txt"

# 4. Create symbolic command alias
ALIAS_PATH="$HOME/.str8zero-agent"
echo "python \"$PYTHON_SCRIPT\" \"\$@\"" > $ALIAS_PATH
chmod +x $ALIAS_PATH

# Add alias to shell profile
if [[ "$SHELL" == *"zsh"* ]]; then
    PROFILE_PATH="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    PROFILE_PATH="$HOME/.bashrc"
else
    PROFILE_PATH="$HOME/.profile"
fi

if ! grep -q "str8zero-agent" $PROFILE_PATH; then
    echo "alias str8zero-agent=\"$ALIAS_PATH\"" >> $PROFILE_PATH
    echo "🔗 CLI alias 'str8zero-agent' added to shell profile"
else
    echo "🔗 Alias already exists in profile"
fi

# 5. Setup config & log folder
mkdir -p "$INSTALL_PATH/config"
mkdir -p "$INSTALL_PATH/logs"
mkdir -p "$INSTALL_PATH/agents"
mkdir -p "$INSTALL_PATH/generated_apps"
mkdir -p "$INSTALL_PATH/cli/data"

# 6. Create default config if it doesn't exist
CONFIG_PATH="$INSTALL_PATH/config/defaults.yaml"
if [ ! -f "$CONFIG_PATH" ]; then
    cp "$INSTALL_PATH/config/defaults.yaml" "$CONFIG_PATH" 2>/dev/null
fi

# 7. Setup API keys (optional)
ENV_PATH="$INSTALL_PATH/.env"
if [ ! -f "$ENV_PATH" ]; then
    cat > "$ENV_PATH" << EOL
# Str8ZeROCLI API Keys
# Uncomment and add your API keys below

# OPENAI_API_KEY=your_openai_api_key
# GEMINI_API_KEY=your_gemini_api_key
# CLAUDE_API_KEY=your_claude_api_key
EOL
    echo -e "\n📝 Created .env file for API keys at $ENV_PATH"
    echo "   Edit this file to add your API keys for full functionality"
fi

# 8. Launch demo task
echo -e "\n🎤 Running symbolic demo task..."
$ALIAS_PATH "rebellion meets prophecy" --task vibe-gen --explain

echo -e "\n✅ Enhanced Str8ZeROCLI is ready. Use 'str8zero-agent' in any terminal window."
echo "NOTE: You may need to restart your terminal or run 'source $PROFILE_PATH' to use the alias."
echo "      To create a custom agent, run: str8zero-agent --create-agent \"My Agent\""