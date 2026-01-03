# app.py
import os
import streamlit as st
from collections import Counter
from preprocessing import preprocess
from similarity import jaccard_similarity
from utils import read_file
from collections import defaultdict

st.set_page_config(layout="wide")

st.title("📄 Aplikasi Temu Balik Dokumen Bahasa Indonesia")
st.caption("Hybrid Stemming (Dictionary + Rule-Based) & Jaccard Similarity")

folder = st.text_input("Masukkan path folder dokumen:", "documents")

if not os.path.exists(folder):
    st.error("Folder tidak ditemukan.")
    st.stop()

# DAFTAR DOKUMEN
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

st.subheader("📂 Daftar Dokumen")
st.json(files)

documents = {}
raw_texts = {}

for file in files:
    path = os.path.join(folder, file)
    text = read_file(path)
    raw_texts[file] = text
    documents[file] = preprocess(text)

# HASIL PREPROCESSING
st.subheader("⚙️ Hasil Preprocessing & Stemming")

for file, tokens in documents.items():
    with st.expander(f"📄 {file}", expanded=False):

        # ---- teks asli (cuplikan)
        st.markdown("**Teks Asli (Cuplikan):**")
        st.write(raw_texts[file][:1000] + "...")

        # ---- token hasil preprocessing
        st.markdown("**Token Setelah Preprocessing & Stemming:**")
        st.write(tokens)

        # ---- frekuensi kata dasar
        mapping = defaultdict(list)

        for original, stem in tokens:
            mapping[stem].append(original)

        data = []
        for stem, originals in mapping.items():
            data.append({
                "Kata Sebelum Stemming": ", ".join(sorted(set(originals))),
                "Kata Dasar": stem,
                "Frekuensi": len(originals)
            })

        st.markdown("**Kata Sebelum Stemming → Kata Dasar → Frekuensi:**")
        st.table(data)

# QUERY SEARCH
st.subheader("🔎 Pencarian Dokumen")
query = st.text_input("Masukkan query pencarian:")

if query:
    query_tokens = preprocess(query)

    st.subheader("⚙️ Query Setelah Preprocessing")
    st.write(query_tokens)

    # SIMILARITY RESULT
    st.subheader("📊 Hasil Kemiripan (Jaccard Similarity)")

    results = []
    for doc, tokens in documents.items():
        score = jaccard_similarity(tokens, query_tokens)
        results.append({
            "Dokumen": doc,
            "Similarity": round(score, 4),
            "Jumlah Kata Dokumen": len(tokens),
            "Jumlah Kata Query": len(query_tokens)
        })

    results = sorted(results, key=lambda x: x["Similarity"], reverse=True)

    st.table(results)
