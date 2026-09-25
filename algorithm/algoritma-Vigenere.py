def vigenere_encrypt(text: str, key: str):
    """
    Mengenkripsi teks menggunakan Algoritma Vigenère Cipher dan mencatat langkah-langkahnya.
    
    Returns:
        tuple: (ciphertext, steps)
        - ciphertext (str): Hasil teks terenkripsi
        - steps (list of dict): Daftar langkah perhitungan yang cocok untuk Streamlit (st.dataframe / st.table)
    """
    ciphertext = ""
    steps = []
    
    clean_key = ''.join([c.upper() for c in key if c.isalpha()])
    if not clean_key:
        raise ValueError("Kunci harus mengandung setidaknya satu huruf alfabet.")
        
    key_idx = 0
    for char in text:
        if char.isalpha():
            base_val = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base_val
            k_char = clean_key[key_idx % len(clean_key)]
            k_val = ord(k_char) - ord('A')
            
            c_val = (p_val + k_val) % 26
            c_char = chr(c_val + base_val)
            ciphertext += c_char
            
            steps.append({
                'No': len(steps) + 1,
                'Karakter Input': char,
                'P_val (0-25)': p_val,
                'Kunci': k_char,
                'K_val (0-25)': k_val,
                'Rumus Matematis': f"({p_val} + {k_val}) mod 26 = {c_val}",
                'Hasil': c_char
            })
            key_idx += 1
        else:
            ciphertext += char
            steps.append({
                'No': len(steps) + 1,
                'Karakter Input': char,
                'P_val (0-25)': '-',
                'Kunci': '-',
                'K_val (0-25)': '-',
                'Rumus Matematis': 'Abaikan (Non-Alfabet)',
                'Hasil': char
            })
            
    return ciphertext, steps


def vigenere_decrypt(text: str, key: str):
    """
    Mendekripsi teks menggunakan Algoritma Vigenère Cipher dan mencatat langkah-langkahnya.
    
    Returns:
        tuple: (plaintext, steps)
        - plaintext (str): Hasil teks terdekripsi
        - steps (list of dict): Daftar langkah perhitungan yang cocok untuk Streamlit (st.dataframe / st.table)
    """
    plaintext = ""
    steps = []
    
    clean_key = ''.join([c.upper() for c in key if c.isalpha()])
    if not clean_key:
        raise ValueError("Kunci harus mengandung setidaknya satu huruf alfabet.")
        
    key_idx = 0
    for char in text:
        if char.isalpha():
            base_val = ord('A') if char.isupper() else ord('a')
            c_val = ord(char) - base_val
            k_char = clean_key[key_idx % len(clean_key)]
            k_val = ord(k_char) - ord('A')
            
            p_val = (c_val - k_val + 26) % 26
            p_char = chr(p_val + base_val)
            plaintext += p_char
            
            steps.append({
                'No': len(steps) + 1,
                'Karakter Input': char,
                'C_val (0-25)': c_val,
                'Kunci': k_char,
                'K_val (0-25)': k_val,
                'Rumus Matematis': f"({c_val} - {k_val} + 26) mod 26 = {p_val}",
                'Hasil': p_char
            })
            key_idx += 1
        else:
            plaintext += char
            steps.append({
                'No': len(steps) + 1,
                'Karakter Input': char,
                'C_val (0-25)': '-',
                'Kunci': '-',
                'K_val (0-25)': '-',
                'Rumus Matematis': 'Abaikan (Non-Alfabet)',
                'Hasil': char
            })
            
    return plaintext, steps
