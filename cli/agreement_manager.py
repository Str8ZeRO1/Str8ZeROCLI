#!/usr/bin/env python3
"""
Agreement Manager Module
-----------------------
Handles legal agreements and partnership setup.
"""
import os
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

class AgreementManager:
    """Manages legal agreements and partnerships"""
    
    def __init__(self):
        """Initialize the agreement manager"""
        self.legal_dir = os.path.join(Path.home(), "Str8ZeROCLI", "legal")
        self.agreements_file = os.path.join(self.legal_dir, "agreements.json")
        
        # Ensure directory exists
        os.makedirs(self.legal_dir, exist_ok=True)
        
        # Load existing agreements
        self.agreements = self._load_agreements()
        
    def _load_agreements(self):
        """Load existing agreements from file"""
        if os.path.exists(self.agreements_file):
            try:
                with open(self.agreements_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_agreements(self):
        """Save agreements to file"""
        with open(self.agreements_file, 'w') as f:
            json.dump(self.agreements, f, indent=2)
    
    def get_partnership_agreement(self):
        """Get the partnership agreement text"""
        agreement_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "legal", "partnership_agreement.md")
        
        if os.path.exists(agreement_path):
            with open(agreement_path, 'r') as f:
                return f.read()
        else:
            return "Partnership agreement not found."
    
    def present_agreement(self):
        """Present the partnership agreement to the user"""
        agreement_text = self.get_partnership_agreement()
        
        print("\n" + "=" * 80)
        print("REVENUE SHARING PARTNERSHIP AGREEMENT")
        print("=" * 80 + "\n")
        
        # Print the agreement in chunks for readability
        chunk_size = 20
        lines = agreement_text.split('\n')
        for i in range(0, len(lines), chunk_size):
            print('\n'.join(lines[i:i+chunk_size]))
            if i + chunk_size < len(lines):
                input("\nPress Enter to continue...")
        
        print("\n" + "=" * 80)
        print("By using Str8ZeROCLI, you agree to the terms of this partnership agreement.")
        print("=" * 80 + "\n")
        
        return input("Do you accept the terms of this agreement? (yes/no): ").lower().strip() == 'yes'
    
    def record_agreement(self, partner_id, partner_name=None, partner_email=None):
        """Record a partner's agreement to the terms"""
        timestamp = datetime.now().isoformat()
        
        # Create a unique agreement ID
        agreement_id = hashlib.sha256(f"{partner_id}:{timestamp}".encode()).hexdigest()
        
        # Record the agreement
        agreement = {
            "agreement_id": agreement_id,
            "partner_id": partner_id,
            "partner_name": partner_name,
            "partner_email": partner_email,
            "timestamp": timestamp,
            "agreement_version": "1.0",
            "agreement_type": "revenue_sharing",
            "revenue_share": 50,  # 50% to owner, 50% to partner
            "status": "active"
        }
        
        self.agreements.append(agreement)
        self._save_agreements()
        
        return agreement_id
    
    def verify_agreement(self, partner_id):
        """Verify if a partner has agreed to the terms"""
        for agreement in self.agreements:
            if agreement["partner_id"] == partner_id and agreement["status"] == "active":
                return True
        return False
    
    def terminate_agreement(self, agreement_id, reason=None):
        """Terminate an agreement"""
        for agreement in self.agreements:
            if agreement["agreement_id"] == agreement_id:
                agreement["status"] = "terminated"
                agreement["termination_date"] = datetime.now().isoformat()
                agreement["termination_reason"] = reason
                self._save_agreements()
                return True
        return False

# Example usage
if __name__ == "__main__":
    manager = AgreementManager()
    
    # Present agreement
    if manager.present_agreement():
        # Record agreement
        agreement_id = manager.record_agreement(
            partner_id="test_user_123",
            partner_name="Test User",
            partner_email="test@example.com"
        )
        print(f"Agreement recorded with ID: {agreement_id}")
    else:
        print("Agreement not accepted. You cannot use Str8ZeROCLI without accepting the terms.")