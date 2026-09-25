from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def prepare_key(key: str) -> bytes:
    """
    Menyesuaikan panjang key menjadi 16, 24, atau 32 byte.
    """
    key_bytes = key.encode('utf-8')
    if len(key_bytes) <= 16:
        return key_bytes.ljust(16, b'\0')
    elif len(key_bytes) <= 24:
        return key_bytes.ljust(24, b'\0')
    else:
        return key_bytes[:32].ljust(32, b'\0')


def aes_encrypt(text: str, key: str):
    """
    Mengenkripsi teks menggunakan AES (Mode CBC + PKCS7 Padding).
    
    Returns:
        tuple: (ciphertext_b64, steps)
    """
    if not text:
        raise ValueError("Teks tidak boleh kosong.")
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
        
    key_bytes = prepare_key(key)
    iv = get_random_bytes(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    
    text_bytes = text.encode('utf-8')
    padded_bytes = pad(text_bytes, AES.block_size)
    ciphertext_bytes = cipher.encrypt(padded_bytes)
    
    full_encrypted = iv + ciphertext_bytes
    ciphertext_b64 = base64.b64encode(full_encrypted).decode('utf-8')
    
    steps = [
        f"Kunci Asli: '{key}' ({len(key)} karakter)",
        f"Kunci Bytes (Hex): {key_bytes.hex()} ({len(key_bytes)} bytes / {len(key_bytes)*8}-bit AES)",
        f"IV (Initialization Vector Hex): {iv.hex()}",
        f"Plaintext (Hex): {text_bytes.hex()}",
        f"Padded Plaintext PKCS7 (Hex): {padded_bytes.hex()} ({len(padded_bytes)} bytes)",
        f"Ciphertext Raw (Hex): {ciphertext_bytes.hex()}",
        f"IV + Ciphertext Raw (Hex): {full_encrypted.hex()}",
        f"Hasil Akhir Base64: {ciphertext_b64}"
    ]
    
    return ciphertext_b64, steps


def aes_decrypt(encrypted_b64: str, key: str):
    """
    Mendekripsi Base64 ciphertext menggunakan AES (Mode CBC).
    
    Returns:
        tuple: (plaintext, steps)
    """
    if not encrypted_b64:
        raise ValueError("Ciphertext tidak boleh kosong.")
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
        
    key_bytes = prepare_key(key)
    
    try:
        full_encrypted = base64.b64decode(encrypted_b64)
        if len(full_encrypted) < 32:
            raise ValueError("Data terenkripsi terlalu pendek / invalid.")
            
        iv = full_encrypted[:16]
        ciphertext_bytes = full_encrypted[16:]
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext_bytes)
        plaintext_bytes = unpad(padded_plaintext, AES.block_size)
        plaintext = plaintext_bytes.decode('utf-8')
        
        steps = [
            f"Kunci Bytes (Hex): {key_bytes.hex()} ({len(key_bytes)} bytes)",
            f"Decoded Base64 (Hex): {full_encrypted.hex()}",
            f"IV Terekstraksi (Hex): {iv.hex()}",
            f"Ciphertext Raw (Hex): {ciphertext_bytes.hex()}",
            f"Padded Decrypted Bytes (Hex): {padded_plaintext.hex()}",
            f"Unpadded Plaintext Bytes (Hex): {plaintext_bytes.hex()}",
            f"Hasil Dekripsi (Plaintext): '{plaintext}'"
        ]
        
        return plaintext, steps
    except Exception as e:
        raise ValueError(f"Dekripsi AES gagal! Pastikan Kunci dan Ciphertext Base64 valid. Error: {str(e)}")
