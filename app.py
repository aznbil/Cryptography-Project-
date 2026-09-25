import base64
import hashlib

import streamlit as st
from Crypto.Cipher import AES, ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# Konfigurasi Halaman
st.set_page_config(
    page_title="Aplikasi Kriptografi",
    page_icon="🔐",
    layout="wide",
)


def caesar_cipher(text: str, shift: int, mode: str) -> str:
    result = []
    steps = shift if mode == "encrypt" else -shift
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + steps) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def vigenere_cipher(text: str, key: str, mode: str) -> str:
    key = key.replace(" ", "").upper()
    if not key:
        raise ValueError("Kunci Vigenere tidak boleh kosong.")

    result = []
    key_index = 0
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord("A")
            if mode == "decrypt":
                shift *= -1
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


def normalize_aes_key(key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    if len(key_bytes) in (16, 24, 32):
        return key_bytes
    return hashlib.sha256(key_bytes).digest()


def aes_encrypt(plaintext: str, key: str) -> str:
    key_bytes = normalize_aes_key(key)
    iv = get_random_bytes(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def aes_decrypt(encrypted_text: str, key: str) -> str:
    key_bytes = normalize_aes_key(key)
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)
    return unpad(padded, AES.block_size).decode("utf-8")


def normalize_chacha_key(key: str) -> bytes:
    return hashlib.sha256(key.encode("utf-8")).digest()


def chacha_encrypt(plaintext: str, key: str, nonce: str) -> str:
    key_bytes = normalize_chacha_key(key)
    nonce_bytes = bytes.fromhex(nonce) if nonce else get_random_bytes(12).hex()
    if isinstance(nonce_bytes, str):
        nonce_bytes = bytes.fromhex(nonce_bytes)
    cipher = ChaCha20.new(key=key_bytes, nonce=nonce_bytes)
    ciphertext = cipher.encrypt(plaintext.encode("utf-8"))
    return base64.b64encode(nonce_bytes + ciphertext).decode("utf-8")


def chacha_decrypt(encrypted_text: str, key: str) -> str:
    key_bytes = normalize_chacha_key(key)
    encrypted_data = base64.b64decode(encrypted_text)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    cipher = ChaCha20.new(key=key_bytes, nonce=nonce)
    return cipher.decrypt(ciphertext).decode("utf-8")


def super_encrypt(plaintext: str, key: str, shift: int) -> str:
    step1 = caesar_cipher(plaintext, shift, "encrypt")
    step2 = vigenere_cipher(step1, key, "encrypt")
    step3 = aes_encrypt(step2, key)
    step4 = chacha_encrypt(step3, key, "001122334455")
    return step4


def super_decrypt(ciphertext: str, key: str, shift: int) -> str:
    step1 = chacha_decrypt(ciphertext, key)
    step2 = aes_decrypt(step1, key)
    step3 = vigenere_cipher(step2, key, "decrypt")
    step4 = caesar_cipher(step3, shift, "decrypt")
    return step4


# Sidebar Navigasi
st.sidebar.title("🔐 Menu Kriptografi")
menu = st.sidebar.selectbox(
    "Pilih Menu:",
    (
        "Beranda / Home",
        "1. Caesar Cipher",
        "2. Vigenere Cipher",
        "3. AES",
        "4. ChaCha20",
        "5. Super Enkripsi (Gabungan)",
    ),
)

# Konten Berdasarkan Menu
if menu == "Beranda / Home":
    st.title("Aplikasi Enkripsi & Dekripsi Kriptografi")
    st.markdown(
        """
        Selamat datang di aplikasi kriptografi berbasis Streamlit.

        ### Fitur utama:
        - Menu 1: Caesar Cipher
        - Menu 2: Vigenere Cipher
        - Menu 3: AES
        - Menu 4: ChaCha20
        - Menu 5: Super Enkripsi (gabungan beberapa algoritma)

        Pilih menu di sisi kiri untuk mulai menggunakan aplikasi.
        """
    )
    st.success("✅ Aplikasi siap digunakan.")

elif menu == "1. Caesar Cipher":
    st.header("Menu 1: Caesar Cipher")
    with st.form("caesar_form"):
        plaintext = st.text_area("Masukkan teks", height=150)
        shift = st.number_input("Nilai pergeseran (shift)", min_value=0, max_value=25, value=3)
        mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
        submitted = st.form_submit_button("Proses")

    if submitted and plaintext:
        result = caesar_cipher(plaintext, shift, mode)
        st.subheader("Hasil")
        st.code(result)

elif menu == "2. Vigenere Cipher":
    st.header("Menu 2: Vigenere Cipher")
    with st.form("vigenere_form"):
        plaintext = st.text_area("Masukkan teks", height=150)
        key = st.text_input("Kunci Vigenere", value="RAHASIA")
        mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
        submitted = st.form_submit_button("Proses")

    if submitted and plaintext:
        try:
            result = vigenere_cipher(plaintext, key, mode)
            st.subheader("Hasil")
            st.code(result)
        except ValueError as e:
            st.error(str(e))

elif menu == "3. AES":
    st.header("Menu 3: AES")
    with st.form("aes_form"):
        plaintext = st.text_area("Masukkan teks", height=150)
        key = st.text_input("Kunci AES", value="RahasiaKunci12345")
        mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
        submitted = st.form_submit_button("Proses")

    if submitted and plaintext:
        try:
            if mode == "encrypt":
                result = aes_encrypt(plaintext, key)
            else:
                result = aes_decrypt(plaintext, key)
            st.subheader("Hasil")
            st.code(result)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

elif menu == "4. ChaCha20":
    st.header("Menu 4: ChaCha20")
    with st.form("chacha_form"):
        plaintext = st.text_area("Masukkan teks", height=150)
        key = st.text_input("Kunci ChaCha20", value="kunci-chacha-2026-rahasia")
        nonce = st.text_input("Nonce (12 byte / 24 hex)", value="001122334455")
        mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
        submitted = st.form_submit_button("Proses")

    if submitted and plaintext:
        try:
            if mode == "encrypt":
                result = chacha_encrypt(plaintext, key, nonce)
            else:
                result = chacha_decrypt(plaintext, key)
            st.subheader("Hasil")
            st.code(result)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

elif menu == "5. Super Enkripsi (Gabungan)":
    st.header("Menu 5: Super Enkripsi (Gabungan)")
    with st.form("super_form"):
        plaintext = st.text_area("Masukkan teks", height=150)
        key = st.text_input("Kunci gabungan", value="gabungan-kriptografi")
        shift = st.number_input("Shift Caesar", min_value=0, max_value=25, value=3)
        mode = st.radio("Mode", ["encrypt", "decrypt"], horizontal=True)
        submitted = st.form_submit_button("Proses")

    if submitted and plaintext:
        try:
            if mode == "encrypt":
                result = super_encrypt(plaintext, key, shift)
            else:
                result = super_decrypt(plaintext, key, shift)
            st.subheader("Hasil")
            st.code(result)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")