import os
from Crypto.Random import get_random_bytes

class NonceManager:
    NONCE_DIR = 'nonce'
    NONCE_FILE = os.path.join(NONCE_DIR, 'nonce.bin')

    @staticmethod
    def get_nonce():
        """Loading the nonce"""
        if os.path.exists(NonceManager.NONCE_FILE):
            with open(NonceManager.NONCE_FILE, 'rb') as f:
                return f.read()
        else:
            return None 