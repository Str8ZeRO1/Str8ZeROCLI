#!/bin/bash
# Str8ZeROCLI Profile Setup Script

echo -e "\n🚀 Setting up Str8ZeROCLI profile..."

# 1. Define paths
INSTALL_PATH="$HOME/Str8ZeROCLI"
PROFILE_PATH="$INSTALL_PATH/profiles"
PYTHON_SCRIPT="$INSTALL_PATH/cli/main.py"
ALIAS_PATH="$HOME/.str8zero-agent"

# 2. Create profile directory if it doesn't exist
mkdir -p "$PROFILE_PATH"
echo "📁 Created profiles directory"

# 3. Create default profile if it doesn't exist
DEFAULT_PROFILE_PATH="$PROFILE_PATH/default.yaml"
if [ ! -f "$DEFAULT_PROFILE_PATH" ]; then
    cat > "$DEFAULT_PROFILE_PATH" << EOL
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
EOL
    echo "📄 Created default profile"
fi

# 4. Create development profile
DEV_PROFILE_PATH="$PROFILE_PATH/development.yaml"
cat > "$DEV_PROFILE_PATH" << EOL
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
EOL
echo "📄 Created development profile"

# 5. Create creative profile
CREATIVE_PROFILE_PATH="$PROFILE_PATH/creative.yaml"
cat > "$CREATIVE_PROFILE_PATH" << EOL
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
EOL
echo "📄 Created creative profile"

# 6. Create deployment profile
DEPLOY_PROFILE_PATH="$PROFILE_PATH/deployment.yaml"
cat > "$DEPLOY_PROFILE_PATH" << EOL
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
EOL
echo "📄 Created deployment profile"

# 7. Update main script alias to include profile support
cat > "$ALIAS_PATH" << EOL
#!/bin/bash

# Check if --profile is specified
profile_name="default"
args=()

for ((i=1; i<\$#; i++)); do
    if [[ "\${!i}" == "--profile" && \$((i+1)) -le \$# ]]; then
        profile_name="\${@:\$((i+1)):1}"
        i=\$((i+1))
    else
        args+=("\${!i}")
    fi
done

# Add profile parameter
args+=("--profile" "\$profile_name")

# Run the script with all parameters
if [ \$# -gt 0 ]; then
    python "$PYTHON_SCRIPT" "\$1" "\${args[@]}"
else
    python "$PYTHON_SCRIPT" "\${args[@]}"
fi
EOL
chmod +x "$ALIAS_PATH"

# 8. Update shell profile if needed
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
else
    SHELL_PROFILE="$HOME/.profile"
fi

if ! grep -q "str8zero-agent" "$SHELL_PROFILE"; then
    echo "alias str8zero-agent=\"$ALIAS_PATH\"" >> "$SHELL_PROFILE"
    echo "🔗 CLI alias 'str8zero-agent' added to shell profile"
else
    echo "🔗 Alias already exists in profile"
fi

echo -e "\n✅ Str8ZeROCLI profiles are ready!"
echo "   You can now use profiles with: str8zero-agent \"your prompt\" --profile development"
echo "   Available profiles: default, development, creative, deployment"
echo "   NOTE: You may need to restart your terminal or run 'source $SHELL_PROFILE' to use the alias."