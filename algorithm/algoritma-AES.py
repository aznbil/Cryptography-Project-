import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, key: bytes = None):
        """
        Inisialisasi cipher AES.

        Args:
            key: Key AES 16, 24, atau 32 byte.
                 Jika None, akan generate key random 32 byte (AES-256).
        """

        if key is None:
            self.key = get_random_bytes(32)
        else:
            if len(key) not in [16, 24, 32]:
                raise ValueError("Key harus 16, 24, atau 32 byte")
            self.key = key

    def aes_encrypt(self, plaintext: str):
        """
        Enkripsi plaintext menggunakan AES-CBC.

        Returns:
            tuple:
                encrypted_text: ciphertext dalam Base64
                langkah: daftar langkah proses enkripsi
        """

        langkah = []

        # ==========================================
        # 1. Plaintext
        # ==========================================
        langkah.append("=== LANGKAH ENKRIPSI AES-CBC ===")
        langkah.append(f"1. Plaintext: {plaintext}")

        plaintext_bytes = plaintext.encode("utf-8")

        langkah.append(
            f"2. Plaintext diubah menjadi bytes: {plaintext_bytes.hex()}"
        )

        langkah.append(
            f"3. Panjang plaintext: {len(plaintext_bytes)} byte"
        )

        # ==========================================
        # 2. Informasi Key
        # ==========================================
        key_size = len(self.key) * 8

        langkah.append(
            f"4. Key AES: {self.key.hex()}"
        )

        langkah.append(
            f"5. Panjang key: {len(self.key)} byte (AES-{key_size})"
        )

        # ==========================================
        # 3. Generate IV
        # ==========================================
        iv = get_random_bytes(16)

        langkah.append(
            f"6. IV random (16 byte): {iv.hex()}"
        )

        # ==========================================
        # 4. Padding
        # ==========================================
        padded_plaintext = pad(
            plaintext_bytes,
            AES.block_size
        )

        padding_length = len(padded_plaintext) - len(plaintext_bytes)

        langkah.append(
            f"7. Padding PKCS#7 ditambahkan: {padding_length} byte"
        )

        langkah.append(
            f"8. Plaintext setelah padding: {padded_plaintext.hex()}"
        )

        langkah.append(
            f"9. Panjang data setelah padding: "
            f"{len(padded_plaintext)} byte"
        )

        # ==========================================
        # 5. AES CBC Encryption
        # ==========================================
        cipher = AES.new(
            self.key,
            AES.MODE_CBC,
            iv
        )

        ciphertext = cipher.encrypt(
            padded_plaintext
        )

        langkah.append(
            f"10. Ciphertext hasil AES-CBC: {ciphertext.hex()}"
        )

        # ==========================================
        # 6. Gabungkan IV + Ciphertext
        # ==========================================
        encrypted_data = iv + ciphertext

        langkah.append(
            f"11. IV + Ciphertext: {encrypted_data.hex()}"
        )

        # ==========================================
        # 7. Base64
        # ==========================================
        encrypted_base64 = base64.b64encode(
            encrypted_data
        ).decode("utf-8")

        langkah.append(
            f"12. Hasil akhir Base64: {encrypted_base64}"
        )

        return encrypted_base64, langkah

    def aes_decrypt(self, encrypted_text: str):
        """
        Dekripsi ciphertext Base64 menggunakan AES-CBC.

        Returns:
            tuple:
                plaintext: hasil dekripsi
                langkah: daftar langkah proses dekripsi
        """

        try:
            langkah = []

            # ==========================================
            # 1. Ciphertext Base64
            # ==========================================
            langkah.append("=== LANGKAH DEKRIPSI AES-CBC ===")

            langkah.append(
                f"1. Ciphertext Base64: {encrypted_text}"
            )

            # ==========================================
            # 2. Decode Base64
            # ==========================================
            encrypted_data = base64.b64decode(
                encrypted_text
            )

            langkah.append(
                f"2. Hasil decode Base64: {encrypted_data.hex()}"
            )

            langkah.append(
                f"3. Panjang data terenkripsi: "
                f"{len(encrypted_data)} byte"
            )

            # ==========================================
            # 3. Pisahkan IV
            # ==========================================
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

            langkah.append(
                f"4. IV (16 byte pertama): {iv.hex()}"
            )

            langkah.append(
                f"5. Ciphertext: {ciphertext.hex()}"
            )

            # ==========================================
            # 4. Informasi Key
            # ==========================================
            key_size = len(self.key) * 8

            langkah.append(
                f"6. Key AES: {self.key.hex()}"
            )

            langkah.append(
                f"7. Panjang key: "
                f"{len(self.key)} byte (AES-{key_size})"
            )

            # ==========================================
            # 5. AES CBC Decryption
            # ==========================================
            cipher = AES.new(
                self.key,
                AES.MODE_CBC,
                iv
            )

            padded_plaintext = cipher.decrypt(
                ciphertext
            )

            langkah.append(
                f"8. Hasil dekripsi sebelum unpadding: "
                f"{padded_plaintext.hex()}"
            )

            # ==========================================
            # 6. Remove Padding
            # ==========================================
            plaintext_bytes = unpad(
                padded_plaintext,
                AES.block_size
            )

            langkah.append(
                f"9. Padding PKCS#7 dihapus"
            )

            langkah.append(
                f"10. Plaintext bytes: "
                f"{plaintext_bytes.hex()}"
            )

            # ==========================================
            # 7. Bytes -> String
            # ==========================================
            plaintext = plaintext_bytes.decode(
                "utf-8"
            )

            langkah.append(
                f"11. Plaintext akhir: {plaintext}"
            )

            return plaintext, langkah

        except ValueError as e:
            raise ValueError(
                f"Dekrips gagal: {str(e)}"
            )