#!/usr/bin/env python3
"""
Str8ZeROCLI - AI-Powered Business OS
-----------------------------------
Transform symbolic intention into profitable reality.
"""
import os
import sys
import json
import click
import random
from datetime import datetime
from pathlib import Path

# Import core modules
from cli.str8zero_core import Str8ZeroCore
from cli.market_analysis import MarketAnalyzer
from cli.app_generator import AppGenerator
from cli.memory.kernel import load_user_profile, save_user_profile

# Set up paths
HOME_DIR = Path.home()
STR8ZERO_DIR = os.path.join(HOME_DIR, "Str8ZeROCLI")
CONFIG_DIR = os.path.join(STR8ZERO_DIR, "config")
LOGS_DIR = os.path.join(STR8ZERO_DIR, "logs")
DATA_DIR = os.path.join(STR8ZERO_DIR, "data")
APPS_DIR = os.path.join(STR8ZERO_DIR, "generated_apps")

# Ensure directories exist
for directory in [CONFIG_DIR, LOGS_DIR, DATA_DIR, APPS_DIR]:
    os.makedirs(directory, exist_ok=True)

@click.group()
def cli():
    """Str8ZeRO AI Agent - Transform symbolic intention into profitable reality."""
    pass

@cli.command()
@click.argument('prompt')
@click.option('--task', default='app-gen', help='Task to perform: app-gen, deploy, monetize, vibe-gen')
@click.option('--platform', default='all', help='Target platform: android, ios, web, all')
@click.option('--explain', is_flag=True, help='Show detailed explanation')
@click.option('--override', help='Override agent selection: aider, gemini, codex, claude')
@click.option('--profile', default='default', help='Use a specific profile')
def build(prompt, task, platform, explain, override, profile):
    """Build an app or solution from a prompt."""
    click.echo(f"\n🚀 Str8ZeRO Agent - Processing: '{prompt}'")
    
    # Initialize core
    core = Str8ZeroCore(profile, prompt)
    
    # Execute build pipeline
    result = core.build()
    
    # Display results
    click.echo(f"\n✅ Build completed successfully!")
    click.echo(f"📱 App Type: {result['logic']['app_type']}")
    click.echo(f"🎯 Target Platforms: {', '.join(result['deployment']['targets'])}")
    
    if explain:
        click.echo("\n📊 Build Details:")
        click.echo(f"  • Intent: {result['intent']['goal']}")
        click.echo(f"  • Domain: {result['intent']['domain']}")
        click.echo(f"  • Features: {', '.join(result['logic']['features'])}")
        click.echo(f"  • Monetization: {result['monetization']['model']}")
        click.echo(f"  • Est. Revenue: ${result['monetization']['revenue_potential']['estimated_monthly_revenue']}/month")
    
    return result

@cli.command()
@click.option('--category', help='App category to analyze')
@click.option('--keywords', help='Keywords to search for (comma-separated)')
def analyze(category, keywords):
    """Analyze the app market for opportunities."""
    click.echo(f"\n🔍 Analyzing market...")
    
    # Parse keywords if provided
    keyword_list = keywords.split(',') if keywords else None
    
    # Initialize market analyzer
    analyzer = MarketAnalyzer()
    
    # Analyze market
    results = analyzer.analyze_market(category, keyword_list)
    
    # Display results
    click.echo(f"\n✅ Market analysis completed!")
    click.echo(f"📊 Apps analyzed: {results['apps_analyzed']}")
    
    # Show opportunities
    click.echo(f"\n💡 Opportunities found: {len(results['opportunities'])}")
    for i, opportunity in enumerate(results['opportunities']):
        click.echo(f"\n  {i+1}. {opportunity['type'].replace('_', ' ').title()}")
        click.echo(f"     {opportunity['description']}")
        click.echo(f"     Potential: {opportunity['potential'].upper()}")
    
    # Show competition
    click.echo(f"\n🥊 Competition level: {results['competition_analysis']['level'].upper()}")
    
    return results

@cli.command()
@click.argument('app_name')
@click.option('--app-type', required=True, help='Type of app to generate')
@click.option('--features', help='Comma-separated list of features')
@click.option('--platform', default='all', help='Target platform: android, ios, web, all')
def generate(app_name, app_type, features, platform):
    """Generate app code based on specifications."""
    click.echo(f"\n🛠️ Generating app: {app_name}")
    
    # Parse features if provided
    feature_list = features.split(',') if features else None
    
    # Initialize app generator
    generator = AppGenerator()
    
    # Generate app
    result = generator.generate_app(app_name, app_type, feature_list, platform)
    
    # Display results
    click.echo(f"\n✅ App generated successfully!")
    click.echo(f"📁 App directory: {result['app_dir']}")
    click.echo(f"📊 Files generated: {result['files_generated']}")
    click.echo(f"🎯 Platforms: {', '.join(result['platforms'])}")
    
    return result

@cli.command()
@click.option('--list-agents', is_flag=True, help='List all available agents')
@click.option('--list-profiles', is_flag=True, help='List all available profiles')
def info(list_agents, list_profiles):
    """Display information about Str8ZeROCLI."""
    if list_agents:
        click.echo("\n🤖 Available Agents:")
        click.echo("  • Built-in Agents:")
        click.echo("    - Semantic Agent: Interprets user prompts")
        click.echo("    - Logic Agent: Generates app blueprints")
        click.echo("    - Visual Agent: Creates UI/UX")
        click.echo("    - Marketing Agent: Generates marketing plans")
        click.echo("    - Monetization Agent: Configures revenue streams")
        click.echo("    - Deployment Agent: Handles app deployment")
    
    if list_profiles:
        profiles_dir = os.path.join(STR8ZERO_DIR, "profiles")
        if os.path.exists(profiles_dir):
            profiles = [f.stem for f in Path(profiles_dir).glob("*.yaml")]
            click.echo("\n📋 Available Profiles:")
            for profile in profiles:
                click.echo(f"  • {profile}")
        else:
            click.echo("\n📋 No profiles found.")
    
    if not list_agents and not list_profiles:
        click.echo("\n🚀 Str8ZeROCLI - AI-Powered Business OS")
        click.echo("\nCommands:")
        click.echo("  build     Build an app from a prompt")
        click.echo("  analyze   Analyze the app market")
        click.echo("  generate  Generate app code")
        click.echo("  info      Display information")
        
        click.echo("\nRun 'str8zero-agent COMMAND --help' for command-specific help.")

if __name__ == '__main__':
    # Check if any arguments were provided
    if len(sys.argv) > 1:
        cli()
    else:
        # If no arguments, show welcome message and help
        click.echo("\n🚀 Welcome to Str8ZeROCLI - AI-Powered Business OS")
        click.echo("\nUsage:")
        click.echo("  str8zero-agent build \"your prompt\" [OPTIONS]")
        click.echo("  str8zero-agent analyze --category CATEGORY [OPTIONS]")
        click.echo("  str8zero-agent generate APP_NAME --app-type TYPE [OPTIONS]")
        click.echo("  str8zero-agent info [OPTIONS]")
        
        click.echo("\nRun 'str8zero-agent --help' for more information.")