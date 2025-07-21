#!/usr/bin/env python3
"""
Str8ZeROCLI Core Engine
-----------------------
Central orchestration system for the Str8ZeROCLI business OS.
Coordinates all agents and processes to transform user intent into profitable apps.
"""
import os
import json
from datetime import datetime
from pathlib import Path

# Import agents
from cli.agents.semantic import interpret_prompt
from cli.agents.logic import generate_app_logic
from cli.agents.visual import generate_ui
from cli.agents.deploy import deploy_to_targets
from cli.agents.marketing import generate_marketing_plan
from cli.agents.monetization import setup_monetization
from cli.memory.kernel import load_user_profile, save_user_profile

class Str8ZeroCore:
    """Core orchestration engine for Str8ZeROCLI business OS"""
    
    def __init__(self, user_context, prompt):
        """Initialize the core engine with user context and prompt"""
        self.timestamp = datetime.now().isoformat()
        self.user_context = user_context
        self.prompt = prompt
        self.memory = load_user_profile(user_context)
        self.log_path = os.path.join(Path.home(), "Str8ZeROCLI", "logs", "core_operations.log")
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # Log initialization
        self._log_operation("init", f"Core initialized with prompt: {prompt[:50]}...")
    
    def build(self):
        """Execute the full build pipeline"""
        # Step 1: Semantic analysis
        self._log_operation("semantic", "Interpreting user intent")
        self.intent = interpret_prompt(self.prompt, self.memory)
        
        # Step 2: Generate app logic
        self._log_operation("logic", f"Generating app logic for domain: {self.intent.get('domain', 'unknown')}")
        self.logic = generate_app_logic(self.intent)
        
        # Step 3: Generate UI
        self._log_operation("visual", "Creating adaptive UI")
        self.visual = generate_ui(self.intent, self.logic)
        
        # Step 4: Setup monetization
        self._log_operation("monetize", "Configuring revenue streams")
        self.monetization = setup_monetization(self.intent, self.logic)
        
        # Step 5: Generate marketing plan
        self._log_operation("marketing", "Creating marketing strategy")
        self.marketing = generate_marketing_plan(self.intent, self.logic)
        
        # Step 6: Deploy to targets
        self._log_operation("deploy", "Preparing deployment package")
        self.deployment = deploy_to_targets(self.logic, self.visual, self.memory)
        
        # Step 7: Update user memory with this operation
        self.memory["history"].append({
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "intent": self.intent,
            "app_type": self.logic.get("app_type", "unknown")
        })
        save_user_profile(self.user_context, self.memory)
        
        # Return complete result
        return {
            "timestamp": self.timestamp,
            "intent": self.intent,
            "logic": self.logic,
            "visual": self.visual,
            "monetization": self.monetization,
            "marketing": self.marketing,
            "deployment": self.deployment
        }
    
    def _log_operation(self, stage, message):
        """Log an operation to the core operations log"""
        with open(self.log_path, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] [{self.user_context}] [{stage}] {message}\n")