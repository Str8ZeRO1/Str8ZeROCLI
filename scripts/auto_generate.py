import os
from datetime import datetime

# Project root path
PROJECT_ROOT = r"c:\Users\jay10\NIS development eco-system\Str8ZeROCLI_repo"

def write_to_file(relative_path, content):
    abs_path = os.path.join(PROJECT_ROOT, relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{datetime.now()}] Wrote: {abs_path}")
    return abs_path

def update_docs(module, filename, description):
    docs_path = os.path.join(PROJECT_ROOT, 'docs', f'{module}.md')
    os.makedirs(os.path.dirname(docs_path), exist_ok=True)
    doc_entry = f"\n### `{filename}`\n{description}\n"
    
    if os.path.exists(docs_path):
        with open(docs_path, 'a', encoding='utf-8') as f:
            f.write(doc_entry)
    else:
        with open(docs_path, 'w', encoding='utf-8') as f:
            f.write(f"# {module.capitalize()} Module\n{doc_entry}")
    print(f"[{datetime.now()}] Updated docs: {docs_path}")

def auto_generate(module, filename, content, description):
    folder_map = {
        'cli': 'cli/',
        'agents': 'cli/agents/',
        'profiles': 'profiles/',
        'config': 'config/',
        'examples': 'examples/',
        'docs': 'docs/',
        'scripts': 'scripts/',
    }
    
    folder = folder_map.get(module, '')
    rel_path = os.path.join(folder, filename)
    abs_path = write_to_file(rel_path, content)
    update_docs(module, filename, description)
    return abs_path

if __name__ == "__main__":
    # Example: create a new agent
    agent_code = '''#!/usr/bin/env python3
"""
Custom Agent: Music Generator
"""
import os
import requests

class Agent:
    """Custom agent implementation for music generation"""
    
    # Agent name (used for routing)
    name = "Music Generator"
    
    # Agent emoji (displayed in CLI)
    emoji = "🎵"
    
    def __init__(self):
        self.api_key = os.environ.get("MUSIC_API_KEY")
        
    def process(self, prompt, task, platform=None, explain=False):
        """Process a prompt with this agent"""
        try:
            return {
                "success": True,
                "output": f"Generated music for: {prompt}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
'''
    description = "Music generation agent that creates audio from text prompts."
    auto_generate('agents', 'music_generator.py', agent_code, description)