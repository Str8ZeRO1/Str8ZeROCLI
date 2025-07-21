#!/usr/bin/env python3
import os
import requests
import json
import subprocess
from pathlib import Path

class AgentInterface:
    """Base class for agent integrations"""
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get(f"{self.__class__.__name__.upper()}_API_KEY")
        
    def process(self, prompt, task, platform=None, explain=False):
        """Process a prompt with the agent"""
        raise NotImplementedError("Agent must implement process method")

class AiderAgent(AgentInterface):
    """Integration with Aider CLI"""
    def process(self, prompt, task, platform=None, explain=False):
        try:
            # Check if Aider is installed
            result = subprocess.run(["aider", "--version"], capture_output=True, text=True)
            
            # Prepare command
            cmd = ["aider", "--message", prompt]
            if explain:
                cmd.append("--verbose")
                
            # Execute Aider
            if task == "app-gen":
                # For app generation, create a new directory
                app_name = prompt.title().replace(' ', '')
                app_dir = os.path.join(os.path.expanduser("~"), "Str8ZeROCLI", "generated_apps", app_name)
                os.makedirs(app_dir, exist_ok=True)
                
                # Run Aider in the app directory
                result = subprocess.run(cmd, cwd=app_dir, capture_output=True, text=True)
                return {
                    "success": True,
                    "output": result.stdout,
                    "app_dir": app_dir
                }
            else:
                # For other tasks, run in current directory
                result = subprocess.run(cmd, capture_output=True, text=True)
                return {
                    "success": True,
                    "output": result.stdout
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class GeminiAgent(AgentInterface):
    """Integration with Google Gemini API"""
    def process(self, prompt, task, platform=None, explain=False):
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "GEMINI_API_KEY environment variable not set"
                }
                
            # Prepare the request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Enhance prompt based on task
            if task == "app-gen":
                enhanced_prompt = f"Generate code for: {prompt}. Include HTML, CSS, and JavaScript."
            elif task == "vibe-gen":
                enhanced_prompt = f"Generate creative vibes for: {prompt}. Be poetic and insightful."
            else:
                enhanced_prompt = prompt
                
            data = {
                "contents": [{
                    "parts": [{
                        "text": enhanced_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }
            
            # Make API request
            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "output": result["candidates"][0]["content"]["parts"][0]["text"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class ClaudeAgent(AgentInterface):
    """Integration with Anthropic Claude API"""
    def process(self, prompt, task, platform=None, explain=False):
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "CLAUDE_API_KEY environment variable not set"
                }
                
            # Prepare the request
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            # Enhance prompt based on task
            system_prompt = "You are a helpful AI assistant."
            if task == "app-gen":
                system_prompt = "You are an expert software developer. Generate clean, well-documented code."
            elif task == "deploy":
                system_prompt = "You are a DevOps expert. Provide detailed deployment instructions."
            elif task == "monetize":
                system_prompt = "You are a monetization expert. Provide detailed strategies for app monetization."
                
            data = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            
            # Make API request
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "output": result["content"][0]["text"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class CodexAgent(AgentInterface):
    """Integration with OpenAI Codex API"""
    def process(self, prompt, task, platform=None, explain=False):
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "OPENAI_API_KEY environment variable not set"
                }
                
            # Prepare the request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Enhance prompt based on task
            if task == "app-gen":
                system_message = "You are an expert programmer. Generate complete, working code for the application described."
            elif task == "deploy":
                system_message = "You are a DevOps expert. Provide detailed deployment instructions."
            else:
                system_message = "You are a helpful AI assistant."
                
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            # Make API request
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "output": result["choices"][0]["message"]["content"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def get_agent(name, api_key=None):
    """Factory function to get the appropriate agent"""
    agents = {
        "Aider": AiderAgent,
        "Gemini CLI": GeminiAgent,
        "Claude Code": ClaudeAgent,
        "Codex CLI": CodexAgent
    }
    
    if name in agents:
        return agents[name](api_key)
    else:
        raise ValueError(f"Unknown agent: {name}")