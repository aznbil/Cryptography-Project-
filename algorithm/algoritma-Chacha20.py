import base64
import struct

_MASK32 = 0xFFFFFFFF
_BLOCK_SIZE = 64


def _rotl32(value, shift):
    return (((value << shift) & _MASK32) | (value >> (32 - shift)))


def _quarter_round(state, a, b, c, d):
    state[a] = (state[a] + state[b]) & _MASK32
    state[d] ^= state[a]
    state[d] = _rotl32(state[d], 16)

    state[c] = (state[c] + state[d]) & _MASK32
    state[b] ^= state[c]
    state[b] = _rotl32(state[b], 12)

    state[a] = (state[a] + state[b]) & _MASK32
    state[d] ^= state[a]
    state[d] = _rotl32(state[d], 8)

    state[c] = (state[c] + state[d]) & _MASK32
    state[b] ^= state[c]
    state[b] = _rotl32(state[b], 7)


def _validate_key_nonce(key, nonce):
    try:
        key_bytes = bytes.fromhex(key)
        nonce_bytes = bytes.fromhex(nonce)
    except (ValueError, TypeError):
        raise ValueError("Key dan nonce harus berupa hexadecimal yang valid.")

    if len(key_bytes) != 32:
        raise ValueError("Key harus 32 byte (256-bit atau 64 karakter hex).")
    if len(nonce_bytes) != 12:
        raise ValueError("Nonce harus 12 byte (96-bit atau 24 karakter hex).")
    return key_bytes, nonce_bytes


def _format_state(state):
    return "\n".join(
        " | ".join(f"{value:08x}" for value in state[row * 4:row * 4 + 4])
        for row in range(4)
    )


def _chacha20_block(key_bytes, counter, nonce_bytes, steps=None):
    constants = struct.unpack("<4I", b"expand 32-byte k")
    key_words = list(struct.unpack("<8I", key_bytes))
    nonce_words = list(struct.unpack("<3I", nonce_bytes))
    initial_state = list(constants) + key_words + [counter] + nonce_words
    working_state = initial_state.copy()

    if steps is not None:
        steps.append(
            "TAHAP 1 — INITIAL STATE\n"
            "Susunan: Constant (4 word) + Key (8 word) + Counter (1 word) + Nonce (3 word).\n"
            f"Counter: {counter}\nInitial State:\n{_format_state(initial_state)}"
        )

    for round_index in range(10):
        # Column round
        _quarter_round(working_state, 0, 4, 8, 12)
        _quarter_round(working_state, 1, 5, 9, 13)
        _quarter_round(working_state, 2, 6, 10, 14)
        _quarter_round(working_state, 3, 7, 11, 15)

        if steps is not None:
            steps.append(
                f"DOUBLE ROUND {round_index + 1} — COLUMN ROUND\n"
                "Quarter Round pada indeks (0,4,8,12), (1,5,9,13), "
                "(2,6,10,14), (3,7,11,15).\n"
                f"State:\n{_format_state(working_state)}"
            )

        # Diagonal round
        _quarter_round(working_state, 0, 5, 10, 15)
        _quarter_round(working_state, 1, 6, 11, 12)
        _quarter_round(working_state, 2, 7, 8, 13)
        _quarter_round(working_state, 3, 4, 9, 14)

        if steps is not None:
            steps.append(
                f"DOUBLE ROUND {round_index + 1} — DIAGONAL ROUND\n"
                "Quarter Round pada indeks (0,5,10,15), (1,6,11,12), "
                "(2,7,8,13), (3,4,9,14).\n"
                f"State:\n{_format_state(working_state)}"
            )

    output_state = [
        (working_state[i] + initial_state[i]) & _MASK32
        for i in range(16)
    ]

    if steps is not None:
        steps.append(
            "TAHAP 2 — ADD INITIAL STATE\n"
            "Setiap word hasil 20 rounds ditambah dengan word initial state modulo 2^32.\n"
            f"Output State:\n{_format_state(output_state)}"
        )

    keystream = struct.pack("<16I", *output_state)
    if steps is not None:
        steps.append(
            "TAHAP 3 — KEYSTREAM\n"
            f"Keystream (hex): {keystream.hex()}\nPanjang: {len(keystream)} byte."
        )
    return keystream


