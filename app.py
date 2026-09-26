import streamlit as st
import importlib

# Import algoritma caesar
from algorithm.algoritma_caesar import caesar_encrypt, caesar_decrypt

# Import fungsi Vigenere menggunakan importlib (karena nama file mengandung tanda -)
vigenere_module = importlib.import_module("algorithm.algoritma-Vigenere")
vigenere_encrypt = vigenere_module.vigenere_encrypt
vigenere_decrypt = vigenere_module.vigenere_decrypt

# Import fungsi AES menggunakan importlib (karena nama file mengandung tanda -)
# aes_encrypt = AESCipher.aes_encrypt
# aes_decrypt = AESCipher.aes_decrypt
aes_module = importlib.import_module("algorithm.algoritma-AES")
AESCipher = aes_module.AESCipher


# Import fungsi ChaCha20 menggunakan importlib (karena nama file mengandung tanda -)
chacha_module = importlib.import_module("algorithm.algoritma-Chacha20")
chacha20_encrypt = chacha_module.chacha20_encrypt
chacha20_decrypt = chacha_module.chacha20_decrypt

# Konfigurasi Halaman
st.set_page_config(
    page_title="Aplikasi Kriptografi",
    page_icon="🔐",
    layout="wide"
)

# Sidebar Navigasi
st.sidebar.title("🔐 Menu Kriptografi")
menu = st.sidebar.selectbox(
    "Pilih Menu:",
    (
        "Beranda / Home",
        "1. Algoritma Klasik 1 (Caesar Cipher)",
        "2. Algoritma Klasik 2 (Vigenère Cipher)",
        "3. Algoritma Modern 1 (AES)",
        "4. Algoritma Modern 2 (ChaCha20)",
        "5. Super Enkripsi (Gabungan)"
    )
)

# Konten Berdasarkan Menu
if menu == "Beranda / Home":
    st.title("Aplikasi Enkripsi & Dekripsi Kriptografi")
    st.markdown("""
    Selamat datang di aplikasi web tugas kelompok mata kuliah Kriptografi.
    
    ### Fitur Aplikasi:
    - **Menu 1 & 2:** Algoritma Kriptografi Klasik
    - **Menu 3 & 4:** Algoritma Kriptografi Modern
    - **Menu 5:** Super Enkripsi (Gabungan 4 Algoritma)
    - **Visualisasi Proses:** Menampilkan tahapan detail proses enkripsi & dekripsi.
    
    *Silakan pilih menu di sebelah kiri untuk mulai menggunakan aplikasi.*
    """)
    
    st.info("💡 Jangan lupa untuk memperbarui informasi anggota kelompok di file README.md.")

elif menu == "1. Algoritma Klasik 1 (Caesar Cipher)":
    st.header("Menu 1: Caesar Cipher")
    st.write("Algoritma substitusi klasik yang menggeser posisi huruf pada alfabet. Algoritma ini sangat rentan terhadap serangan Brute Force karena hanya memiliki 25 kemungkinan kunci.")

    # Form Input dari user
    teks = st.text_area("Masukkan Teks (Plaintext / Ciphertext):", height=100)
    shift = st.number_input("Masukkan Kunci Pergeseran (Shift / N):", min_value=1, max_value=25, value=3)

    # Membagi layout menjadi 3 kolom untuk tombol Encrypt, Decrypt, dan Brute Force
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔒 Encrypt (Enkripsi)", use_container_width=True):
            if teks:
                hasil, langkah = caesar_encrypt(teks, shift)
                st.success("Teks Berhasil Dienkripsi!")
                st.text_input("Hasil Ciphertext:", value=hasil, disabled=True)

                with st.expander("Tampilkan Langkah-langkah Enkripsi"):
                    for step in langkah:
                        st.write(f"- {step}")
            else:
                st.warning("Silakan masukkan teks terlebih dahulu.")

    with col2:
        if st.button("🔓 Decrypt (Dekripsi)", use_container_width=True):
            if teks:
                hasil, langkah = caesar_decrypt(teks, shift)
                st.success("Teks Berhasil Didekripsi!")
                st.text_input("Hasil Plaintext:", value=hasil, disabled=True)

                with st.expander("Tampilkan Langkah-langkah Dekripsi"):
                    for step in langkah:
                        st.write(f"- {step}")
            else:
                st.warning("Silakan masukkan teks terlebih dahulu.")

    with col3:
        if st.button("🔍 Brute Force", use_container_width=True, type="primary"):
            if teks:
                st.warning("Menjalankan serangan Brute Force (menguji 25 kemungkinan kunci)...")

                # Menggunakan expander yang langsung terbuka agar hasilnya rapi
                with st.expander("Lihat Hasil Brute Force (Shift 1 - 25)", expanded=True):
                    # Looping dari pergeseran 1 sampai 25
                    for i in range(1, 26):
                        # Kita abaikan variabel 'langkah' menggunakan underscore (_)
                        # karena untuk brute force kita hanya butuh hasil akhirnya saja
                        hasil_brute, _ = caesar_decrypt(teks, i)
                        st.markdown(f"**Key {i}:** {hasil_brute}")
            else:
                st.warning("Silakan masukkan ciphertext terlebih dahulu.")

