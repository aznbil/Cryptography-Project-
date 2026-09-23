def caesar_encrypt(text, shift):
    result = ""
    steps = [] # Array untuk merekam langkah-langkah
    
    for char in text:
        if char.isalpha(): # Mengecek apakah karakter adalah alfabet (A-Z, a-z)
            # Menentukan nilai desimal ASCII (65 untuk 'A', 97 untuk 'a')
            ascii_offset = 65 if char.isupper() else 97
            
            # Rumus pergeseran melingkar (modulo 26)
            new_char_code = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            new_char = chr(new_char_code)
            
            result += new_char
            steps.append(f"Karakter '{char}' digeser maju {shift} -> '{new_char}'")
        else:
            # Jika spasi, angka, atau simbol, biarkan saja tanpa pergeseran
            result += char
            steps.append(f"Karakter '{char}' (bukan alfabet, tidak digeser)")
            
    return result, steps

def caesar_decrypt(text, shift):
    result = ""
    steps = []
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            
            # Rumus dekripsi sama dengan enkripsi, namun arah pergeseran dikurangi (-)
            new_char_code = (ord(char) - ascii_offset - shift) % 26 + ascii_offset
            new_char = chr(new_char_code)
            
            result += new_char
            steps.append(f"Karakter '{char}' digeser mundur {shift} -> '{new_char}'")
        else:
            result += char
            steps.append(f"Karakter '{char}' (bukan alfabet, tidak digeser)")
            
    return result, steps
