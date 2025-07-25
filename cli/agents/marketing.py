#!/usr/bin/env python3
"""
Marketing Agent
--------------
Generates marketing strategies, ad copy, and ASO keywords for apps.
"""
import os
import json
import random
from pathlib import Path

def generate_marketing_plan(intent, logic):
    """
    Generate a comprehensive marketing plan based on user intent and app logic
    
    Args:
        intent (dict): User intent with emotion, goal, and domain
        logic (dict): App logic with app_type and features
        
    Returns:
        dict: Complete marketing plan with strategies, copy, and channels
    """
    app_type = logic.get("app_type", "generic")
    domain = intent.get("domain", "unknown")
    emotion = intent.get("emotion", "neutral")
    
    # Generate app store optimization keywords
    aso_keywords = generate_aso_keywords(app_type, domain)
    
    # Generate ad copy
    ad_copy = generate_ad_copy(intent, logic)
    
    # Determine marketing channels
    channels = select_marketing_channels(app_type, domain)
    
    # Create marketing budget allocation
    budget = allocate_budget(channels)
    
    return {
        "aso_keywords": aso_keywords,
        "ad_copy": ad_copy,
        "channels": channels,
        "budget_allocation": budget,
        "estimated_cac": estimate_customer_acquisition_cost(app_type, channels),
        "estimated_roi": estimate_roi(app_type, channels, logic.get("features", []))
    }

def generate_aso_keywords(app_type, domain):
    """Generate App Store Optimization keywords"""
    base_keywords = []
    
    # Domain-specific keywords
    if domain == "billing":
        base_keywords = ["bill tracker", "utility monitor", "expense alert", "bill management"]
    elif domain == "scheduling":
        base_keywords = ["appointment", "scheduler", "calendar", "reminder", "time management"]
    elif domain == "decluttering":
        base_keywords = ["organize", "declutter", "donation", "minimalism", "tidy"]
    else:
        base_keywords = ["app", "utility", "tool", "helper"]
    
    # App type specific keywords
    if app_type == "bill_monitor":
        base_keywords.extend(["bill alert", "utility tracker", "expense monitor"])
    elif app_type == "scheduler":
        base_keywords.extend(["appointment booker", "time saver", "calendar sync"])
    
    # Add generic high-performance keywords
    base_keywords.extend(["free", "easy", "simple", "fast", "efficient"])
    
    return base_keywords

def generate_ad_copy(intent, logic):
    """Generate compelling ad copy based on intent and logic"""
    emotion = intent.get("emotion", "neutral")
    app_type = logic.get("app_type", "app")
    features = logic.get("features", [])
    
    # Headline templates
    headlines = [
        f"Never Worry About {app_type.replace('_', ' ').title()} Again",
        f"The Smartest {app_type.replace('_', ' ').title()} App You'll Ever Use",
        f"Simplify Your Life with Our {app_type.replace('_', ' ').title()} Solution"
    ]
    
    # Description templates
    descriptions = [
        f"Effortlessly manage {app_type.replace('_', ' ')}s with our intuitive app.",
        f"Save time and reduce stress with automated {app_type.replace('_', ' ')} management.",
        f"Join thousands of satisfied users who've simplified their {app_type.replace('_', ' ')} process."
    ]
    
    # Feature bullets
    feature_bullets = []
    for feature in features[:3]:  # Top 3 features
        feature_bullets.append(f"• {feature.replace('_', ' ').title()}")
    
    # Call to action
    ctas = [
        "Download Now - Free!",
        "Try It Today",
        "Start Simplifying Now"
    ]
    
    return {
        "headline": random.choice(headlines),
        "description": random.choice(descriptions),
        "features": feature_bullets,
        "cta": random.choice(ctas)
    }

def select_marketing_channels(app_type, domain):
    """Select optimal marketing channels based on app type and domain"""
    channels = ["App Store", "Google Play"]  # Default channels
    
    # Add channels based on app type
    if app_type == "bill_monitor":
        channels.extend(["Facebook", "Google Search", "Finance Forums"])
    elif app_type == "scheduler":
        channels.extend(["LinkedIn", "Productivity Blogs", "Google Search"])
    elif app_type == "donation_pickup":
        channels.extend(["Facebook", "Local Community Groups", "Charity Networks"])
    
    return channels

def allocate_budget(channels):
    """Allocate marketing budget across channels"""
    total_budget = 1000  # Default budget
    allocation = {}
    
    # Simple equal allocation for now
    channel_budget = total_budget / len(channels)
    for channel in channels:
        allocation[channel] = round(channel_budget, 2)
    
    return allocation

def estimate_customer_acquisition_cost(app_type, channels):
    """Estimate customer acquisition cost based on app type and channels"""
    # Base CAC by app type
    if app_type == "bill_monitor":
        base_cac = 2.50
    elif app_type == "scheduler":
        base_cac = 3.75
    elif app_type == "donation_pickup":
        base_cac = 1.85
    else:
        base_cac = 3.00
    
    # Adjust for channels
    channel_multipliers = {
        "App Store": 1.0,
        "Google Play": 1.1,
        "Facebook": 1.2,
        "Google Search": 1.5,
        "LinkedIn": 2.0,
        "Productivity Blogs": 0.8,
        "Finance Forums": 0.7,
        "Local Community Groups": 0.5,
        "Charity Networks": 0.6
    }
    
    # Calculate average multiplier
    total_multiplier = sum(channel_multipliers.get(channel, 1.0) for channel in channels)
    avg_multiplier = total_multiplier / len(channels)
    
    return round(base_cac * avg_multiplier, 2)

def estimate_roi(app_type, channels, features):
    """Estimate ROI based on app type, channels, and features"""
    # Base ROI by app type
    if app_type == "bill_monitor":
        base_roi = 2.5  # 250%
    elif app_type == "scheduler":
        base_roi = 3.0  # 300%
    elif app_type == "donation_pickup":
        base_roi = 1.8  # 180%
    else:
        base_roi = 2.0  # 200%
    
    # Adjust for number of features
    feature_multiplier = min(1.0 + (len(features) * 0.1), 1.5)
    
    # Adjust for channels (more channels = better reach but diminishing returns)
    channel_multiplier = min(1.0 + (len(channels) * 0.05), 1.3)
    
    return round(base_roi * feature_multiplier * channel_multiplier, 2)