elif menu == "2. Algoritma Klasik 2 (Vigenère Cipher)":
    st.header("Menu 2: Vigenère Cipher")
    st.write("Algoritma substitusi polialfabetik yang menggunakan kata kunci (*key*) untuk menggeser karakter. Setiap huruf pada pesan dienkripsi dengan pergeseran yang berbeda sesuai huruf kunci yang bersangkutan.")

    teks_vigenere = st.text_area("Masukkan Teks (Plaintext / Ciphertext):", height=100, key="vigenere_text")
    kunci_vigenere = st.text_input("Masukkan Kata Kunci (Key):", value="KEY", key="vigenere_key")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Encrypt (Enkripsi)", use_container_width=True, key="vigenere_enc_btn"):
            if teks_vigenere and kunci_vigenere:
                try:
                    hasil, langkah = vigenere_encrypt(teks_vigenere, kunci_vigenere)
                    st.success("Teks Berhasil Dienkripsi!")
                    st.text_input("Hasil Ciphertext:", value=hasil, disabled=True, key="vigenere_res_enc")

                    with st.expander("Tampilkan Langkah-langkah Enkripsi", expanded=True):
                        st.dataframe(langkah, use_container_width=True)
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Silakan masukkan teks dan kata kunci terlebih dahulu.")

    with col2:
        if st.button("🔓 Decrypt (Dekripsi)", use_container_width=True, key="vigenere_dec_btn"):
            if teks_vigenere and kunci_vigenere:
                try:
                    hasil, langkah = vigenere_decrypt(teks_vigenere, kunci_vigenere)
                    st.success("Teks Berhasil Didekripsi!")
                    st.text_input("Hasil Plaintext:", value=hasil, disabled=True, key="vigenere_res_dec")

                    with st.expander("Tampilkan Langkah-langkah Dekripsi", expanded=True):
                        st.dataframe(langkah, use_container_width=True)
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Silakan masukkan teks dan kata kunci terlebih dahulu.")

elif menu == "3. Algoritma Modern 1 (AES)":

    st.header("Menu 3: AES (Advanced Encryption Standard)")

    st.write(
        "Algoritma simetris block cipher modern menggunakan "
        "mode CBC (Cipher Block Chaining) dan padding PKCS7."
    )

    # =========================
    # INPUT AES
    # =========================

    teks_aes = st.text_area(
        "Masukkan Teks (Plaintext / Base64 Ciphertext):",
        height=100,
        key="aes_text"
    )

    kunci_aes = st.text_input(
        "Masukkan Kunci AES:",
        type="password",
        help="Kunci harus memiliki panjang 16, 24, atau 32 byte.",
        key="aes_key"
    )

    col1, col2 = st.columns(2)

    # =========================
    # ENCRYPT
    # =========================

    with col1:

        if st.button(
            "🔒 Encrypt (Enkripsi)",
            use_container_width=True,
            key="aes_enc_btn"
        ):

            if teks_aes and kunci_aes:

                try:

                    # Convert key string -> bytes
                    key_bytes = kunci_aes.encode("utf-8")

                    # Validasi panjang key
                    if len(key_bytes) not in [16, 24, 32]:

                        st.error(
                            f"Key harus 16, 24, atau 32 byte. "
                            f"Key kamu sekarang {len(key_bytes)} byte."
                        )

                    else:

                        # Buat object AES menggunakan key dari user
                        cipher = AESCipher(key_bytes)

                        # Encrypt
                        hasil, langkah = cipher.aes_encrypt(
                            teks_aes
                        )

                        st.success(
                            "Teks berhasil dienkripsi dengan AES CBC!"
                        )

                        # =========================
                        # OUTPUT CIPHERTEXT
                        # =========================

                        st.text_area(
                            "Hasil Ciphertext (Base64):",
                            value=hasil,
                            height=100,
                            key="aes_res_enc"
                        )

                        # =========================
                        # OUTPUT LANGKAH
                        # =========================

                        with st.expander(
                            "🔍 Tampilkan Langkah-Langkah Enkripsi AES",
                            expanded=True
                        ):

                            for i, step in enumerate(langkah, start=1):

                                st.write(
                                    f"**Langkah {i}:** {step}"
                                )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {str(e)}"
                    )

            else:

                st.warning(
                    "Silakan masukkan teks dan kunci terlebih dahulu."
                )

    # =========================
    # DECRYPT
    # =========================

    with col2:

        if st.button(
            "🔓 Decrypt (Dekripsi)",
            use_container_width=True,
            key="aes_dec_btn"
        ):

            if teks_aes and kunci_aes:

                try:

                    # Convert key string -> bytes
                    key_bytes = kunci_aes.encode("utf-8")

                    # Validasi panjang key
                    if len(key_bytes) not in [16, 24, 32]:

                        st.error(
                            f"Key harus 16, 24, atau 32 byte. "
                            f"Key kamu sekarang {len(key_bytes)} byte."
                        )

                    else:

                        # Buat object AES
                        cipher = AESCipher(key_bytes)

                        # Decrypt
                        hasil, langkah = cipher.aes_decrypt(
                            teks_aes
                        )

                        st.success(
                            "Teks berhasil didekripsi dengan AES CBC!"
                        )

                        # =========================
                        # OUTPUT PLAINTEXT
                        # =========================

                        st.text_area(
                            "Hasil Plaintext:",
                            value=hasil,
                            height=100,
                            key="aes_res_dec"
                        )

                        # =========================
                        # OUTPUT LANGKAH
                        # =========================

                        with st.expander(
                            "🔍 Tampilkan Langkah-Langkah Dekripsi AES",
                            expanded=True
                        ):

                            for i, step in enumerate(langkah, start=1):

                                st.write(
                                    f"**Langkah {i}:** {step}"
                                )

                except Exception as e:

                    st.error(
                        f"Terjadi kesalahan: {str(e)}"
                    )

            else:

                st.warning(
                    "Silakan masukkan ciphertext Base64 dan kunci terlebih dahulu."
                )

