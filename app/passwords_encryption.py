import os
import hashlib
import hmac

class HashPasswords:
    @staticmethod
    def encrypt_password(password):
        salt = os.urandom(16)
        encrypted_password = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,100000)
        return salt,encrypted_password
    
    @staticmethod
    def check_password(salt, encrypted_password, password):
         return hmac.compare_digest(
            encrypted_password,
            hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        )
    
    