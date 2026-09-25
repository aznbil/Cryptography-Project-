import streamlit as st
import importlib

# Pastikan nama file di dalam folder algorithm adalah algoritma_caesar.py
from algorithm.algoritma_caesar import caesar_encrypt, caesar_decrypt

# Import fungsi Vigenere menggunakan importlib (karena nama file mengandung tanda -)
vigenere_module = importlib.import_module("algorithm.algoritma-Vigenere")
vigenere_encrypt = vigenere_module.vigenere_encrypt
vigenere_decrypt = vigenere_module.vigenere_decrypt

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
        "3. Algoritma Modern 1",
        "4. Algoritma Modern 2",
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

elif menu == "3. Algoritma Modern 1":
    st.header("Menu 3: Algoritma Modern 1")
    st.write("implementasikan kode enkripsi/dekripsi modern pertama di sini.")

elif menu == "4. Algoritma Modern 2":
    st.header("Menu 4: Algoritma Modern 2")
    st.write("implementasikan kode enkripsi/dekripsi modern kedua di sini.")

elif menu == "5. Super Enkripsi (Gabungan)":
    st.header("Menu 5: Super Enkripsi")
    st.write("implementasikan gabungan 4 algoritma di sini.")