def _chacha20_xor(data, key_bytes, nonce_bytes, counter, steps):
    result = bytearray()
    total_blocks = (len(data) + _BLOCK_SIZE - 1) // _BLOCK_SIZE

    steps.append(f"TAHAP 4 — XOR\nTotal blok: {total_blocks}.")

    for block_index in range(total_blocks):
        current_counter = counter + block_index
        if current_counter > _MASK32:
            raise ValueError("Counter melebihi batas maksimum.")

        data_block = data[
            block_index * _BLOCK_SIZE:(block_index + 1) * _BLOCK_SIZE
        ]
        keystream = _chacha20_block(
            key_bytes, current_counter, nonce_bytes, steps
        )

        encrypted_block = bytearray()
        steps.append(f"Blok {block_index + 1} — XOR per byte:")

        for byte_index, (data_byte, key_byte) in enumerate(zip(data_block, keystream)):
            output_byte = data_byte ^ key_byte
            encrypted_block.append(output_byte)
            steps.append(
                f"Byte {byte_index + 1}: {data_byte:02x} XOR "
                f"{key_byte:02x} = {output_byte:02x}"
            )

        result.extend(encrypted_block)

    return bytes(result)


def chacha20_encrypt(text, key, nonce, counter=1):
    if not isinstance(text, str):
        raise ValueError("Plaintext harus berupa string.")
    if not isinstance(counter, int) or isinstance(counter, bool):
        raise ValueError("Counter harus berupa bilangan bulat.")
    if not 0 <= counter <= _MASK32:
        raise ValueError("Counter berada di luar rentang 0 sampai 2^32-1.")

    key_bytes, nonce_bytes = _validate_key_nonce(key, nonce)
    plaintext_bytes = text.encode("utf-8")
    steps = [
        "PROSES ENKRIPSI CHACHA20",
        "TAHAP 0 — INPUT\n"
        f"Plaintext: {text}\nByte UTF-8 (hex): {plaintext_bytes.hex()}\n"
        f"Key (hex): {key_bytes.hex()}\nNonce (hex): {nonce_bytes.hex()}\n"
        f"Counter awal: {counter}"
    ]

    ciphertext_bytes = _chacha20_xor(
        plaintext_bytes, key_bytes, nonce_bytes, counter, steps
    )
    result = base64.b64encode(ciphertext_bytes).decode("ascii")
    steps.append(
        "TAHAP 5 — HASIL ENKRIPSI\n"
        f"Ciphertext (hex): {ciphertext_bytes.hex()}\n"
        f"Ciphertext (Base64): {result}"
    )
    return result, steps


def chacha20_decrypt(text, key, nonce, counter=1):
    if not isinstance(text, str):
        raise ValueError("Ciphertext harus berupa string Base64.")
    if not isinstance(counter, int) or isinstance(counter, bool):
        raise ValueError("Counter harus berupa bilangan bulat.")
    if not 0 <= counter <= _MASK32:
        raise ValueError("Counter berada di luar rentang 0 sampai 2^32-1.")

    key_bytes, nonce_bytes = _validate_key_nonce(key, nonce)
    try:
        ciphertext_bytes = base64.b64decode(text, validate=True)
    except (ValueError, base64.binascii.Error):
        raise ValueError("Ciphertext Base64 tidak valid.")

    steps = [
        "PROSES DEKRIPSI CHACHA20",
        "TAHAP 0 — INPUT\n"
        f"Ciphertext (Base64): {text}\nCiphertext (hex): {ciphertext_bytes.hex()}\n"
        f"Key (hex): {key_bytes.hex()}\nNonce (hex): {nonce_bytes.hex()}\n"
        f"Counter awal: {counter}"
    ]

    plaintext_bytes = _chacha20_xor(
        ciphertext_bytes, key_bytes, nonce_bytes, counter, steps
    )
    try:
        result = plaintext_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            "Hasil dekripsi bukan UTF-8 valid. Periksa key, nonce, dan counter."
        )

    steps.append(
        "TAHAP 5 — HASIL DEKRIPSI\n"
        f"Plaintext (hex): {plaintext_bytes.hex()}\nPlaintext: {result}"
    )
    return result, steps
