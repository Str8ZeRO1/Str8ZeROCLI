def generate_ui(intent):
    """Generate UI based on user intent"""
    emotion = intent.get("emotion", "neutral")
    
    # Adjust UI based on emotion
    if emotion == "frustration":
        theme = "calm"
        color_scheme = "blue"
    elif emotion == "excitement":
        theme = "energetic"
        color_scheme = "vibrant"
    else:
        theme = "neutral"
        color_scheme = "standard"
    
    return {
        "theme": theme,
        "color_scheme": color_scheme,
        "layout": "adaptive"
    }
