# Str8ZeROCLI

Str8ZeROCLI is a symbolic-to-reality agent router—an AI-powered command-line orchestrator that transforms emotional intention into executable code. From "freedom as signal" to "rebellion meets prophecy," this CLI parses mood, syntax, and deployment goals to route tasks to the optimal coding agent: Aider, Gemini CLI, Codex CLI, Claude Code, or Warp. With sci-fi gearshift visuals, mood-based override logic, and auto-Git telemetry, it's mission control for creative developers ready to command living systems from the terminal.

## Installation

### Windows
```powershell
irm https://raw.githubusercontent.com/Str8ZeRO1/Str8ZeROCLI/main/setup-str8zero.ps1 | iex
```

### Linux/macOS
```bash
curl -sL https://raw.githubusercontent.com/Str8ZeRO1/Str8ZeROCLI/main/install.sh | bash
```

## Usage

```
str8zero-agent "your prompt" [OPTIONS]
```

### Options

```
--task [app-gen|deploy|monetize|vibe-gen]  Task to perform (default: app-gen)
--platform [android|ios|web|all]           Target platform (default: all)
--explain                                  Show detailed explanation
--override [aider|gemini|codex|claude]     Override agent selection
```

### Examples

```powershell
# Generate a fitness app
str8zero-agent "fitness app with workout tracking" --task app-gen

# Deploy an app to iOS
str8zero-agent "deploy my fitness app" --task deploy --platform ios

# Set up monetization
str8zero-agent "monetize with subscription model" --task monetize

# Generate creative vibes
str8zero-agent "rebellion meets prophecy" --task vibe-gen --explain
```

## Agent Selection

Str8ZeROCLI automatically selects the optimal agent based on:

1. **Mood** - Emotional signals in your prompt
2. **Syntax** - Code patterns in your request
3. **Task** - The specific operation you're performing

For example:
- "rebellion meets prophecy" → Gemini CLI (creative, sketch-based)
- "precise test suite" → Claude Code (testing, multi-file)
- "quick refactor" → Aider (efficient, code-focused)

See [AGENTS.md](AGENTS.md) for detailed configuration options.

## Customization

Edit your agent routing preferences in `~/Str8ZeROCLI/config/defaults.yaml`:

```yaml
preferences:
  vibe-gen:
    mood:
      rebellious: "Gemini CLI"
    syntax:
      sketch-based: "Gemini CLI"
    fallback: "Aider"
```

## Directory Structure

```
~/Str8ZeROCLI/
├── cli/
│   └── main.py
├── config/
│   └── defaults.yaml
├── logs/
│   └── agent_history.json
└── generated_apps/
    └── [Your generated apps]
```