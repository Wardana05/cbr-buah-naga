# 🐉 CBR Buah Naga v3 — Sistem Pakar Diagnosa Penyakit Tanaman Buah Naga

Aplikasi web interaktif berbasis **Streamlit** untuk mendiagnosa hama dan penyakit tanaman buah naga menggunakan metode **Case-Based Reasoning (CBR)** dan **Cosine Similarity**.

## Fitur Utama
- **Beranda Interaktif**: Ringkasan statistik penyakit, gejala, basis kasus, serta alur 4 tahapan CBR (*Retrieve, Reuse, Revise, Retain*).
- **Diagnosa Penyakit**: Pencarian gejala cepat, pemilihan gejala interaktif, perhitungan Cosine Similarity real-time, peringkat kemiripan dengan *progress bar* gradasi, rekomendasi penanganan, serta fitur **Revise & Retain** langsung ke basis kasus aktif.
- **Basis Data & Kasus**: Eksplorasi Tabel Penyakit (P1–P7), Tabel Gejala (G1–G22), dan Matriks Basis Kasus Biner (1/0) dengan filter pencarian.
- **Kasus Tersimpan (Retain)**: Kelola kasus baru yang telah divalidasi pakar selama sesi berlangsung.

## Cara Menjalankan Lokal
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy ke Streamlit Community Cloud
1. Unggah seluruh isi folder `cbr web v3` ke repositori GitHub Anda.
2. Buka [share.streamlit.io](https://share.streamlit.io), pilih repositori Anda, dan arahkan *Main file path* ke `streamlit_app.py`.
3. Klik **Deploy**.

---
**Pengembang:** Virdan Andi Wardana (Mahasiswa Bisnis Informatika - Politeknik Negeri Banyuwangi)  
**Sumber Data:** Pratama dkk. (2022), *Jurnal Smart Teknologi* 4(1), 77–82.
