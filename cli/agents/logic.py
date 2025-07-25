def generate_app_logic(intent):
    """Generate app logic based on user intent"""
    domain = intent.get("domain", "")
    
    if domain == "billing":
        return {
            "app_type": "bill_monitor",
            "features": ["bill upload", "anomaly detection", "auto-inquiry"]
        }
    elif domain == "scheduling":
        return {
            "app_type": "scheduler",
            "features": ["auto-nudge", "calendar sync", "reminder system"]
        }
    
    return {"app_type": "generic", "features": []}
