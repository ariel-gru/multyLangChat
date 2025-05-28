import os
import hashlib
import hmac

class HashPasswords:
    @staticmethod
    def encrypt_password(password):
        """
        Encrypts the password using pbkdf2_hmac and generates a salt.
        """
        salt = os.urandom(16) # Generate a 16-byte random salt
        encrypted_password = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,100000)
        return salt,encrypted_password  # Return both the salt and the hashed password
    
    @staticmethod
    def check_password(salt, encrypted_password, password):
        """
        Checks if the provided password matches the stored hash.
        """
        return hmac.compare_digest( # Compare the stored hash with a newly computed one in constant time
            encrypted_password,
            hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000) # Recalculate the hash with the same salt and iterations
        )
    
    