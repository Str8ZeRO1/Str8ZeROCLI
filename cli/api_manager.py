#!/usr/bin/env python3
import os
import json
import requests
import subprocess
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, set_key

class ApiKeyManager:
    """Manages API keys for various services"""
    
    def __init__(self):
        self.env_path = os.path.join(os.path.expanduser("~"), "Str8ZeROCLI", ".env")
        self.keys_dir = os.path.join(os.path.expanduser("~"), "Str8ZeROCLI", ".keys")
        
        # Create keys directory if it doesn't exist
        os.makedirs(self.keys_dir, exist_ok=True)
        
        # Create .env file if it doesn't exist
        if not os.path.exists(self.env_path):
            with open(self.env_path, 'w') as f:
                f.write("# Str8ZeROCLI API Keys\n")
        
        # Load environment variables
        load_dotenv(self.env_path)
        
    def get_api_key(self, service_name):
        """Get API key for a service, prompting if not found"""
        env_var_name = f"{service_name.upper().replace(' ', '_')}_API_KEY"
        
        # Check if key exists in environment
        api_key = os.environ.get(env_var_name)
        if api_key:
            return api_key
            
        # Check if key exists in keys directory
        key_file = os.path.join(self.keys_dir, f"{service_name.lower().replace(' ', '_')}.key")
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                api_key = f.read().strip()
                # Save to .env for future use
                self._save_to_env(env_var_name, api_key)
                return api_key
                
        return None
        
    def set_api_key(self, service_name, api_key):
        """Set API key for a service"""
        env_var_name = f"{service_name.upper().replace(' ', '_')}_API_KEY"
        
        # Save to .env file
        self._save_to_env(env_var_name, api_key)
        
        # Also save to keys directory (for backup)
        key_file = os.path.join(self.keys_dir, f"{service_name.lower().replace(' ', '_')}.key")
        with open(key_file, 'w') as f:
            f.write(api_key)
            
        return True
        
    def _save_to_env(self, var_name, value):
        """Save a variable to .env file"""
        # Use python-dotenv to update .env file
        set_key(self.env_path, var_name, value)
        # Update current environment
        os.environ[var_name] = value
        
    def get_free_api_key(self, service_name):
        """Get a free API key for supported services"""
        if service_name.lower() == "openai":
            return self._get_openai_key()
        elif service_name.lower() == "huggingface":
            return self._get_huggingface_key()
        elif service_name.lower() == "replicate":
            return self._get_replicate_key()
        elif service_name.lower() == "stability":
            return self._get_stability_key()
        else:
            return {
                "success": False,
                "message": f"No free key provider for {service_name}"
            }
            
    def _get_openai_key(self):
        """Guide user to get an OpenAI API key"""
        print("\n📝 OpenAI API Key Instructions:")
        print("1. Go to https://platform.openai.com/account/api-keys")
        print("2. Sign up or log in to your OpenAI account")
        print("3. Click 'Create new secret key'")
        print("4. Copy the key (you won't be able to see it again)")
        
        # Open the website
        webbrowser.open("https://platform.openai.com/account/api-keys")
        
        return {
            "success": False,
            "message": "OpenAI requires manual key creation. Follow the instructions in your browser."
        }
        
    def _get_huggingface_key(self):
        """Get a Hugging Face API key"""
        print("\n📝 Hugging Face API Key Instructions:")
        print("1. Go to https://huggingface.co/settings/tokens")
        print("2. Sign up or log in to your Hugging Face account")
        print("3. Click 'New token'")
        print("4. Copy the key")
        
        # Open the website
        webbrowser.open("https://huggingface.co/settings/tokens")
        
        return {
            "success": False,
            "message": "Hugging Face requires manual key creation. Follow the instructions in your browser."
        }
        
    def _get_replicate_key(self):
        """Get a Replicate API key"""
        print("\n📝 Replicate API Key Instructions:")
        print("1. Go to https://replicate.com/account/api-tokens")
        print("2. Sign up or log in to your Replicate account")
        print("3. Copy your API token")
        
        # Open the website
        webbrowser.open("https://replicate.com/account/api-tokens")
        
        return {
            "success": False,
            "message": "Replicate requires manual key creation. Follow the instructions in your browser."
        }
        
    def _get_stability_key(self):
        """Get a Stability AI API key"""
        print("\n📝 Stability AI API Key Instructions:")
        print("1. Go to https://platform.stability.ai/account/keys")
        print("2. Sign up or log in to your Stability AI account")
        print("3. Click 'Create API Key'")
        print("4. Copy the key")
        
        # Open the website
        webbrowser.open("https://platform.stability.ai/account/keys")
        
        return {
            "success": False,
            "message": "Stability AI requires manual key creation. Follow the instructions in your browser."
        }
        
    def list_available_services(self):
        """List all available services that can be used with API keys"""
        services = [
            {
                "name": "OpenAI",
                "env_var": "OPENAI_API_KEY",
                "url": "https://platform.openai.com/account/api-keys",
                "has_key": bool(os.environ.get("OPENAI_API_KEY")),
                "free_tier": "Limited free credits for new accounts"
            },
            {
                "name": "Google Gemini",
                "env_var": "GEMINI_API_KEY",
                "url": "https://makersuite.google.com/app/apikey",
                "has_key": bool(os.environ.get("GEMINI_API_KEY")),
                "free_tier": "Free tier available"
            },
            {
                "name": "Anthropic Claude",
                "env_var": "CLAUDE_API_KEY",
                "url": "https://console.anthropic.com/account/keys",
                "has_key": bool(os.environ.get("CLAUDE_API_KEY")),
                "free_tier": "Free trial available"
            },
            {
                "name": "Hugging Face",
                "env_var": "HUGGINGFACE_API_KEY",
                "url": "https://huggingface.co/settings/tokens",
                "has_key": bool(os.environ.get("HUGGINGFACE_API_KEY")),
                "free_tier": "Free tier available"
            },
            {
                "name": "Replicate",
                "env_var": "REPLICATE_API_KEY",
                "url": "https://replicate.com/account/api-tokens",
                "has_key": bool(os.environ.get("REPLICATE_API_KEY")),
                "free_tier": "Free credits for new accounts"
            },
            {
                "name": "Stability AI",
                "env_var": "STABILITY_API_KEY",
                "url": "https://platform.stability.ai/account/keys",
                "has_key": bool(os.environ.get("STABILITY_API_KEY")),
                "free_tier": "Limited free credits"
            }
        ]
        
        return services