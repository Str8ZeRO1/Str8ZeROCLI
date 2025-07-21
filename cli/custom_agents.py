#!/usr/bin/env python3
import os
import sys
import json
import importlib.util
import subprocess
from pathlib import Path

class CustomAgentLoader:
    """Loader for custom agent plugins"""
    
    def __init__(self):
        self.custom_agents = {}
        self.custom_agents_dir = os.path.join(os.path.expanduser("~"), "Str8ZeROCLI", "agents")
        
        # Create custom agents directory if it doesn't exist
        os.makedirs(self.custom_agents_dir, exist_ok=True)
        
        # Load custom agents
        self._load_custom_agents()
        
    def _load_custom_agents(self):
        """Load all custom agents from the agents directory"""
        if not os.path.exists(self.custom_agents_dir):
            return
            
        # Look for Python files in the agents directory
        for file_path in Path(self.custom_agents_dir).glob("*.py"):
            try:
                # Load the module
                module_name = file_path.stem
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if the module has an Agent class
                if hasattr(module, "Agent"):
                    agent_class = module.Agent
                    
                    # Check if the class has the required methods
                    if hasattr(agent_class, "name") and hasattr(agent_class, "process"):
                        # Create an instance of the agent
                        agent = agent_class()
                        self.custom_agents[agent.name] = agent
            except Exception as e:
                print(f"Error loading custom agent {file_path}: {e}", file=sys.stderr)
                
    def get_custom_agent(self, name):
        """Get a custom agent by name"""
        return self.custom_agents.get(name)
        
    def list_custom_agents(self):
        """List all available custom agents"""
        return list(self.custom_agents.keys())
        
    def create_agent_template(self, name):
        """Create a template for a new custom agent"""
        # Sanitize the name
        safe_name = "".join(c if c.isalnum() else "_" for c in name)
        file_name = f"{safe_name.lower()}_agent.py"
        file_path = os.path.join(self.custom_agents_dir, file_name)
        
        # Check if the file already exists
        if os.path.exists(file_path):
            return {
                "success": False,
                "error": f"Agent file {file_name} already exists"
            }
            
        # Create the template
        template = f'''#!/usr/bin/env python3
"""
Custom Agent: {name}
"""
import os
import subprocess
import requests

class Agent:
    """Custom agent implementation for {name}"""
    
    # Agent name (used for routing)
    name = "{name}"
    
    # Agent emoji (displayed in CLI)
    emoji = "✨"
    
    # Agent description
    description = "Custom agent for {name}"
    
    def __init__(self):
        # Initialize your agent here
        self.api_key = os.environ.get("{safe_name.upper()}_API_KEY")
        
    def process(self, prompt, task, platform=None, explain=False):
        """
        Process a prompt with this agent
        
        Args:
            prompt (str): The user prompt
            task (str): The task type (app-gen, deploy, monetize, vibe-gen)
            platform (str, optional): Target platform for deployment
            explain (bool): Whether to provide detailed explanation
            
        Returns:
            dict: Result with success status and output
        """
        try:
            # Implement your agent logic here
            # This is just a placeholder implementation
            
            # Example API call:
            # response = requests.post(
            #     "https://api.example.com/v1/generate",
            #     headers={"Authorization": f"Bearer {{self.api_key}}"},
            #     json={"prompt": prompt}
            # )
            # result = response.json()
            
            # For now, just return a simple response
            return {{
                "success": True,
                "output": f"Custom agent {name} processed: {{prompt}}"
            }}
            
        except Exception as e:
            return {{
                "success": False,
                "error": str(e)
            }}
'''
        
        # Write the template to the file
        with open(file_path, "w") as f:
            f.write(template)
            
        return {
            "success": True,
            "path": file_path
        }