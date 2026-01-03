# app_simple.py
import os
import streamlit as st
from preprocessing import preprocess
from similarity import jaccard_similarity
from utils import read_file

st.set_page_config(layout="wide")

st.title("📄 Temu Balik Dokumen - Versi Simple")
st.caption("Stemming AYS + Jaccard Similarity")

# BACA DOKUMEN
folder = st.text_input("Masukkan path folder dokumen:", "documents")

if not os.path.exists(folder):
    st.error("Folder tidak ditemukan.")
    st.stop()

# Ambil semua file dalam folder
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

st.write(f"**Jumlah Dokumen:** {len(files)}")
st.write("**Daftar Dokumen:**", files)

# PREPROCESSING DOKUMEN
st.subheader("📝 Preprocessing Dokumen")

# Gunakan session_state untuk menyimpan hasil preprocessing
# Hanya jalankan preprocessing jika belum pernah atau folder berubah
if 'documents' not in st.session_state or st.session_state.get('folder') != folder:
    st.session_state.folder = folder
    documents = {}
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file in enumerate(files):
        # Update progress
        progress = (idx + 1) / len(files)
        progress_bar.progress(progress)
        status_text.text(f"Memproses {file}... ({idx + 1}/{len(files)})")
        
        # Baca file
        path = os.path.join(folder, file)
        text = read_file(path)
        
        # Preprocessing: case folding → tokenizing → filtering → stemming
        tokens = preprocess(text)
        
        # Simpan hasil (hanya kata dasar)
        documents[file] = [stem for original, stem in tokens]
    
    # Simpan ke session_state
    st.session_state.documents = documents
    
    # Selesai
    status_text.text(f"✅ Selesai memproses {len(files)} dokumen!")
    progress_bar.empty()  # Hilangkan progress bar setelah selesai
else:
    # Ambil dari session_state (tidak preprocessing lagi)
    documents = st.session_state.documents
    st.info(f"✅ Menggunakan {len(documents)} dokumen yang sudah diproses (tidak preprocessing ulang)")

# QUERY SEARCH
st.subheader("🔍 Pencarian Dokumen")
query = st.text_input("Masukkan kata kunci pencarian:")

if query:
    # Preprocessing query
    query_tokens = preprocess(query)
    query_stems = [stem for original, stem in query_tokens]
    
    st.write("**Query setelah preprocessing:**", query_stems)
    
    # HITUNG SIMILARITY
    st.subheader("📊 Hasil Pencarian")
    
    results = []
    
    for doc_name, doc_stems in documents.items():
        # Hitung Jaccard Similarity
        score = jaccard_similarity(
            [(w, w) for w in doc_stems],  # Convert ke tuple format
            [(w, w) for w in query_stems]
        )
        
        results.append({
            "Dokumen": doc_name,
            "Skor": f"{score:.4f}",
            "Relevansi": "⭐⭐⭐" if score > 0.3 else "⭐⭐" if score > 0.1 else "⭐"
        })
    
    # Urutkan berdasarkan skor (descending)
    results = sorted(results, key=lambda x: float(x["Skor"]), reverse=True)
    
    # Tampilkan hasil
    st.table(results)
    
    # Dokumen paling relevan
    if results and float(results[0]["Skor"]) > 0:
        st.success(f"📄 Dokumen paling relevan: **{results[0]['Dokumen']}** (Skor: {results[0]['Skor']})")
    else:
        st.warning("Tidak ada dokumen yang relevan dengan query.")
