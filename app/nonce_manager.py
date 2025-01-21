import os
from Crypto.Random import get_random_bytes

class NonceManager:
    NONCE_DIR = 'nonce'
    NONCE_FILE = os.path.join(NONCE_DIR, 'nonce.bin')

    @staticmethod
    def create_nonce_dir():
        """Creates a nonce folder if it does not exist."""
        if not os.path.exists(NonceManager.NONCE_DIR):
            os.makedirs(NonceManager.NONCE_DIR)

    @staticmethod
    def save_nonce(nonce):
        """Saving the nonce in nonce.bin"""
        NonceManager.create_nonce_dir()  
        with open(NonceManager.NONCE_FILE, 'wb') as f:
            f.write(nonce)

    @staticmethod
    def load_nonce():
        """Loading the nonce"""
        if os.path.exists(NonceManager.NONCE_FILE):
            with open(NonceManager.NONCE_FILE, 'rb') as f:
                return f.read()
        else:
            return None  

    @staticmethod
    def get_nonce():
        """Returning the nonce and creating new if it does not exist"""
        nonce = NonceManager.load_nonce()
        if nonce is None:
            nonce = get_random_bytes(16)  
            NonceManager.save_nonce(nonce)
        return nonce
