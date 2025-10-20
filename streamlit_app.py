import streamlit as st
import os
import subprocess

# Створюємо папки
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("🎬 Video Admin Panel — Merge Footage + Bodies")

# Завантаження футажа
footage_file = st.file_uploader("Upload Footage", type=["mp4", "mov"])
# Завантаження декількох body
body_files = st.file_uploader("Upload Body videos (multiple)", type=["mp4", "mov"], accept_multiple_files=True)

if footage_file and body_files:
    # Зберігаємо футаж
    footage_path = os.path.join("uploads", footage_file.name)
    with open(footage_path, "wb") as f:
        f.write(footage_file.getbuffer())
    st.success(f"Uploaded Footage: {footage_file.name}")

    # Зберігаємо body
    body_paths = []
    for body in body_files:
        path = os.path.join("uploads", body.name)
        with open(path, "wb") as f:
            f.write(body.getbuffer())
        body_paths.append(path)
    st.success(f"Uploaded {len(body_files)} body videos")

    # Кнопка для склейки
    if st.button("Merge Footage with All Bodies"):
        output_files = []
        for body_path in body_paths:
            body_name = os.path.splitext(os.path.basename(body_path))[0]
            footage_name = os.path.splitext(os.path.basename(footage_path))[0]
            output_path = os.path.join("output", f"{footage_name}+{body_name}.mp4")

            # Створюємо тимчасовий list.txt для concat
            list_txt = os.path.join("uploads", "list.txt")
            with open(list_txt, "w") as f:
                f.write(f"file '{footage_path}'\n")
                f.write(f"file '{body_path}'\n")

            # Склеюємо відео
            subprocess.run([
                "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_txt, "-c", "copy", output_path
            ])
            output_files.append(output_path)

        st.success(f"✅ Merged {len(output_files)} videos!")
        for file in output_files:
            st.markdown(f"[Download {os.path.basename(file)}]({file})")
