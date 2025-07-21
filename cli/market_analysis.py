#!/usr/bin/env python3
"""
Market Analysis Module
---------------------
Analyzes app store trends and identifies profitable niches and opportunities.
"""
import os
import json
import random
from datetime import datetime
from pathlib import Path

class MarketAnalyzer:
    """Analyzes app markets to find profitable opportunities"""
    
    def __init__(self):
        """Initialize the market analyzer"""
        self.data_path = os.path.join(Path.home(), "Str8ZeROCLI", "data", "market_data.json")
        self.cache_path = os.path.join(Path.home(), "Str8ZeROCLI", "data", "market_cache.json")
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Load or initialize market data
        self.market_data = self._load_market_data()
        
    def analyze_market(self, category=None, keywords=None):
        """
        Analyze the app market for opportunities
        
        Args:
            category (str, optional): App category to analyze
            keywords (list, optional): Keywords to search for
            
        Returns:
            dict: Market analysis results with opportunities
        """
        # Update market data if needed
        if self._should_update_data():
            self._update_market_data()
        
        # Filter by category if provided
        if category:
            relevant_apps = [app for app in self.market_data.get("apps", []) 
                            if category.lower() in app.get("categories", [])]
        else:
            relevant_apps = self.market_data.get("apps", [])
        
        # Filter by keywords if provided
        if keywords:
            keyword_apps = []
            for app in relevant_apps:
                for keyword in keywords:
                    if (keyword.lower() in app.get("name", "").lower() or
                        keyword.lower() in app.get("description", "").lower() or
                        keyword.lower() in " ".join(app.get("keywords", []))):
                        keyword_apps.append(app)
                        break
            relevant_apps = keyword_apps
        
        # Find gaps and opportunities
        opportunities = self._identify_opportunities(relevant_apps)
        
        # Generate market report
        return {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "keywords": keywords,
            "apps_analyzed": len(relevant_apps),
            "opportunities": opportunities,
            "market_trends": self._identify_trends(relevant_apps),
            "competition_analysis": self._analyze_competition(relevant_apps)
        }
    
    def _load_market_data(self):
        """Load market data from file or initialize with defaults"""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading market data: {e}")
        
        # Return default data structure
        return {
            "last_updated": None,
            "apps": [],
            "categories": [],
            "trends": []
        }
    
    def _should_update_data(self):
        """Check if market data should be updated"""
        # Update if no data or last update was more than 7 days ago
        if not self.market_data.get("last_updated"):
            return True
            
        last_updated = datetime.fromisoformat(self.market_data.get("last_updated"))
        days_since_update = (datetime.now() - last_updated).days
        
        return days_since_update >= 7
    
    def _update_market_data(self):
        """Update market data by crawling app stores"""
        # In a real implementation, this would call APIs or scrape app stores
        # For now, we'll simulate with sample data
        
        # Simulate app store data
        categories = [
            "productivity", "finance", "lifestyle", "health", 
            "utilities", "social", "education", "entertainment"
        ]
        
        # Generate sample apps
        apps = []
        for i in range(100):
            category = random.choice(categories)
            rating = round(random.uniform(2.0, 5.0), 1)
            price_model = random.choice(["free", "paid", "freemium", "subscription"])
            
            if price_model == "paid":
                price = round(random.uniform(0.99, 9.99), 2)
            elif price_model == "subscription":
                price = round(random.uniform(1.99, 14.99), 2)
            else:
                price = 0
                
            downloads = int(10 ** random.uniform(3, 6))  # 1K to 1M
            
            apps.append({
                "id": f"app_{i}",
                "name": f"Sample App {i}",
                "description": f"This is a sample {category} app with various features.",
                "categories": [category],
                "rating": rating,
                "reviews": int(downloads * random.uniform(0.01, 0.1)),
                "price_model": price_model,
                "price": price,
                "downloads": downloads,
                "last_updated": (datetime.now().replace(
                    day=random.randint(1, 28),
                    month=random.randint(1, 12)
                )).isoformat(),
                "keywords": [f"keyword_{j}" for j in range(random.randint(3, 10))]
            })
        
        # Update market data
        self.market_data = {
            "last_updated": datetime.now().isoformat(),
            "apps": apps,
            "categories": categories,
            "trends": self._generate_trends(apps, categories)
        }
        
        # Save to file
        with open(self.data_path, 'w') as f:
            json.dump(self.market_data, f, indent=2)
    
    def _generate_trends(self, apps, categories):
        """Generate market trends from app data"""
        trends = []
        
        # Category popularity
        category_counts = {}
        for app in apps:
            for category in app.get("categories", []):
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Sort categories by popularity
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Add top categories trend
        trends.append({
            "name": "Top Categories",
            "data": sorted_categories[:5]
        })
        
        # Price model distribution
        price_models = {}
        for app in apps:
            model = app.get("price_model", "free")
            price_models[model] = price_models.get(model, 0) + 1
        
        trends.append({
            "name": "Price Model Distribution",
            "data": price_models
        })
        
        # Rating distribution
        rating_ranges = {
            "4.5-5.0": 0,
            "4.0-4.5": 0,
            "3.5-4.0": 0,
            "3.0-3.5": 0,
            "0.0-3.0": 0
        }
        
        for app in apps:
            rating = app.get("rating", 0)
            if rating >= 4.5:
                rating_ranges["4.5-5.0"] += 1
            elif rating >= 4.0:
                rating_ranges["4.0-4.5"] += 1
            elif rating >= 3.5:
                rating_ranges["3.5-4.0"] += 1
            elif rating >= 3.0:
                rating_ranges["3.0-3.5"] += 1
            else:
                rating_ranges["0.0-3.0"] += 1
        
        trends.append({
            "name": "Rating Distribution",
            "data": rating_ranges
        })
        
        return trends
    
    def _identify_opportunities(self, apps):
        """Identify market opportunities from app data"""
        opportunities = []
        
        # Group apps by category
        category_apps = {}
        for app in apps:
            for category in app.get("categories", []):
                if category not in category_apps:
                    category_apps[category] = []
                category_apps[category].append(app)
        
        # Analyze each category
        for category, category_apps_list in category_apps.items():
            # Calculate average rating
            avg_rating = sum(app.get("rating", 0) for app in category_apps_list) / len(category_apps_list) if category_apps_list else 0
            
            # Calculate average price
            paid_apps = [app for app in category_apps_list if app.get("price", 0) > 0]
            avg_price = sum(app.get("price", 0) for app in paid_apps) / len(paid_apps) if paid_apps else 0
            
            # Look for categories with low average rating but high downloads
            total_downloads = sum(app.get("downloads", 0) for app in category_apps_list)
            if avg_rating < 4.0 and total_downloads > 100000:
                opportunities.append({
                    "type": "underserved_category",
                    "category": category,
                    "avg_rating": round(avg_rating, 1),
                    "total_downloads": total_downloads,
                    "potential": "high",
                    "description": f"Underserved {category} market with high demand but low satisfaction"
                })
            
            # Look for categories with high prices but few apps
            if len(category_apps_list) < 10 and avg_price > 3.0:
                opportunities.append({
                    "type": "premium_niche",
                    "category": category,
                    "app_count": len(category_apps_list),
                    "avg_price": round(avg_price, 2),
                    "potential": "medium",
                    "description": f"Premium niche in {category} with few competitors but higher price points"
                })
        
        # Look for outdated but popular apps
        for app in apps:
            if app.get("downloads", 0) > 100000:
                try:
                    last_updated = datetime.fromisoformat(app.get("last_updated", ""))
                    months_since_update = (datetime.now() - last_updated).days / 30
                    
                    if months_since_update > 6:
                        opportunities.append({
                            "type": "outdated_app",
                            "app_name": app.get("name"),
                            "category": app.get("categories", ["unknown"])[0],
                            "downloads": app.get("downloads"),
                            "months_since_update": round(months_since_update, 1),
                            "potential": "high",
                            "description": f"Popular app not updated in {round(months_since_update, 1)} months"
                        })
                except:
                    pass
        
        return opportunities
    
    def _identify_trends(self, apps):
        """Identify trends from filtered apps"""
        trends = []
        
        # Price model distribution
        price_models = {}
        for app in apps:
            model = app.get("price_model", "free")
            price_models[model] = price_models.get(model, 0) + 1
        
        # Calculate percentages
        total = sum(price_models.values())
        price_model_percentages = {k: round(v / total * 100, 1) if total > 0 else 0 
                                  for k, v in price_models.items()}
        
        trends.append({
            "name": "Monetization Models",
            "data": price_model_percentages
        })
        
        # Average price by model
        price_by_model = {}
        for model in ["paid", "subscription"]:
            model_apps = [app for app in apps if app.get("price_model") == model]
            if model_apps:
                avg_price = sum(app.get("price", 0) for app in model_apps) / len(model_apps)
                price_by_model[model] = round(avg_price, 2)
        
        trends.append({
            "name": "Average Prices",
            "data": price_by_model
        })
        
        return trends
    
    def _analyze_competition(self, apps):
        """Analyze competition level from filtered apps"""
        if not apps:
            return {
                "level": "unknown",
                "top_competitors": []
            }
        
        # Sort by downloads
        sorted_apps = sorted(apps, key=lambda x: x.get("downloads", 0), reverse=True)
        
        # Get top competitors
        top_competitors = []
        for app in sorted_apps[:5]:
            top_competitors.append({
                "name": app.get("name"),
                "downloads": app.get("downloads"),
                "rating": app.get("rating"),
                "price_model": app.get("price_model")
            })
        
        # Determine competition level
        if len(apps) > 50:
            competition_level = "very high"
        elif len(apps) > 20:
            competition_level = "high"
        elif len(apps) > 10:
            competition_level = "medium"
        elif len(apps) > 5:
            competition_level = "low"
        else:
            competition_level = "very low"
        
        return {
            "level": competition_level,
            "app_count": len(apps),
            "top_competitors": top_competitors
        }

# Example usage
if __name__ == "__main__":
    analyzer = MarketAnalyzer()
    results = analyzer.analyze_market(category="productivity")
    print(json.dumps(results, indent=2))