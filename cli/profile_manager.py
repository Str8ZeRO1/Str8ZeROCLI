#!/usr/bin/env python3
import os
import yaml
from pathlib import Path

class ProfileManager:
    """Manages user profiles for Str8ZeROCLI"""
    
    def __init__(self):
        self.profiles_dir = os.path.join(os.path.expanduser("~"), "Str8ZeROCLI", "profiles")
        
        # Create profiles directory if it doesn't exist
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        # Create default profile if it doesn't exist
        default_profile_path = os.path.join(self.profiles_dir, "default.yaml")
        if not os.path.exists(default_profile_path):
            default_profile = {
                "name": "Default",
                "description": "Default profile for Str8ZeROCLI",
                "preferences": {
                    "theme": "dark",
                    "auto_commit": True,
                    "telemetry": "minimal",
                    "default_task": "app-gen",
                    "default_platform": "all",
                    "default_agent": "Aider",
                    "api_keys": {
                        "use_env": True
                    }
                }
            }
            
            with open(default_profile_path, 'w') as f:
                yaml.dump(default_profile, f, default_flow_style=False)
    
    def get_profile(self, profile_name="default"):
        """Get a profile by name"""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.yaml")
        
        if not os.path.exists(profile_path):
            # If profile doesn't exist, use default
            profile_path = os.path.join(self.profiles_dir, "default.yaml")
            
            # If default doesn't exist either, return empty profile
            if not os.path.exists(profile_path):
                return {
                    "name": "Default",
                    "description": "Default profile for Str8ZeROCLI",
                    "preferences": {}
                }
        
        try:
            with open(profile_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            return {
                "name": "Default",
                "description": "Default profile for Str8ZeROCLI",
                "preferences": {}
            }
    
    def list_profiles(self):
        """List all available profiles"""
        profiles = []
        
        for file_path in Path(self.profiles_dir).glob("*.yaml"):
            profile_name = file_path.stem
            try:
                with open(file_path, 'r') as f:
                    profile = yaml.safe_load(f)
                    profiles.append({
                        "name": profile.get("name", profile_name),
                        "description": profile.get("description", ""),
                        "path": str(file_path)
                    })
            except:
                profiles.append({
                    "name": profile_name,
                    "description": "Error loading profile",
                    "path": str(file_path)
                })
        
        return profiles
    
    def create_profile(self, profile_name, preferences=None):
        """Create a new profile"""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.yaml")
        
        # Check if profile already exists
        if os.path.exists(profile_path):
            return {
                "success": False,
                "error": f"Profile '{profile_name}' already exists"
            }
        
        # Create profile
        profile = {
            "name": profile_name,
            "description": f"Custom profile: {profile_name}",
            "preferences": preferences or {}
        }
        
        try:
            with open(profile_path, 'w') as f:
                yaml.dump(profile, f, default_flow_style=False)
                
            return {
                "success": True,
                "path": profile_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_profile(self, profile_name, preferences):
        """Update an existing profile"""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.yaml")
        
        # Check if profile exists
        if not os.path.exists(profile_path):
            return {
                "success": False,
                "error": f"Profile '{profile_name}' does not exist"
            }
        
        try:
            # Load existing profile
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
            
            # Update preferences
            profile["preferences"].update(preferences)
            
            # Save profile
            with open(profile_path, 'w') as f:
                yaml.dump(profile, f, default_flow_style=False)
                
            return {
                "success": True,
                "path": profile_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }