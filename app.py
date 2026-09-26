import importlib
import re

import pandas as pd
import streamlit as st

from algorithm.algoritma_caesar import caesar_encrypt, caesar_decrypt

vigenere_module = importlib.import_module("algorithm.algoritma-Vigenere")
vigenere_encrypt = vigenere_module.vigenere_encrypt
vigenere_decrypt = vigenere_module.vigenere_decrypt
aes_module = importlib.import_module("algorithm.algoritma-AES")
AESCipher = aes_module.AESCipher
chacha_module = importlib.import_module("algorithm.algoritma-Chacha20")
chacha20_encrypt = chacha_module.chacha20_encrypt
chacha20_decrypt = chacha_module.chacha20_decrypt

st.set_page_config(page_title="Kriptografi Interaktif", page_icon="🔐", layout="wide")


def save_result(key, result):
    st.session_state[key] = result
    steps = result[1] if isinstance(result, tuple) else []
    first_step = steps[0] if steps else ""
    st.session_state[f"{key}_step"] = (
        2 if isinstance(first_step, str) and first_step.startswith(("PROSES ", "===")) and len(steps) > 1 else 1
    )


def parse_integer_input(label, value, minimum, maximum):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        st.error(f"{label} wajib diisi dengan bilangan bulat.")
        return None
    if not minimum <= parsed <= maximum:
        st.error(f"{label} harus berada di antara {minimum} dan {maximum}.")
        return None
    return parsed


def find_hex_step(steps, prefix):
    for step in steps:
        if isinstance(step, str) and step.startswith(prefix):
            match = re.search(r":\s*([0-9a-fA-F]+)$", step)
            if match:
                return bytes.fromhex(match.group(1))
    return None


def render_byte_state(label, data):
    cells = [f"{byte:02x}" for byte in data[:16]]
    rows = [[cells[row + column * 4] for column in range(4)] for row in range(4)]
    st.caption(label)
    st.dataframe(
        pd.DataFrame(rows, columns=["Kolom 0", "Kolom 1", "Kolom 2", "Kolom 3"]),
        hide_index=True,
        width="stretch",
    )


def render_aes_cbc_simulation(steps, key):
    is_encrypt = key.startswith("aes_encrypt") or key.startswith("super_aes")
    if is_encrypt:
        iv = find_hex_step(steps, "6. IV random")
        data = find_hex_step(steps, "8. Plaintext setelah padding")
        result = find_hex_step(steps, "10. Ciphertext hasil AES-CBC")
    else:
        iv = find_hex_step(steps, "4. IV (16 byte pertama)")
        data = find_hex_step(steps, "5. Ciphertext")
        result = find_hex_step(steps, "8. Hasil dekripsi sebelum unpadding")

    if not iv or not data or not result:
        return

    st.markdown("#### 🔐 Visualisasi blok AES-CBC")
    st.caption(
        "Setiap blok AES berukuran 16 byte. Matriks menunjukkan byte dalam urutan kolom AES; "
        "XOR dan CBC chain dihitung dari data proses ini. Implementasi AES memakai library "
        "kriptografi yang tidak membuka state internal tiap round."
    )
    block_count = min(len(data), len(result)) // 16
    for block_index in range(block_count):
        start = block_index * 16
        current_input = data[start:start + 16]
        current_output = result[start:start + 16]
        chain = iv if block_index == 0 else (
            result[start - 16:start] if is_encrypt else data[start - 16:start]
        )
        xor_result = bytes(left ^ right for left, right in zip(current_input, chain))

        with st.expander(f"Blok {block_index + 1} — {16} byte", expanded=block_index == 0):
            if is_encrypt:
                input_col, chain_col, xor_col, output_col = st.columns(4)
                with input_col:
                    render_byte_state("Plaintext blok", current_input)
                with chain_col:
                    render_byte_state("IV / ciphertext sebelumnya", chain)
                with xor_col:
                    render_byte_state("Hasil XOR sebelum AES", xor_result)
                with output_col:
                    render_byte_state("Output AES (ciphertext)", current_output)
                st.markdown("**Plaintext → XOR dengan IV/ blok sebelumnya → AES → Ciphertext**")
            else:
                input_col, aes_col, chain_col, output_col = st.columns(4)
                with input_col:
                    render_byte_state("Ciphertext blok", current_input)
                with aes_col:
                    render_byte_state("Output AES decrypt", xor_result)
                with chain_col:
                    render_byte_state("IV / ciphertext sebelumnya", chain)
                with output_col:
                    render_byte_state("Plaintext setelah XOR", current_output)
                st.markdown("**Ciphertext → AES decrypt → XOR dengan IV/ blok sebelumnya → Plaintext**")


def render_step_visualization(title, steps, key):
    if not steps:
        st.info("Algoritma tidak menghasilkan langkah untuk ditampilkan.")
        return

    step_key = f"{key}_step"
    if step_key not in st.session_state:
        st.session_state[step_key] = 1
    st.session_state[step_key] = min(st.session_state[step_key], len(steps))

    st.markdown(f"### {title}")
    previous_col, progress_col, next_col = st.columns([1, 4, 1])
    if previous_col.button("← Sebelumnya", key=f"{step_key}_previous", disabled=st.session_state[step_key] <= 1):
        st.session_state[step_key] -= 1
    if next_col.button("Berikutnya →", key=f"{step_key}_next", disabled=st.session_state[step_key] >= len(steps)):
        st.session_state[step_key] += 1
    selected = st.session_state[step_key]
    progress_col.progress(selected / len(steps), text=f"Langkah {selected} dari {len(steps)}")
    step = steps[selected - 1]

    if key.startswith("aes_") or key.startswith("super_aes"):
        render_aes_cbc_simulation(steps, key)

    with st.container(border=True):
        if isinstance(step, dict):
            st.caption(f"LANGKAH {step.get('No', selected)}")
            input_value = step.get("Karakter Input", "-")
            key_value = step.get("Kunci", "-")
            output_value = step.get("Hasil", "-")
            input_col, key_col, output_col = st.columns(3)
            input_col.metric("Input", str(input_value))
            key_col.metric("Karakter kunci", str(key_value))
            output_col.metric("Hasil", str(output_value))
            formula = step.get("Rumus Matematis")
            if formula:
                st.info(f"Operasi: `{formula}`")
            with st.expander("Lihat nilai dan detail perhitungan"):
                st.json(step)
            return

        lines = str(step).splitlines()
        heading = lines[0] if lines else f"Langkah {selected}"
        st.caption(heading.upper())

        if heading.startswith("Karakter '") and "'" in heading[10:]:
            parts = heading.split("'")
            input_value = parts[1] if len(parts) > 1 else ""
            output_value = heading.split("-> '", 1)[1].split("'", 1)[0] if "-> '" in heading else input_value
            input_col, action_col, output_col = st.columns([2, 1, 2])
            input_col.metric("Karakter masuk", input_value or "spasi")
            action_col.markdown("<div style='text-align:center;padding-top:20px;font-size:24px'>→</div>", unsafe_allow_html=True)
            output_col.metric("Karakter keluar", output_value or "spasi")

        state_label = None
        state_rows = []
        detail_lines = []
        for line in lines[1:]:
            if line.endswith("State:") or line.endswith("state:"):
                state_label = line.rstrip(":")
                state_rows = []
                continue
            if state_label and "|" in line:
                state_rows.append([word.strip() for word in line.split("|")])
                continue
            if state_rows and line.strip():
                state_label = None
            detail_lines.append(line)

        if state_rows and all(len(row) == 4 for row in state_rows):
            st.caption(state_label or "State 4 × 4")
            st.dataframe(
                pd.DataFrame(state_rows, columns=["Word 1", "Word 2", "Word 3", "Word 4"]),
                hide_index=True,
                width="stretch",
            )
            quarter_rounds = re.findall(r"\((\d+,\d+,\d+,\d+)\)", "\n".join(lines))
            if quarter_rounds:
                st.caption("Kelompok word yang diproses pada quarter-round ini")
                st.code("   →   ".join(f"({group})" for group in quarter_rounds), language=None)
        details = "\n".join(detail_lines).strip()
        if details:
            st.code(details, language=None)


def render_result(result_key, output_label, visualization_title):
    if result_key not in st.session_state:
        return
    output, steps = st.session_state[result_key]
    st.success(output_label)
    st.code(output, language=None)
    render_step_visualization(visualization_title, steps, result_key)


menu = st.sidebar.selectbox(
    "📋 Pilih Menu:",
    ("🏠 Beranda", "🔑 Caesar Cipher", "🔐 Vigenère Cipher", "⚙️ AES", "🌊 ChaCha20", "🚀 Super Encryption"),
)

if menu == "🏠 Beranda":
    st.title("🔐 Aplikasi Kriptografi Interaktif")
    st.subheader("Simulasi Visual & Edukatif")
    st.info("Pilih algoritma di sidebar untuk mencoba enkripsi/dekripsi dan menelusuri setiap langkahnya.")

elif menu == "🔑 Caesar Cipher":
    st.header("🔑 Caesar Cipher")
    teks = st.text_area("Masukkan teks:", placeholder="HELLO WORLD")
    shift_input = st.number_input(
        "Shift:",
        min_value=1,
        max_value=25,
        value=None,
        step=1,
        placeholder="Masukkan angka 1–25",
    )
    encrypt_col, decrypt_col = st.columns(2)
    if encrypt_col.button("🔒 Enkripsi"):
        shift = parse_integer_input("Shift", shift_input, 1, 25)
        if shift is not None:
            save_result("caesar_encrypt_result", caesar_encrypt(teks, shift))
    if decrypt_col.button("🔓 Dekripsi"):
        shift = parse_integer_input("Shift", shift_input, 1, 25)
        if shift is not None:
            save_result("caesar_decrypt_result", caesar_decrypt(teks, shift))

    render_result(
        "caesar_encrypt_result",
        "Hasil enkripsi:",
        "🔄 Simulasi pergeseran maju",
    )
    render_result(
        "caesar_decrypt_result",
        "Hasil dekripsi:",
        "🔄 Simulasi pergeseran balik",
    )

elif menu == "🔐 Vigenère Cipher":
    st.header("🔐 Vigenère Cipher")
    teks = st.text_area("Masukkan teks:", placeholder="HELLO")
    kunci = st.text_input("Kata Kunci:", placeholder="Masukkan kunci Vigenère")
    encrypt_col, decrypt_col = st.columns(2)
    if encrypt_col.button("🔒 Enkripsi"):
        try:
            save_result("vigenere_encrypt_result", vigenere_encrypt(teks, kunci))
        except ValueError as error:
            st.error(str(error))
    if decrypt_col.button("🔓 Dekripsi"):
        try:
            save_result("vigenere_decrypt_result", vigenere_decrypt(teks, kunci))
        except ValueError as error:
            st.error(str(error))

    for operation in ("encrypt", "decrypt"):
        result_key = f"vigenere_{operation}_result"
        if result_key in st.session_state:
            output, steps = st.session_state[result_key]
            st.success(f"Hasil {'enkripsi' if operation == 'encrypt' else 'dekripsi'}:")
            st.code(output, language=None)
            render_step_visualization(
                f"📊 Simulasi karakter Vigenère — {operation.title()}",
                steps,
                result_key,
            )
            with st.expander("Lihat tabel seluruh karakter"):
                st.dataframe(pd.DataFrame(steps), hide_index=True, width="stretch")

elif menu == "⚙️ AES":
    st.header("⚙️ AES")
    teks = st.text_area("Masukkan teks:", placeholder="SECRET MESSAGE")
    kunci = st.text_input("Kunci AES:", placeholder="Masukkan 16, 24, atau 32 karakter")
    encrypt_col, decrypt_col = st.columns(2)
    if encrypt_col.button("🔒 Enkripsi"):
        try:
            cipher = AESCipher(kunci.encode())
            save_result("aes_encrypt_result", cipher.aes_encrypt(teks))
        except ValueError as error:
            st.error(str(error))
    if decrypt_col.button("🔓 Dekripsi"):
        try:
            cipher = AESCipher(kunci.encode())
            save_result("aes_decrypt_result", cipher.aes_decrypt(teks))
        except ValueError as error:
            st.error(str(error))

    render_result(
        "aes_encrypt_result",
        "Hasil enkripsi:",
        "🔄 Simulasi proses AES-CBC",
    )
    render_result(
        "aes_decrypt_result",
        "Hasil dekripsi:",
        "🔄 Simulasi proses AES-CBC",
    )

elif menu == "🌊 ChaCha20":
    st.header("🌊 ChaCha20")
    teks = st.text_area("Masukkan teks:", placeholder="SECRET MESSAGE")
    kunci = st.text_input(
        "Key (Hex):",
        placeholder="Masukkan key 64 karakter hex",
    )
    nonce = st.text_input("Nonce (Hex):", placeholder="Masukkan nonce 24 karakter hex")
    counter_input = st.number_input(
        "Counter:",
        min_value=0,
        max_value=4294967295,
        value=None,
        step=1,
        placeholder="Masukkan angka 0–4294967295",
    )
    encrypt_col, decrypt_col = st.columns(2)
    if encrypt_col.button("🔒 Enkripsi"):
        counter = parse_integer_input("Counter", counter_input, 0, 4294967295)
        if counter is not None:
            try:
                save_result("chacha_encrypt_result", chacha20_encrypt(teks, kunci, nonce, counter))
            except ValueError as error:
                st.error(str(error))
    if decrypt_col.button("🔓 Dekripsi"):
        counter = parse_integer_input("Counter", counter_input, 0, 4294967295)
        if counter is not None:
            try:
                save_result("chacha_decrypt_result", chacha20_decrypt(teks, kunci, nonce, counter))
            except ValueError as error:
                st.error(str(error))

    render_result(
        "chacha_encrypt_result",
        "Hasil enkripsi:",
        "🌊 Simulasi state dan operasi ChaCha20",
    )
    render_result(
        "chacha_decrypt_result",
        "Hasil dekripsi:",
        "🌊 Simulasi state dan operasi ChaCha20",
    )

elif menu == "🚀 Super Encryption":
    st.header("🚀 Super Encryption")
    teks = st.text_area("Masukkan teks:", placeholder="SECRET MESSAGE")
    shift_input = st.number_input(
        "Shift Caesar:",
        min_value=1,
        max_value=25,
        value=None,
        step=1,
        placeholder="Masukkan angka 1–25",
    )
    kunci_vig = st.text_input("Kunci Vigenère:", placeholder="Masukkan kunci Vigenère")
    kunci_aes = st.text_input("Kunci AES:", placeholder="Masukkan 16, 24, atau 32 karakter")
    kunci_chacha = st.text_input(
        "Key (Hex):",
        placeholder="Masukkan key 64 karakter hex",
    )
    nonce_chacha = st.text_input("Nonce (Hex):", placeholder="Masukkan nonce 24 karakter hex")
    counter_input = st.number_input(
        "Counter ChaCha20:",
        min_value=0,
        max_value=4294967295,
        value=None,
        step=1,
        placeholder="Masukkan angka 0–4294967295",
    )

    if st.button("🚀 Enkripsi Super"):
        shift = parse_integer_input("Shift Caesar", shift_input, 1, 25)
        counter_chacha = parse_integer_input("Counter ChaCha20", counter_input, 0, 4294967295)
        if shift is not None and counter_chacha is not None:
            try:
                hasil_caesar, langkah_caesar = caesar_encrypt(teks, shift)
                hasil_vig, langkah_vig = vigenere_encrypt(hasil_caesar, kunci_vig)
                cipher = AESCipher(kunci_aes.encode())
                hasil_aes, langkah_aes = cipher.aes_encrypt(hasil_vig)
                hasil_chacha, langkah_chacha = chacha20_encrypt(
                    hasil_aes, kunci_chacha, nonce_chacha, counter_chacha
                )
                save_result(
                    "super_result",
                    {
                        "outputs": [teks, hasil_caesar, hasil_vig, hasil_aes, hasil_chacha],
                        "steps": [langkah_caesar, langkah_vig, langkah_aes, langkah_chacha],
                    },
                )
                st.session_state["super_stage"] = "Caesar"
            except ValueError as error:
                st.error(str(error))

    if "super_result" in st.session_state:
        result = st.session_state["super_result"]
        output_labels = ["Plaintext", "Caesar", "Vigenère", "AES-CBC", "ChaCha20"]
        st.markdown("### 🔗 Alur enkripsi")
        pipeline_cols = st.columns(len(output_labels))
        for column, label, output in zip(pipeline_cols, output_labels, result["outputs"]):
            preview = output if len(output) <= 18 else f"{output[:15]}…"
            column.metric(label, preview)
        st.success("Hasil enkripsi super:")
        st.code(result["outputs"][-1], language=None)

        stage_steps = dict(zip(output_labels[1:], result["steps"]))
        selected_stage = st.selectbox(
            "Pilih tahap untuk ditelusuri:",
            list(stage_steps),
            key="super_stage",
        )
        render_step_visualization(
            f"Langkah {selected_stage}",
            stage_steps[selected_stage],
            f"super_{selected_stage.lower()}",
        )