elif menu == "4. Algoritma Modern 2 (ChaCha20)":
    st.header("Menu 4: ChaCha20 Stream Cipher")
    st.write("Algoritma kriptografi simetris tipe *stream cipher* modern yang sangat cepat dan aman. Menggunakan state matrix 4x4 (64 bytes) serta melakukan 20 putaran *quarter-round* (ARX: Addition, Rotation, XOR).")

    teks_chacha = st.text_area("Masukkan Teks (Plaintext / Base64 Ciphertext):", height=100, key="chacha_text")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        kunci_chacha = st.text_input("Kunci / Key (32 Byte / 64 Hex):", value="000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f", key="chacha_key")
    with col_k2:
        nonce_chacha = st.text_input("Nonce (12 Byte / 24 Hex):", value="000000000000000000000000", key="chacha_nonce")
    with col_k3:
        counter_chacha = st.number_input("Counter Awal:", min_value=0, max_value=4294967295, value=1, key="chacha_counter")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Encrypt (Enkripsi)", use_container_width=True, key="chacha_enc_btn"):
            if teks_chacha and kunci_chacha and nonce_chacha:
                try:
                    hasil, langkah = chacha20_encrypt(teks_chacha, kunci_chacha, nonce_chacha, int(counter_chacha))
                    st.success("Teks Berhasil Dienkripsi dengan ChaCha20!")
                    st.text_area("Hasil Ciphertext (Base64):", value=hasil, height=100, key="chacha_res_enc")

                    with st.expander("Tampilkan Detail Langkah State & Double Round ChaCha20", expanded=True):
                        for step in langkah:
                            if "\n" in step:
                                st.text(step)
                            else:
                                st.write(f"- {step}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")
            else:
                st.warning("Silakan masukkan teks, key, dan nonce terlebih dahulu.")

    with col2:
        if st.button("🔓 Decrypt (Dekripsi)", use_container_width=True, key="chacha_dec_btn"):
            if teks_chacha and kunci_chacha and nonce_chacha:
                try:
                    hasil, langkah = chacha20_decrypt(teks_chacha, kunci_chacha, nonce_chacha, int(counter_chacha))
                    st.success("Teks Berhasil Didekripsi dengan ChaCha20!")
                    st.text_area("Hasil Plaintext:", value=hasil, height=100, key="chacha_res_dec")

                    with st.expander("Tampilkan Detail Langkah State & Double Round ChaCha20", expanded=True):
                        for step in langkah:
                            if "\n" in step:
                                st.text(step)
                            else:
                                st.write(f"- {step}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")
            else:
                st.warning("Silakan masukkan ciphertext Base64, key, dan nonce terlebih dahulu.")

