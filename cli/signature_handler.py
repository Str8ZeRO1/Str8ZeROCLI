#!/usr/bin/env python3
"""
Signature Handler Module
-----------------------
Securely manages digital signatures for legal documents.
"""
import os
import base64
import hashlib
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SignatureHandler:
    """Handles secure signature operations"""
    
    def __init__(self):
        """Initialize the signature handler"""
        self.secure_dir = os.path.join(Path.home(), "Str8ZeROCLI", "secure")
        self.signature_file = os.path.join(self.secure_dir, "signature.enc")
        
        # Ensure directory exists
        os.makedirs(self.secure_dir, exist_ok=True)
        
        # Initialize encryption
        self._setup_encryption()
    
    def _setup_encryption(self):
        """Set up encryption for secure storage"""
        # Use a device-specific salt (or create one if it doesn't exist)
        salt_file = os.path.join(self.secure_dir, "sig_salt.bin")
        if os.path.exists(salt_file):
            with open(salt_file, "rb") as f:
                self.salt = f.read()
        else:
            self.salt = os.urandom(16)
            with open(salt_file, "wb") as f:
                f.write(self.salt)
        
        # Use machine-specific info as password base
        machine_info = self._get_machine_info()
        password = machine_info.encode()
        
        # Generate key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher = Fernet(key)
    
    def _get_machine_info(self):
        """Get unique machine info for encryption"""
        # This is a simplified version - in production use more robust machine fingerprinting
        import platform
        import uuid
        
        # Get machine-specific identifiers
        system_info = platform.system() + platform.version()
        machine_id = str(uuid.getnode())  # MAC address as integer
        
        # Combine and hash
        combined = system_info + machine_id
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def store_signature(self, signature_data):
        """
        Securely store signature data
        
        Args:
            signature_data (bytes): The signature image data
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Encrypt the signature data
            encrypted_data = self.cipher.encrypt(signature_data)
            
            # Save to file
            with open(self.signature_file, "wb") as f:
                f.write(encrypted_data)
            
            return True
        except Exception:
            return False
    
    def get_signature(self):
        """
        Retrieve the stored signature
        
        Returns:
            bytes: The signature data, or None if not found
        """
        if not os.path.exists(self.signature_file):
            return None
        
        try:
            # Read encrypted data
            with open(self.signature_file, "rb") as f:
                encrypted_data = f.read()
            
            # Decrypt
            return self.cipher.decrypt(encrypted_data)
        except Exception:
            return None
    
    def apply_signature_to_document(self, document_path, output_path=None):
        """
        Apply the signature to a document
        
        Args:
            document_path (str): Path to the document
            output_path (str, optional): Path to save the signed document
        
        Returns:
            str: Path to the signed document
        """
        # In a real implementation, this would use a PDF library to apply the signature
        # For now, we'll just append a signature line to text documents
        
        if output_path is None:
            output_path = document_path.replace('.', '_signed.')
        
        try:
            # Read the document
            with open(document_path, 'r') as f:
                content = f.read()
            
            # Add signature line
            signature_line = f"\n\nSigned by: Alex Trujillo\nDate: {datetime.now().strftime('%Y-%m-%d')}\nSignature ID: {self._generate_signature_id()}\n"
            content += signature_line
            
            # Write the signed document
            with open(output_path, 'w') as f:
                f.write(content)
            
            return output_path
        except Exception as e:
            print(f"Error applying signature: {e}")
            return None
    
    def _generate_signature_id(self):
        """Generate a unique signature ID"""
        timestamp = datetime.now().isoformat()
        unique_id = hashlib.sha256(f"Alex Trujillo:{timestamp}".encode()).hexdigest()
        return unique_id[:16]

# Example usage
if __name__ == "__main__":
    handler = SignatureHandler()
    
    # Example: Store a signature (would normally be image data)
    # with open("signature.png", "rb") as f:
    #     signature_data = f.read()
    #     handler.store_signature(signature_data)
    
    # Example: Apply signature to a document
    # handler.apply_signature_to_document("document.txt")