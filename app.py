import streamlit as st

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
        "1. Algoritma Klasik 1",
        "2. Algoritma Klasik 2",
        "3. Algoritma Modern 1",
        "4. Algoritma Modern 2",
        "5. Super Enkripsi (Gabungan)"
    )
)

# Konten Berdasarkan Menu
if menu == "Beranda / Home":
    st.title("Aplikasi Enkripsi & Dekripsi Kriptografi")
    st.markdown("""
    Selamat datang di aplikasi web tugas kelompok mata kuliah Kriptografi[cite: 1].
    
    ### Fitur Aplikasi:
    - **Menu 1 & 2:** Algoritma Kriptografi Klasik[cite: 1]
    - **Menu 3 & 4:** Algoritma Kriptografi Modern[cite: 1]
    - **Menu 5:** Super Enkripsi (Gabungan 4 Algoritma)[cite: 1]
    - **Visualisasi Proses:** Menampilkan tahapan detail proses enkripsi & dekripsi[cite: 1].
    
    *Silakan pilih menu di sebelah kiri untuk mulai menggunakan aplikasi.*
    """)
    
    st.info("💡 Jangan lupa untuk memperbarui informasi anggota kelompok di file README.md.")

elif menu == "1. Algoritma Klasik 1":
    st.header("Menu 1: Algoritma Klasik 1")
    st.write("implementasikan kode enkripsi/dekripsi klasik pertama di sini.")

elif menu == "2. Algoritma Klasik 2":
    st.header("Menu 2: Algoritma Klasik 2")
    st.write("implementasikan kode enkripsi/dekripsi klasik kedua di sini.")

elif menu == "3. Algoritma Modern 1":
    st.header("Menu 3: Algoritma Modern 1")
    st.write("implementasikan kode enkripsi/dekripsi modern pertama di sini.")

elif menu == "4. Algoritma Modern 2":
    st.header("Menu 4: Algoritma Modern 2")
    st.write("implementasikan kode enkripsi/dekripsi modern kedua di sini.")

elif menu == "5. Super Enkripsi (Gabungan)":
    st.header("Menu 5: Super Enkripsi")
    st.write("implementasikan gabungan 4 algoritma di sini.")