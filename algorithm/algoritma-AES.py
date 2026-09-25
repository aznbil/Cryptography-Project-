from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

class AESCipher:
    def __init__(self, key: bytes = None):
        """
        Inisialisasi cipher AES
        
        Args:
            key: Key AES (16, 24, atau 32 byte untuk AES-128, AES-192, AES-256)
                 Jika None, akan generate key random 32 byte (AES-256)
        """
        if key is None:
            self.key = get_random_bytes(32)  # Generate 256-bit key
        else:
            if len(key) not in [16, 24, 32]:
                raise ValueError("Key harus 16, 24, atau 32 byte")
            self.key = key
    
    def encrypt(self, plaintext: str) -> str:
        """
        Enkripsi plaintext menggunakan AES
        
        Args:
            plaintext: Teks yang ingin dienkripsi
            
        Returns:
            String base64 dari (IV + ciphertext)
        """
        # Generate random IV (Initialization Vector)
        iv = get_random_bytes(16)
        
        # Buat cipher dengan mode CBC
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Padding plaintext agar kelipatan 16 byte
        padded_plaintext = pad(plaintext.encode(), AES.block_size)
        
        # Enkripsi
        ciphertext = cipher.encrypt(padded_plaintext)
        
        # Gabung IV + ciphertext dan encode ke base64
        encrypted_data = iv + ciphertext
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Dekrips ciphertext yang dienkripsi dengan AES
        
        Args:
            encrypted_text: String base64 hasil enkripsi
            
        Returns:
            Plaintext original
        """
        try:
            # Decode dari base64
            encrypted_data = base64.b64decode(encrypted_text)
            
            # Pisahkan IV dan ciphertext
            # IV adalah 16 byte pertama
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # Buat cipher dengan IV yang sama
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Dekrips
            padded_plaintext = cipher.decrypt(ciphertext)
            
            # Hapus padding
            plaintext = unpad(padded_plaintext, AES.block_size)
            
            return plaintext.decode()
        except ValueError as e:
            raise ValueError(f"Dekrips gagal: {str(e)}")


# ==================== CONTOH PENGGUNAAN ====================

def main():
    print("=" * 50)
    print("AES Encryption & Decryption Demo")
    print("=" * 50)
    
    # Method 1: Generate key otomatis (AES-256)
    print("\n[Method 1] Menggunakan key yang di-generate")
    cipher1 = AESCipher()
    print(f"Key (hex): {cipher1.key.hex()}")
    
    plaintext = "Halo, ini adalah pesan rahasia!"
    print(f"\nPlaintext: {plaintext}")
    
    # Enkripsi
    encrypted = cipher1.encrypt(plaintext)
    print(f"Encrypted: {encrypted}")
    
    # Dekrips
    decrypted = cipher1.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Verifikasi
    print(f"Verifikasi: {plaintext == decrypted} ✓" if plaintext == decrypted else "✗")
    
    # Method 2: Menggunakan key yang sudah ditentukan
    print("\n" + "=" * 50)
    print("[Method 2] Menggunakan key yang sudah ditentukan")
    
    # Key bisa dari string atau bytes
    key_str = "MySecretKey1234567890123456789!"  # 32 karakter = 32 byte
    key = key_str.encode()  # Convert ke bytes
    print(f"Key: {key_str}")
    
    cipher2 = AESCipher(key)
    
    plaintext2 = "Pesan penting dari Ahsan"
    print(f"\nPlaintext: {plaintext2}")
    
    encrypted2 = cipher2.encrypt(plaintext2)
    print(f"Encrypted: {encrypted2}")
    
    decrypted2 = cipher2.decrypt(encrypted2)
    print(f"Decrypted: {decrypted2}")
    
    print(f"Verifikasi: {plaintext2 == decrypted2} ✓" if plaintext2 == decrypted2 else "✗")
    
    # Method 3: Enkripsi banyak pesan dengan key yang sama
    print("\n" + "=" * 50)
    print("[Method 3] Enkripsi multiple messages")
    
    messages = [
        "Pesan pertama",
        "Pesan kedua",
        "Pesan ketiga"
    ]
    
    encrypted_messages = []
    for msg in messages:
        encrypted = cipher2.encrypt(msg)
        encrypted_messages.append(encrypted)
        print(f"'{msg}' -> {encrypted[:50]}...")
    
    print("\nDekrips semua pesan:")
    for i, enc in enumerate(encrypted_messages):
        dec = cipher2.decrypt(enc)
        print(f"  {i+1}. {dec}")


if __name__ == "__main__":
    main()
