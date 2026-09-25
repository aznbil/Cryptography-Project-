import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def normalize_key(key):
    if isinstance(key, str):
        key = key.encode("utf-8")

    if len(key) not in (16, 24, 32):
        key = hashlib.sha256(key).digest()

    return key


class AESCipher:
    def __init__(self, key=None):
        if key is None:
            self.key = get_random_bytes(32)
        else:
            self.key = normalize_key(key)

    def encrypt(self, plaintext: str) -> str:
        if not isinstance(plaintext, str):
            raise TypeError("Plaintext harus bertipe string.")

        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        encrypted_data = iv + ciphertext
        return base64.b64encode(encrypted_data).decode("utf-8")

    def decrypt(self, encrypted_text: str) -> str:
        if not isinstance(encrypted_text, str):
            raise TypeError("Ciphertext harus bertipe string.")

        try:
            encrypted_data = base64.b64decode(encrypted_text)
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size)
            return plaintext.decode("utf-8")
        except ValueError as exc:
            raise ValueError("Dekrips gagal: kunci atau ciphertext tidak valid.") from exc


def encrypt_aes(plaintext: str, key) -> str:
    cipher = AESCipher(key)
    return cipher.encrypt(plaintext)


def decrypt_aes(encrypted_text: str, key) -> str:
    cipher = AESCipher(key)
    return cipher.decrypt(encrypted_text)

