from Crypto.PublicKey import DH
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

class Encryption:
    def __init__(self):
        # יצירת מפתח ציבורי ופרטי עם Diffie-Hellman
        self.key = DH.generate(2048)  # יצירת מפתח ציבורי ופרטי

    def get_public_key(self):
        return self.key.publickey()

    def generate_shared_key(self, peer_public_key):
        # יצירת המפתח המשותף
        shared_key = self.key.exchange(peer_public_key)
        # Hashing של המפתח המשותף
        shared_key = SHA256.new(shared_key).digest()
        return shared_key

    def encrypt_message(self, shared_key, message):
        # יצירת AES עם המפתח המשותף
        cipher = AES.new(shared_key, AES.MODE_CBC)
        iv = cipher.iv
        # הצפנת ההודעה עם AES
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return iv + ciphertext  # החזרת ה-IV וההודעה המוצפנת

    def decrypt_message(self, shared_key, encrypted_message):
        # חילוץ ה-IV
        iv = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = AES.new(shared_key, AES.MODE_CBC, iv=iv)
        # דהצפנת ההודעה
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return decrypted_message

# יצירת שני צדדים לצורך דוגמה
encryption_a = Encryption()
encryption_b = Encryption()

# שליחת המפתח הציבורי של כל צד לשני
public_key_a = encryption_a.get_public_key()
public_key_b = encryption_b.get_public_key()

# כל צד מחשב את המפתח המשותף
shared_key_a = encryption_a.generate_shared_key(public_key_b)
shared_key_b = encryption_b.generate_shared_key(public_key_a)

# כל צד מצפין את ההודעה
message = "Hello from A to B"
encrypted_message = encryption_a.encrypt_message(shared_key_a, message)

# צד B דהצפין את ההודעה
decrypted_message = encryption_b.decrypt_message(shared_key_b, encrypted_message)

print(f"Decrypted message: {decrypted_message}")
