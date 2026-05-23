"""
Unit tests for encryption module
"""
import unittest
from crypto import EncryptionManager, encrypt, decrypt, generate_key


class TestEncryptionManager(unittest.TestCase):
    """Test cases for EncryptionManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.key = generate_key()
        self.test_message = "This is a secret message for testing!"
    
    def test_generate_key(self):
        """Test key generation"""
        key1 = generate_key()
        key2 = generate_key()
        
        self.assertIsNotNone(key1)
        self.assertIsNotNone(key2)
        self.assertNotEqual(key1, key2)
        self.assertIsInstance(key1, bytes)
    
    def test_encrypt_message(self):
        """Test message encryption"""
        encrypted = EncryptionManager.encrypt_message(self.test_message, self.key)
        
        self.assertIsNotNone(encrypted)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, self.test_message)
    
    def test_decrypt_message(self):
        """Test message decryption"""
        encrypted = EncryptionManager.encrypt_message(self.test_message, self.key)
        decrypted = EncryptionManager.decrypt_message(encrypted, self.key)
        
        self.assertEqual(decrypted, self.test_message)
    
    def test_decrypt_with_wrong_key(self):
        """Test decryption with wrong key fails"""
        encrypted = EncryptionManager.encrypt_message(self.test_message, self.key)
        wrong_key = generate_key()
        
        with self.assertRaises(ValueError):
            EncryptionManager.decrypt_message(encrypted, wrong_key)
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        encrypted = encrypt(self.test_message, self.key)
        decrypted = decrypt(encrypted, self.key)
        
        self.assertEqual(decrypted, self.test_message)
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "SecurePassword123!"
        hash1, salt1 = EncryptionManager.hash_password(password)
        hash2, salt2 = EncryptionManager.hash_password(password)
        
        self.assertIsNotNone(hash1)
        self.assertIsNotNone(salt1)
        # Different salts should produce different hashes
        self.assertNotEqual(hash1, hash2)
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "SecurePassword123!"
        password_hash, salt = EncryptionManager.hash_password(password)
        
        result = EncryptionManager.verify_password(password, password_hash, salt)
        self.assertTrue(result)
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "SecurePassword123!"
        password_hash, salt = EncryptionManager.hash_password(password)
        
        result = EncryptionManager.verify_password("WrongPassword", password_hash, salt)
        self.assertFalse(result)
    
    def test_encrypt_empty_message(self):
        """Test encrypting empty message"""
        encrypted = EncryptionManager.encrypt_message("", self.key)
        decrypted = EncryptionManager.decrypt_message(encrypted, self.key)
        
        self.assertEqual(decrypted, "")
    
    def test_encrypt_long_message(self):
        """Test encrypting long message"""
        long_message = "A" * 10000
        encrypted = EncryptionManager.encrypt_message(long_message, self.key)
        decrypted = EncryptionManager.decrypt_message(encrypted, self.key)
        
        self.assertEqual(decrypted, long_message)
    
    def test_encrypt_special_characters(self):
        """Test encrypting message with special characters"""
        special_message = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>? 中文 🔐"
        encrypted = EncryptionManager.encrypt_message(special_message, self.key)
        decrypted = EncryptionManager.decrypt_message(encrypted, self.key)
        
        self.assertEqual(decrypted, special_message)


if __name__ == '__main__':
    unittest.main()
