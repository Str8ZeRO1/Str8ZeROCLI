# Str8ZeRO Agent Configuration

This document explains how to configure and customize the agent routing system in Str8ZeROCLI.

## Available Agents

| Agent | Emoji | Strengths | Cost |
|-------|-------|-----------|------|
| Aider | 🕶 | Fast, efficient, low-cost | $ |
| Codex CLI | 🧠 | Code generation, refactoring | $$ |
| Gemini CLI | 🚀 | Creative, UI/UX, sketching | $$ |
| Claude Code | 🔐 | Precise, multi-file, testing | $$$ |

## Routing Configuration

The agent router selects the optimal agent based on:

1. **Mood** - Emotional signals detected in your prompt
2. **Syntax** - Code patterns and structures in your request
3. **Task** - The specific operation you're performing

### Customizing Agent Selection

Edit `~/Str8ZeROCLI/config/defaults.yaml` to customize routing:

```yaml
preferences:
  vibe-gen:
    mood:
      rebellious: "Gemini CLI"  # When rebellious mood > 0.7, use Gemini
    syntax:
      sketch-based: "Gemini CLI"  # When sketch syntax detected, use Gemini
    fallback: "Aider"  # Default for this task
```

### Available Moods

- `rebellious` - Freedom, anarchy, breaking conventions
- `elegant` - Clean, precise, structured
- `nostalgic` - Retro, classic, familiar
- `futuristic` - Forward-looking, innovative
- `precise` - Exact, detailed, meticulous
- `rapid` - Fast, efficient, quick
- `cautious` - Careful, thorough, safe

### Available Syntax Patterns

- `sketch-based` - UI/UX design, visual elements
- `code-refactor` - Improving existing code
- `multi-file` - Working across multiple files
- `API-bindings` - Connecting to external services

## Manual Override

You can override the agent selection with the `--override` flag:

```bash
str8zero-agent "your prompt" --override "Claude Code"
```

## Adding Custom Agents

To add a new agent:

1. Create an adapter in `~/Str8ZeROCLI/agents/`
2. Add the agent to your `defaults.yaml` configuration
3. Update the routing logic as needed

## Troubleshooting

If agent selection isn't working as expected:

1. Use `--explain` to see the routing logic
2. Check your `defaults.yaml` for syntax errors
3. Ensure your prompt contains clear mood or syntax signals
4. Try a manual override to test different agents