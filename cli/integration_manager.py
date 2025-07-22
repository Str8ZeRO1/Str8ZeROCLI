#!/usr/bin/env python3
"""
Integration Manager Module
-------------------------
Integrates all components of the Str8ZeROCLI system.
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Import core modules
from cli.str8zero_core import Str8ZeroCore
from cli.market_analysis import MarketAnalyzer
from cli.app_generator import AppGenerator
from cli.secure_payment import SecurePaymentProcessor
from cli.agreement_manager import AgreementManager
from cli.signature_handler import SignatureHandler

class IntegrationManager:
    """Manages integration of all Str8ZeROCLI components"""
    
    def __init__(self):
        """Initialize the integration manager"""
        self.config_dir = os.path.join(Path.home(), "Str8ZeROCLI", "config")
        self.data_dir = os.path.join(Path.home(), "Str8ZeROCLI", "data")
        
        # Ensure directories exist
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components
        self.payment_processor = SecurePaymentProcessor()
        self.agreement_manager = AgreementManager()
        self.signature_handler = SignatureHandler()
        
        # Check if system is initialized
        self.initialized = self._check_initialization()
        
    def _check_initialization(self):
        """Check if the system is initialized"""
        init_file = os.path.join(self.config_dir, "initialized.json")
        if os.path.exists(init_file):
            try:
                with open(init_file, 'r') as f:
                    init_data = json.load(f)
                return init_data.get("initialized", False)
            except:
                pass
        return False
    
    def initialize_system(self, owner_info=None):
        """Initialize the system with owner information"""
        if owner_info is None:
            owner_info = {
                "name": "Alex Trujillo",
                "brand": "Str8ZeRO",
                "email": "alex@str8zero.com"
            }
        
        # Record initialization
        init_file = os.path.join(self.config_dir, "initialized.json")
        init_data = {
            "initialized": True,
            "timestamp": datetime.now().isoformat(),
            "owner": owner_info
        }
        
        with open(init_file, 'w') as f:
            json.dump(init_data, f, indent=2)
        
        self.initialized = True
        return True
    
    def process_new_user(self, user_id, user_info=None):
        """Process a new user of the system"""
        # Present partnership agreement
        if self.agreement_manager.present_agreement():
            # Record agreement
            agreement_id = self.agreement_manager.record_agreement(
                partner_id=user_id,
                partner_name=user_info.get("name") if user_info else None,
                partner_email=user_info.get("email") if user_info else None
            )
            
            return {
                "success": True,
                "agreement_id": agreement_id,
                "message": "Partnership agreement accepted."
            }
        else:
            return {
                "success": False,
                "message": "Partnership agreement not accepted. You cannot use Str8ZeROCLI without accepting the terms."
            }
    
    def generate_app(self, user_id, app_name, app_type, features=None, platform="all"):
        """Generate an app with revenue sharing setup"""
        # Verify user agreement
        if not self.agreement_manager.verify_agreement(user_id):
            return {
                "success": False,
                "message": "You must accept the partnership agreement before generating apps."
            }
        
        # Generate the app
        generator = AppGenerator()
        result = generator.generate_app(app_name, app_type, features, platform)
        
        # Set up revenue sharing
        app_id = f"app_{app_name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
        revenue_setup = self.payment_processor.setup_revenue_sharing(
            app_id=app_id,
            partner_stripe_account=f"partner_{user_id}"  # This would be the actual Stripe account in production
        )
        
        # Add revenue sharing info to result
        result["revenue_sharing"] = {
            "app_id": app_id,
            "owner_share": revenue_setup.get("owner_share", 50),
            "partner_share": revenue_setup.get("partner_share", 50)
        }
        
        return result
    
    def analyze_market_with_agreement(self, user_id, category=None, keywords=None):
        """Analyze market with agreement verification"""
        # Verify user agreement
        if not self.agreement_manager.verify_agreement(user_id):
            return {
                "success": False,
                "message": "You must accept the partnership agreement before using market analysis."
            }
        
        # Analyze market
        analyzer = MarketAnalyzer()
        result = analyzer.analyze_market(category, keywords)
        
        return result
    
    def process_revenue(self, app_id, amount):
        """Process revenue for an app"""
        result = self.payment_processor.process_revenue_share(amount, app_id)
        
        if result.get("success", False):
            # Log the transaction
            transaction_log = os.path.join(self.data_dir, "transactions.json")
            
            transactions = []
            if os.path.exists(transaction_log):
                try:
                    with open(transaction_log, 'r') as f:
                        transactions = json.load(f)
                except:
                    transactions = []
            
            transactions.append({
                "timestamp": datetime.now().isoformat(),
                "app_id": app_id,
                "amount": amount,
                "owner_amount": result.get("owner_amount"),
                "partner_amount": result.get("partner_amount")
            })
            
            with open(transaction_log, 'w') as f:
                json.dump(transactions, f, indent=2)
        
        return result

# Example usage
if __name__ == "__main__":
    manager = IntegrationManager()
    
    # Initialize system if needed
    if not manager.initialized:
        manager.initialize_system()
        print("System initialized.")
    
    # Process a new user
    result = manager.process_new_user(
        user_id="test_user_123",
        user_info={
            "name": "Test User",
            "email": "test@example.com"
        }
    )
    
    if result.get("success", False):
        # Generate an app
        app_result = manager.generate_app(
            user_id="test_user_123",
            app_name="Test App",
            app_type="bill_monitor",
            features=["bill_upload", "anomaly_detection"]
        )
        
        print(f"App generated: {app_result.get('app_name')}")
        print(f"Revenue sharing: {app_result.get('revenue_sharing')}")
    else:
        print(result.get("message"))