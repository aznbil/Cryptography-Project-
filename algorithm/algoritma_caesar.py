def caesar_encrypt(text, shift):
    result = ""
    steps = [] 
    
    for char in text:
        # Cek dulu ini huruf beneran atau bukan. Spasi, angka, tanda baca kita lewatin.
        if char.isalpha(): 
            
            # Komputer nyimpen huruf 'A' itu sebagai angka 65, dan 'a' kecil sebagai 97.
            # Jadi kita set dulu patokan dasarnya.
            ascii_offset = 65 if char.isupper() else 97
            
            # INTI RUMUSNYA:
            # 1. ord() -> ubah huruf jadi angka
            # 2. Kurangin patokan dasar, tambahin shift (geser maju)
            # 3. % 26 -> biar kalau udah mentok di 'Z', dia muter balik lagi ke 'A'
            # 4. Tambahin patokan dasarnya lagi biar balik ke standar angka ASCII komputer
            new_char_code = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            
            # chr() -> balikin angka yang udah digeser tadi jadi huruf lagi
            new_char = chr(new_char_code)
            
            result += new_char
            steps.append(f"Karakter '{char}' digeser maju {shift} -> '{new_char}'")
            
        else:
            # Kalau spasi atau simbol, langsung copas aja ke hasil
            result += char
            steps.append(f"Karakter '{char}' (bukan huruf, skip geser)")
            
    return result, steps


def caesar_decrypt(text, shift):
    result = ""
    steps = []
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            
            # RUMUS DECRYPT:
            # Sama persis kayak encrypt, bedanya ini minus (-) shift karena jalannya mundur.
            new_char_code = (ord(char) - ascii_offset - shift) % 26 + ascii_offset
            new_char = chr(new_char_code)
            
            result += new_char
            steps.append(f"Karakter '{char}' digeser mundur {shift} -> '{new_char}'")
        else:
            result += char
            steps.append(f"Karakter '{char}' (bukan huruf, skip geser)")
            
    return result, steps
