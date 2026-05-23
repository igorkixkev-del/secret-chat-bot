"""
Encryption module for Secret Chat Bot
Provides Fernet-based encryption for messages
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os
import base64


class EncryptionManager:
    """Manages encryption and decryption of messages"""
    
    # KDF parameters
    ITERATIONS = 100000
    ALGORITHM = hashes.SHA256()
    
    @staticmethod
    def generate_key():
        """Generate a new encryption key"""
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt for KDF (generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=EncryptionManager.ALGORITHM,
            length=32,
            salt=salt,
            iterations=EncryptionManager.ITERATIONS,
        )
        
        key_bytes = kdf.derive(password.encode())
        key = base64.urlsafe_b64encode(key_bytes)
        
        return key, salt
    
    @staticmethod
    def encrypt_message(message: str, key: bytes) -> str:
        """
        Encrypt a message using Fernet
        
        Args:
            message: Plain text message
            key: Encryption key (bytes)
            
        Returns:
            Encrypted message (string)
        """
        try:
            f = Fernet(key)
            encrypted = f.encrypt(message.encode())
            return encrypted.decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_message(encrypted_message: str, key: bytes) -> str:
        """
        Decrypt a message using Fernet
        
        Args:
            encrypted_message: Encrypted message (string)
            key: Encryption key (bytes)
            
        Returns:
            Decrypted message (string)
        """
        try:
            f = Fernet(key)
            decrypted = f.decrypt(encrypted_message.encode())
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def hash_password(password: str) -> tuple:
        """
        Hash a password for storage
        
        Args:
            password: Plain text password
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        key, salt = EncryptionManager.derive_key_from_password(password)
        return key.decode(), base64.b64encode(salt).decode()
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt_b64: str) -> bool:
        """
        Verify a password against stored hash
        
        Args:
            password: Plain text password to verify
            stored_hash: Stored password hash
            salt_b64: Stored salt (base64 encoded)
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            salt = base64.b64decode(salt_b64.encode())
            key, _ = EncryptionManager.derive_key_from_password(password, salt)
            return key.decode() == stored_hash
        except Exception:
            return False


# Convenience functions
def encrypt(message: str, key: bytes) -> str:
    """Encrypt a message"""
    return EncryptionManager.encrypt_message(message, key)


def decrypt(encrypted_message: str, key: bytes) -> str:
    """Decrypt a message"""
    return EncryptionManager.decrypt_message(encrypted_message, key)


def generate_key() -> bytes:
    """Generate a new encryption key"""
    return EncryptionManager.generate_key()
