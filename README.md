# Aplikasi Kriptografi - Tugas Kelompok

Aplikasi web berbasis Python menggunakan **Streamlit** untuk melakukan enkripsi dan dekripsi menggunakan berbagai algoritma kriptografi klasik, modern, serta super enkripsi[cite: 1].

## Fitur Menu Aplikasi
1. **Algoritma Klasik 1** (Caesar Cipher)
2. **Algoritma Klasik 2** (Vigener Cipher)
3. **Algoritma Modern 1** (AES)
4. **Algoritma Modern 2** (Chacha20)
5. **Super Enkripsi** (Gabungan berurutan dari 4 algoritma di atas)

Setelah menjalankan enkripsi atau dekripsi, gunakan tombol **“Sebelumnya”** dan **“Berikutnya”** untuk menelusuri proses tanpa kehilangan hasil. Vigenère menampilkan perhitungan tiap karakter, AES memperlihatkan susunan byte dan rantai XOR per blok CBC, ChaCha20 menampilkan state 4×4 beserta kelompok quarter-round, dan Super Encryption menyediakan alur serta pilihan tahap yang dapat ditelusuri.

---

## Anggota Kelompok
1. [Karina Sulistiya W] - [123240237]
2. [Aziz Nabil Putra D] - [123240239]
3. [M. Dimas Setiaji] - [123240240]
4. [M. Ahsan R.S] - [123240246]
---

## Cara Instalasi & Menjalankan Program

1. **Clone Repository ini:**
   ```bash
   git clone https://github.com/<username>/Cryptography-Project-.git 
   cd Cryptography-Project-
   ```
2. **Run the app**
   ```bash
   streamlit run app.py
   ```
