"""
Algoritma Vigenère Cipher (Enkripsi dan Dekripsi)
Lengkap dengan pencatatan dan penampil langkah-langkah perhitungan matematika.
"""

def vigenere_encrypt(text: str, key: str):
    """
    Mengenkripsi teks menggunakan Algoritma Vigenère Cipher.
    
    Rumus Enkripsi: C_i = (P_i + K_i) mod 26
    
    Returns:
        tuple: (ciphertext, steps)
    """
    ciphertext = ""
    steps = []
    
    # Menghapus karakter non-alfabet pada kunci dan diubah ke huruf kapital
    clean_key = ''.join([c.upper() for c in key if c.isalpha()])
    if not clean_key:
        raise ValueError("Kunci harus mengandung setidaknya satu huruf alfabet.")
        
    key_idx = 0
    
    for char in text:
        if char.isalpha():
            base_val = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base_val  # Indeks Plaintext (0-25)
            
            k_char = clean_key[key_idx % len(clean_key)]
            k_val = ord(k_char) - ord('A')  # Indeks Kunci (0-25)
            
            c_val = (p_val + k_val) % 26     # Rumus Enkripsi
            c_char = chr(c_val + base_val)
            
            ciphertext += c_char
            
            steps.append({
                'no': len(steps) + 1,
                'char': char,
                'p_val': p_val,
                'key_char': k_char,
                'k_val': k_val,
                'formula': f"({p_val} + {k_val}) mod 26 = {c_val}",
                'result_char': c_char
            })
            key_idx += 1
        else:
            # Karakter non-alfabet (spasi, angka, tanda baca) diabaikan/diteruskan
            ciphertext += char
            steps.append({
                'no': len(steps) + 1,
                'char': char,
                'p_val': '-',
                'key_char': '-',
                'k_val': '-',
                'formula': 'Abaikan (Non-Alfabet)',
                'result_char': char
            })
            
    return ciphertext, steps


def vigenere_decrypt(text: str, key: str):
    """
    Mendekripsi teks menggunakan Algoritma Vigenère Cipher.
    
    Rumus Dekripsi: P_i = (C_i - K_i + 26) mod 26
    
    Returns:
        tuple: (plaintext, steps)
    """
    plaintext = ""
    steps = []
    
    # Menghapus karakter non-alfabet pada kunci dan diubah ke huruf kapital
    clean_key = ''.join([c.upper() for c in key if c.isalpha()])
    if not clean_key:
        raise ValueError("Kunci harus mengandung setidaknya satu huruf alfabet.")
        
    key_idx = 0
    
    for char in text:
        if char.isalpha():
            base_val = ord('A') if char.isupper() else ord('a')
            c_val = ord(char) - base_val  # Indeks Ciphertext (0-25)
            
            k_char = clean_key[key_idx % len(clean_key)]
            k_val = ord(k_char) - ord('A')  # Indeks Kunci (0-25)
            
            p_val = (c_val - k_val + 26) % 26  # Rumus Dekripsi
            p_char = chr(p_val + base_val)
            
            plaintext += p_char
            
            steps.append({
                'no': len(steps) + 1,
                'char': char,
                'c_val': c_val,
                'key_char': k_char,
                'k_val': k_val,
                'formula': f"({c_val} - {k_val} + 26) mod 26 = {p_val}",
                'result_char': p_char
            })
            key_idx += 1
        else:
            plaintext += char
            steps.append({
                'no': len(steps) + 1,
                'char': char,
                'c_val': '-',
                'key_char': '-',
                'k_val': '-',
                'formula': 'Abaikan (Non-Alfabet)',
                'result_char': char
            })
            
    return plaintext, steps


def cetak_tabel_langkah(steps, mode="Enkripsi"):
    """
    Mencetak tabel langkah-langkah proses ke konsol.
    """
    print(f"\n--- TABEL LANGKAH-LANGKAH PROSES ({mode.upper()}) ---")
    header_val = "P_val" if mode.lower() == "enkripsi" else "C_val"
    print(f"{'No':<4} | {'Input':<6} | {header_val:<6} | {'Kunci':<6} | {'K_val':<6} | {'Rumus Matematis':<25} | {'Hasil':<6}")
    print("-" * 75)
    
    for s in steps:
        val_in = s.get('p_val', s.get('c_val'))
        print(f"{s['no']:<4} | {s['char']:<6} | {str(val_in):<6} | {s['key_char']:<6} | {str(s['k_val']):<6} | {s['formula']:<25} | {s['result_char']:<6}")
    print("-" * 75)


if __name__ == "__main__":
    print("==========================================")
    print("   DEMO ALGORITMA VIGENÈRE CIPHER LENGKAP ")
    print("==========================================")
    print("Pilih Mode:")
    print("1. Enkripsi (Plaintext -> Ciphertext)")
    print("2. Dekripsi (Ciphertext -> Plaintext)")
    
    pilihan = input("Masukkan pilihan (1/2): ").strip()
    
    if pilihan == "1":
        teks_input = input("Masukkan Teks (Plaintext): ").strip()
        kunci_input = input("Masukkan Kunci (Key): ").strip()
        
        if not teks_input or not kunci_input:
            print("\n[!] Teks dan Kunci tidak boleh kosong! Menggunakan contoh default.")
            teks_input = "KRIPTOGRAFI"
            kunci_input = "KEY"
            
        print(f"\n[+] Plaintext : {teks_input}")
        print(f"[+] Kunci     : {kunci_input}")
        
        ciphertext, steps_enc = vigenere_encrypt(teks_input, kunci_input)
        print(f"\n[=>] HASIL ENKRIPSI (CIPHERTEXT): {ciphertext}")
        cetak_tabel_langkah(steps_enc, mode="Enkripsi")

    elif pilihan == "2":
        teks_input = input("Masukkan Teks (Ciphertext): ").strip()
        kunci_input = input("Masukkan Kunci (Key): ").strip()
        
        if not teks_input or not kunci_input:
            print("\n[!] Teks dan Kunci tidak boleh kosong! Menggunakan contoh default.")
            teks_input = "UAVNZREYLDS"
            kunci_input = "KEY"
            
        print(f"\n[+] Ciphertext : {teks_input}")
        print(f"[+] Kunci      : {kunci_input}")
        
        plaintext, steps_dec = vigenere_decrypt(teks_input, kunci_input)
        print(f"\n[=>] HASIL DEKRIPSI (PLAINTEXT): {plaintext}")
        cetak_tabel_langkah(steps_dec, mode="Dekripsi")

    else:
        print("\n[!] Pilihan tidak valid. Silakan pilih 1 atau 2.")

