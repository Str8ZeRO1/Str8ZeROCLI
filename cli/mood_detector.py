#!/usr/bin/env python3
import re
import os
import json
from collections import defaultdict

class MoodDetector:
    """Advanced mood detection for agent routing"""
    
    def __init__(self):
        self.emotion_lexicon = self._load_emotion_lexicon()
        self.syntax_patterns = self._load_syntax_patterns()
        
    def _load_emotion_lexicon(self):
        """Load emotion lexicon from file or use default"""
        lexicon_path = os.path.join(os.path.dirname(__file__), "data", "emotion_lexicon.json")
        
        default_lexicon = {
            "rebellious": ["rebellion", "freedom", "break", "disrupt", "revolution", "anarchy", "resist", "defy", "challenge", "unconventional"],
            "elegant": ["clean", "elegant", "minimal", "precise", "refined", "sophisticated", "polished", "sleek", "streamlined", "graceful"],
            "nostalgic": ["retro", "nostalgia", "classic", "vintage", "old-school", "traditional", "legacy", "throwback", "memory", "reminiscent"],
            "futuristic": ["future", "prophecy", "advanced", "cutting-edge", "innovative", "forward", "next-gen", "tomorrow", "visionary", "ahead"],
            "precise": ["precise", "exact", "accurate", "meticulous", "detailed", "rigorous", "specific", "exacting", "careful", "thorough"],
            "rapid": ["rapid", "quick", "fast", "swift", "speedy", "immediate", "instant", "prompt", "expedient", "hasty"],
            "cautious": ["cautious", "careful", "prudent", "wary", "vigilant", "guarded", "conservative", "safe", "measured", "deliberate"]
        }
        
        try:
            if os.path.exists(lexicon_path):
                with open(lexicon_path, 'r') as f:
                    return json.load(f)
            else:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
                
                # Save default lexicon
                with open(lexicon_path, 'w') as f:
                    json.dump(default_lexicon, f, indent=2)
                    
                return default_lexicon
        except:
            return default_lexicon
            
    def _load_syntax_patterns(self):
        """Load syntax patterns from file or use default"""
        patterns_path = os.path.join(os.path.dirname(__file__), "data", "syntax_patterns.json")
        
        default_patterns = {
            "sketch-based": [
                r"sketch", r"design", r"wireframe", r"mockup", r"prototype", 
                r"layout", r"ui", r"ux", r"interface", r"visual"
            ],
            "code-refactor": [
                r"refactor", r"improve", r"optimize", r"clean", r"restructure", 
                r"rewrite", r"enhance", r"upgrade", r"modernize", r"fix"
            ],
            "multi-file": [
                r"files", r"project", r"codebase", r"repository", r"directory", 
                r"structure", r"organize", r"architecture", r"system", r"framework"
            ],
            "API-bindings": [
                r"api", r"connect", r"integrate", r"binding", r"interface", 
                r"endpoint", r"service", r"request", r"response", r"data"
            ]
        }
        
        try:
            if os.path.exists(patterns_path):
                with open(patterns_path, 'r') as f:
                    return json.load(f)
            else:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(patterns_path), exist_ok=True)
                
                # Save default patterns
                with open(patterns_path, 'w') as f:
                    json.dump(default_patterns, f, indent=2)
                    
                return default_patterns
        except:
            return default_patterns
    
    def detect_emotion(self, prompt):
        """Detect emotional signals in prompt with advanced NLP techniques"""
        prompt_lower = prompt.lower()
        emotions = defaultdict(float)
        
        # Count emotion words
        for emotion, keywords in self.emotion_lexicon.items():
            for keyword in keywords:
                # Look for whole word matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(pattern, prompt_lower)
                
                # Add weight for each match
                if matches:
                    # Primary matches (exact keywords)
                    emotions[emotion] += 0.3 * len(matches)
                    
                    # Check for intensifiers near emotion words
                    intensifiers = ["very", "extremely", "deeply", "highly", "incredibly", "truly", "absolutely"]
                    for intensifier in intensifiers:
                        if f"{intensifier} {keyword}" in prompt_lower:
                            emotions[emotion] += 0.2
                            
        # Context-based analysis
        if "freedom" in prompt_lower and "expression" in prompt_lower:
            emotions["rebellious"] += 0.4
            
        if "clean" in prompt_lower and "code" in prompt_lower:
            emotions["elegant"] += 0.4
            
        if "like the old days" in prompt_lower or "remember when" in prompt_lower:
            emotions["nostalgic"] += 0.4
            
        if "cutting edge" in prompt_lower or "next generation" in prompt_lower:
            emotions["futuristic"] += 0.4
            
        if "no errors" in prompt_lower or "perfect output" in prompt_lower:
            emotions["precise"] += 0.4
            
        if "deadline" in prompt_lower or "as soon as possible" in prompt_lower:
            emotions["rapid"] += 0.4
            
        if "make sure" in prompt_lower or "double check" in prompt_lower:
            emotions["cautious"] += 0.4
            
        # Normalize scores to 0-1 range
        max_score = max(emotions.values()) if emotions else 0
        if max_score > 0:
            for emotion in emotions:
                emotions[emotion] = min(emotions[emotion] / max_score, 1.0)
                
        # Return top emotions
        return {k: v for k, v in emotions.items() if v > 0.3}
        
    def analyze_syntax(self, prompt):
        """Analyze syntax patterns in prompt with regex matching"""
        prompt_lower = prompt.lower()
        syntax = {}
        
        # Check each syntax pattern
        for pattern_type, patterns in self.syntax_patterns.items():
            # Look for any pattern matches
            for pattern in patterns:
                if re.search(r'\b' + pattern + r'\b', prompt_lower):
                    syntax[pattern_type] = True
                    break
            else:
                syntax[pattern_type] = False
                
        # Additional context-based analysis
        if "create a ui" in prompt_lower or "design an interface" in prompt_lower:
            syntax["sketch-based"] = True
            
        if "improve performance" in prompt_lower or "make it faster" in prompt_lower:
            syntax["code-refactor"] = True
            
        if "project structure" in prompt_lower or "organize code" in prompt_lower:
            syntax["multi-file"] = True
            
        if "connect to" in prompt_lower or "integrate with" in prompt_lower:
            syntax["API-bindings"] = True
            
        return syntax