elif menu == "5. Super Enkripsi (Gabungan)":
    st.header("Menu 5: Super Enkripsi (Gabungan 4 Algoritma)")
    st.write("Super Enkripsi ini menggabungkan 4 algoritma secara berturut-turut: **Caesar Cipher ➔ Vigenère Cipher ➔ AES ➔ ChaCha20** (Enkripsi) dan alur kebalikannya saat Dekripsi.")

    teks_super = st.text_area("Masukkan Teks (Plaintext / Super Ciphertext):", height=100, key="super_text")

    st.subheader("🔑 Konfigurasi Kunci & Parameter 4 Algoritma")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        shift_super = st.number_input("1. Caesar Shift (N):", min_value=1, max_value=25, value=3, key="super_shift")
        kunci_vigenere_super = st.text_input("2. Kunci Vigenère:", value="KEY", key="super_vig_key")
        kunci_aes_super = st.text_input("3. Kunci AES:", value="MySecretKey123456", key="super_aes_key")
    
    with col_k2:
        kunci_chacha_super = st.text_input("4a. Kunci ChaCha20 (64 Hex):", value="000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f", key="super_chacha_key")
        nonce_chacha_super = st.text_input("4b. Nonce ChaCha20 (24 Hex):", value="000000000000000000000000", key="super_chacha_nonce")
        counter_chacha_super = st.number_input("4c. Counter ChaCha20:", min_value=0, max_value=4294967295, value=1, key="super_chacha_counter")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Super Encrypt (Enkripsi 4 Tahap)", use_container_width=True, type="primary", key="super_enc_btn"):
            if teks_super:
                try:
                    aes_cipher = AESCipher(
                    kunci_aes_super.encode("utf-8")
                    )
                    # 1. Caesar Encrypt
                    t1, _ = caesar_encrypt(teks_super, shift_super)
                    # 2. Vigenere Encrypt
                    t2, _ = vigenere_encrypt(t1, kunci_vigenere_super)
                    # 3. AES Encrypt
                    t3, _ = aes_cipher.aes_encrypt(t2)
                    # 4. ChaCha20 Encrypt
                    final_ciphertext, _ = chacha20_encrypt(t3, kunci_chacha_super, nonce_chacha_super, int(counter_chacha_super))

                    st.success("Super Enkripsi 4 Tahap Berhasil Selesai!")
                    st.text_area("Hasil Super Ciphertext (Final Base64):", value=final_ciphertext, height=120, key="super_res_enc")

                    with st.expander("Lihat Alur Hasil Setiap Tahap (Caesar ➔ Vigenère ➔ AES ➔ ChaCha20)", expanded=True):
                        st.markdown(f"**Plaintext Awal:** `{teks_super}`")
                        st.markdown(f"**Tahap 1 (Caesar Cipher):** `{t1}`")
                        st.markdown(f"**Tahap 2 (Vigenère Cipher):** `{t2}`")
                        st.markdown(f"**Tahap 3 (AES CBC Base64):** `{t3}`")
                        st.markdown(f"**Tahap 4 (ChaCha20 Final Base64):** `{final_ciphertext}`")
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada Super Enkripsi: {str(e)}")
            else:
                st.warning("Silakan masukkan teks terlebih dahulu.")

    with col2:
        if st.button("🔓 Super Decrypt (Dekripsi 4 Tahap)", use_container_width=True, key="super_dec_btn"):
            if teks_super:
                try:
                    aes_cipher = AESCipher(
                    kunci_aes_super.encode("utf-8")
                    )
                    # 1. ChaCha20 Decrypt
                    d3, _ = chacha20_decrypt(teks_super, kunci_chacha_super, nonce_chacha_super, int(counter_chacha_super))
                    # 2. AES Decrypt
                    d2, _ =  aes_cipher.aes_decrypt(d3)
                    # 3. Vigenere Decrypt
                    d1, _ = vigenere_decrypt(d2, kunci_vigenere_super)
                    # 4. Caesar Decrypt
                    original_plaintext, _ = caesar_decrypt(d1, shift_super)

                    st.success("Super Dekripsi 4 Tahap Berhasil Selesai!")
                    st.text_area("Hasil Plaintext Asli:", value=original_plaintext, height=120, key="super_res_dec")

                    with st.expander("Lihat Alur Dekripsi Setiap Tahap (ChaCha20 ➔ AES ➔ Vigenère ➔ Caesar)", expanded=True):
                        st.markdown(f"**Super Ciphertext Input:** `{teks_super}`")
                        st.markdown(f"**Tahap 1 Dekripsi (ChaCha20 ➔ AES Base64):** `{d3}`")
                        st.markdown(f"**Tahap 2 Dekripsi (AES ➔ Vigenère Text):** `{d2}`")
                        st.markdown(f"**Tahap 3 Dekripsi (Vigenère ➔ Caesar Text):** `{d1}`")
                        st.markdown(f"**Tahap 4 Dekripsi (Caesar ➔ Plaintext Asli):** `{original_plaintext}`")
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada Super Dekripsi: {str(e)}")
            else:
                st.warning("Silakan masukkan super ciphertext terlebih dahulu.")
