# streamlit_app.py
# Sistem Pakar Diagnosa Penyakit Tanaman Buah Naga (CBR Buah Naga v3)
# Metode: Case-Based Reasoning (CBR) + Cosine Similarity
# Pengembang: Virdan Andi Wardana (Mahasiswa Bisnis Informatika - Politeknik Negeri Banyuwangi)

import math
import pandas as pd
import numpy as np
import streamlit as st
from data import PENYAKIT, GEJALA, BASIS_KASUS, SOLUSI_PENANGANAN

# -------------------- Konfigurasi Halaman --------------------
st.set_page_config(
    page_title="CBR Buah Naga v3 — Sistem Pakar Agri-Tech",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)

DAFTAR_GEJALA = list(GEJALA.keys())  # G1 ... G22

# -------------------- Inisialisasi Session State --------------------
def init_session_state():
    if "kasus_list" not in st.session_state:
        st.session_state.kasus_list = [
            {"id": kode, "penyakit": kode, "gejala": list(daftar), "baru": False}
            for kode, daftar in BASIS_KASUS.items()
        ]
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Beranda"
    if "last_diagnosa" not in st.session_state:
        st.session_state.last_diagnosa = None
    if "selected_gejala" not in st.session_state:
        st.session_state.selected_gejala = []

init_session_state()

# -------------------- Logika Perhitungan CBR (100% Sesuai app.py) --------------------
def buat_vektor(daftar_kode):
    """Ubah daftar kode gejala jadi vektor 0/1 sepanjang 22 gejala."""
    return [1 if kode in daftar_kode else 0 for kode in DAFTAR_GEJALA]


def panjang_vektor(vektor):
    """||V|| = akar dari jumlah kuadrat (untuk isi 0/1 = akar jumlah angka 1)."""
    return math.sqrt(sum(x * x for x in vektor))


def hitung_kemiripan(gejala_user):
    """RETRIEVE: bandingkan kasus baru (A) dengan semua kasus lama (B)."""
    a = buat_vektor(gejala_user)
    norm_a = panjang_vektor(a)
    hasil = []
    for kasus in st.session_state.kasus_list:
        b = buat_vektor(kasus["gejala"])
        norm_b = panjang_vektor(b)
        sama = [g for g in gejala_user if g in kasus["gejala"]]
        dot = len(sama)  # A . B
        nilai = dot / (norm_a * norm_b) if norm_a * norm_b > 0 else 0.0
        hasil.append({
            "id": kasus["id"],
            "penyakit": kasus["penyakit"],
            "nama": PENYAKIT[kasus["penyakit"]],
            "sama": sama,
            "dot": dot,
            "jumlah_b": len(kasus["gejala"]),
            "norm_b": norm_b,
            "nilai": nilai,
            "persen": nilai * 100,
            "baru": kasus["baru"],
        })
    hasil.sort(key=lambda x: x["nilai"], reverse=True)
    return norm_a, hasil


# -------------------- Custom CSS Injection (Vibrant Cosmic Botanical & Gradient Mesh) --------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --deep-emerald: #042F2E;
    --emerald-rich: #065F46;
    --emerald-glow: #10B981;
    --midnight-teal: #0F172A;
    --dragon-magenta: #E11D48;
    --dragon-crimson: #BE123C;
    --glass-bg: rgba(15, 23, 42, 0.58);
    --glass-border: rgba(255, 255, 255, 0.14);
}

/* Global Typography & Cosmic Mesh Background */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #F8FAFC !important;
}

.stApp {
    background-color: #042F2E !important;
    background-image:
        radial-gradient(at 8% 12%, rgba(16, 185, 129, 0.28) 0px, transparent 48%),
        radial-gradient(at 92% 10%, rgba(225, 29, 72, 0.34) 0px, transparent 50%),
        radial-gradient(at 82% 85%, rgba(190, 18, 60, 0.26) 0px, transparent 52%),
        radial-gradient(at 15% 88%, rgba(6, 78, 59, 0.55) 0px, transparent 55%),
        linear-gradient(135deg, #042F2E 0%, #0F172A 52%, #1E1B2E 100%) !important;
    background-attachment: fixed !important;
}

h1, h2, h3, h4, .heading-font {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.02em;
}

/* Hide default Streamlit branding header/footer clutter while keeping sidebar toggle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: rgba(4, 47, 46, 0.35) !important;
    backdrop-filter: blur(10px);
}

/* Main container spacing */
.block-container {
    padding-top: 1.75rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1220px !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(4, 47, 46, 0.92) 0%, rgba(15, 23, 42, 0.96) 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(16px);
}

/* Animated Gradient Hero Banner */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floatOrb {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-8px) rotate(2deg); }
}

.hero-banner {
    background: linear-gradient(-45deg, #042F2E, #065F46, #BE123C, #E11D48, #0F172A);
    background-size: 320% 320%;
    animation: gradientShift 11s ease infinite;
    border-radius: 26px;
    padding: 2.3rem 2.4rem;
    border: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow: 0 24px 55px -15px rgba(0, 0, 0, 0.55), 0 0 32px rgba(225, 29, 72, 0.22);
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.hero-banner::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(8px);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #A7F3D0;
    margin-bottom: 0.9rem;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(1.75rem, 3.2vw, 2.55rem);
    font-weight: 800;
    line-height: 1.16;
    color: #FFFFFF;
    margin: 0 0 0.75rem 0;
}

.hero-subtitle {
    font-size: 0.98rem;
    line-height: 1.65;
    color: rgba(241, 245, 249, 0.92);
    max-width: 720px;
    margin: 0;
}

.hero-float-icon {
    animation: floatOrb 5s ease-in-out infinite;
}

/* Glassmorphism Cards with Hover Lift & Glow */
.glass-card {
    background: rgba(15, 23, 42, 0.56);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 22px;
    padding: 1.45rem;
    box-shadow: 0 12px 32px -10px rgba(0, 0, 0, 0.45);
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.glass-card:hover {
    transform: translateY(-5px);
    border-color: rgba(16, 185, 129, 0.48);
    box-shadow: 0 20px 42px -12px rgba(0, 0, 0, 0.6), 0 0 24px rgba(16, 185, 129, 0.2);
}

/* Gradient Stat Cards */
.stat-card-emerald {
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.78) 0%, rgba(16, 185, 129, 0.32) 100%);
    border: 1px solid rgba(52, 211, 153, 0.35);
    border-radius: 22px;
    padding: 1.4rem 1.5rem;
    backdrop-filter: blur(12px);
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 14px 30px -10px rgba(4, 47, 46, 0.65);
}

.stat-card-magenta {
    background: linear-gradient(135deg, rgba(159, 18, 57, 0.78) 0%, rgba(225, 29, 72, 0.35) 100%);
    border: 1px solid rgba(251, 113, 133, 0.38);
    border-radius: 22px;
    padding: 1.4rem 1.5rem;
    backdrop-filter: blur(12px);
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 14px 30px -10px rgba(136, 19, 55, 0.55);
}

.stat-card-teal {
    background: linear-gradient(135deg, rgba(15, 118, 110, 0.75) 0%, rgba(56, 189, 248, 0.28) 100%);
    border: 1px solid rgba(45, 212, 191, 0.38);
    border-radius: 22px;
    padding: 1.4rem 1.5rem;
    backdrop-filter: blur(12px);
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 14px 30px -10px rgba(15, 23, 42, 0.65);
}

.stat-card-emerald:hover, .stat-card-magenta:hover, .stat-card-teal:hover {
    transform: translateY(-6px) scale(1.015);
    box-shadow: 0 22px 42px -12px rgba(0, 0, 0, 0.65), 0 0 26px rgba(225, 29, 72, 0.24);
}

/* CBR 4-Stage Interactive Cards */
.cbr-step-card {
    border-radius: 20px;
    padding: 1.35rem;
    height: 100%;
    backdrop-filter: blur(14px);
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    position: relative;
    overflow: hidden;
}

.cbr-step-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 20px 38px -10px rgba(0, 0, 0, 0.6);
}

.step-1 {
    background: linear-gradient(145deg, rgba(6, 95, 70, 0.72), rgba(15, 23, 42, 0.82));
    border: 1px solid rgba(16, 185, 129, 0.42);
}
.step-2 {
    background: linear-gradient(145deg, rgba(13, 148, 136, 0.65), rgba(15, 23, 42, 0.82));
    border: 1px solid rgba(45, 212, 191, 0.42);
}
.step-3 {
    background: linear-gradient(145deg, rgba(190, 18, 60, 0.68), rgba(15, 23, 42, 0.82));
    border: 1px solid rgba(251, 113, 133, 0.45);
}
.step-4 {
    background: linear-gradient(145deg, rgba(124, 58, 237, 0.55), rgba(15, 23, 42, 0.84));
    border: 1px solid rgba(167, 139, 250, 0.42);
}

/* Animated Progress Bar for Similarity Results */
@keyframes fillProgress {
    from { width: 0%; }
}

.sim-progress-track {
    width: 100%;
    height: 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 6px;
}

.sim-progress-bar-winner {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #10B981 0%, #34D399 45%, #E11D48 100%);
    animation: fillProgress 1.1s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 0 14px rgba(225, 29, 72, 0.55);
}

.sim-progress-bar-normal {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #059669 0%, #10B981 100%);
    animation: fillProgress 1.1s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Streamlit Buttons Customization */
div.stButton > button {
    background: linear-gradient(135deg, #E11D48 0%, #BE123C 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.35rem !important;
    box-shadow: 0 10px 25px -6px rgba(225, 29, 72, 0.55) !important;
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 16px 32px -6px rgba(225, 29, 72, 0.72), 0 0 18px rgba(225, 29, 72, 0.4) !important;
}

/* Secondary / Nav Pills styling */
.top-nav-wrap {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 20px;
    padding: 0.85rem 1.25rem;
    margin-bottom: 1.35rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.45);
}

.social-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: #E2E8F0 !important;
    text-decoration: none !important;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.25s ease;
}

.social-pill:hover {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.35), rgba(225, 29, 72, 0.35));
    border-color: rgba(255, 255, 255, 0.35);
    color: #FFFFFF !important;
    transform: translateY(-2px);
}

/* Custom Inputs & Checkboxes */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background-color: rgba(15, 23, 42, 0.72) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
}

div[data-testid="stCheckbox"] {
    background: rgba(15, 23, 42, 0.52);
    border: 1px solid rgba(255, 255, 255, 0.11);
    border-radius: 14px;
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.45rem;
    transition: all 0.25s ease;
}

div[data-testid="stCheckbox"]:hover {
    background: rgba(6, 78, 59, 0.52);
    border-color: rgba(16, 185, 129, 0.48);
    transform: translateX(3px);
}

/* Complex Multi-Column Footer */
.custom-footer {
    margin-top: 3.5rem;
    background: linear-gradient(145deg, rgba(4, 47, 46, 0.92) 0%, rgba(15, 23, 42, 0.96) 65%, rgba(67, 12, 34, 0.88) 100%);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 26px;
    padding: 2.2rem 2.2rem 1.5rem 2.2rem;
    box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.65);
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding-bottom: 1.6rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.footer-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.footer-text {
    font-size: 0.86rem;
    line-height: 1.65;
    color: #CBD5E1;
    margin: 0 0 0.65rem 0;
}

.footer-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    border-radius: 10px;
    color: #E2E8F0 !important;
    text-decoration: none !important;
    font-size: 0.86rem;
    font-weight: 500;
    transition: all 0.25s ease;
    margin-bottom: 4px;
}

.footer-link:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #34D399 !important;
    transform: translateX(4px);
}

.footer-bottom {
    padding-top: 1.2rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.78rem;
    color: #94A3B8;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------- Komponen Header & Sidebar --------------------
PAGES = [
    ("Beranda", "🏠 Beranda"),
    ("Diagnosa Penyakit", "🩺 Diagnosa Penyakit"),
    ("Basis Data & Kasus", "📊 Basis Data & Kasus"),
    ("Kasus Tersimpan", "💾 Kasus Tersimpan"),
]

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:44px; height:44px; border-radius:14px; background:linear-gradient(135deg,#10B981,#E11D48); display:flex; align-items:center; justify-content:center; font-size:1.45rem; box-shadow:0 8px 20px rgba(225,29,72,0.4);">
                🐉
            </div>
            <div>
                <div class="heading-font" style="font-size:1.15rem; font-weight:800; color:#FFFFFF; line-height:1.1;">
                    CBR <span style="color:#FB7185;">Buah Naga</span>
                </div>
                <div style="font-size:0.74rem; color:#6EE7B7; font-weight:600; margin-top:2px;">
                    Agri-Tech Expert v3
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Navigasi Utama")
    for page_key, page_label in PAGES:
        is_active = st.session_state.active_page == page_key
        btn_label = f"▶ {page_label}" if is_active else page_label
        if st.button(btn_label, key=f"side_nav_{page_key}", use_container_width=True):
            st.session_state.active_page = page_key
            st.rerun()

    st.markdown("---")
    kasus_baru_count = sum(1 for k in st.session_state.kasus_list if k["baru"])
    st.markdown(f"""
    <div class="glass-card" style="padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; color:#6EE7B7; font-weight:700;">Status Basis Kasus</div>
        <div style="font-size:1.45rem; font-weight:800; color:#FFFFFF; margin-top:4px;">{len(st.session_state.kasus_list)} Kasus Aktif</div>
        <div style="font-size:0.8rem; color:#CBD5E1; margin-top:2px;">7 jurnal + {kasus_baru_count} kasus Retain</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👨‍💻 Profil Pengembang")
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:8px;">
        <a class="social-pill" href="https://github.com" target="_blank">
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11.02 11.02 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.8-.01 3.18 0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/></svg>
            GitHub
        </a>
        <a class="social-pill" href="https://instagram.com" target="_blank">
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5a4.25 4.25 0 0 0 4.25 4.25h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5a4.25 4.25 0 0 0-4.25-4.25h-8.5zm8.75 2.25a1 1 0 1 1 0 2 1 1 0 0 1 0-2zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z"/></svg>
            Instagram
        </a>
        <a class="social-pill" href="https://linkedin.com" target="_blank">
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V23h-4V8zm7.5 0h3.8v2.05h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V23h-4v-7.9c0-1.88-.03-4.3-2.62-4.3-2.62 0-3.02 2.05-3.02 4.16V23h-4V8z"/></svg>
            LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)

# Top Header Bar with Quick Links & Horizontal Navigation
st.markdown("""
<div class="top-nav-wrap">
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:1.55rem;">🐉</span>
        <div>
            <span class="heading-font" style="font-size:1.1rem; font-weight:800; color:#FFFFFF;">CBR Buah Naga <span style="background:linear-gradient(90deg,#34D399,#FB7185); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">v3.0</span></span>
            <span style="display:block; font-size:0.75rem; color:#94A3B8;">Sistem Pakar Diagnosa Penyakit Tanaman Buah Naga</span>
        </div>
    </div>
    <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px;">
        <a class="social-pill" href="https://github.com" target="_blank">
            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11.02 11.02 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.8-.01 3.18 0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/></svg>
            GitHub
        </a>
        <a class="social-pill" href="https://instagram.com" target="_blank">
            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5a4.25 4.25 0 0 0 4.25 4.25h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5a4.25 4.25 0 0 0-4.25-4.25h-8.5zm8.75 2.25a1 1 0 1 1 0 2 1 1 0 0 1 0-2zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z"/></svg>
            Instagram
        </a>
        <a class="social-pill" href="https://linkedin.com" target="_blank">
            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V23h-4V8zm7.5 0h3.8v2.05h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V23h-4v-7.9c0-1.88-.03-4.3-2.62-4.3-2.62 0-3.02 2.05-3.02 4.16V23h-4V8z"/></svg>
            LinkedIn
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Tab Navigation Bar
nav_cols = st.columns(4)
for idx, (page_key, page_label) in enumerate(PAGES):
    with nav_cols[idx]:
        active_marker = "✨ " if st.session_state.active_page == page_key else ""
        if st.button(f"{active_marker}{page_label}", key=f"top_nav_{page_key}", use_container_width=True):
            st.session_state.active_page = page_key
            st.rerun()

st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

# ==============================================================================
# HALAMAN 1: BERANDA
# ==============================================================================
if st.session_state.active_page == "Beranda":
    # Hero Section Bergradasi
    st.markdown("""
    <div class="hero-banner">
        <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:1.5rem; position:relative; z-index:2;">
            <div style="flex:1 1 540px;">
                <div class="hero-badge">🌿 Smart Precision Agri-Tech Platform</div>
                <h1 class="hero-title">
                    Sistem Pakar Diagnosa Penyakit Tanaman <span style="color:#FDE047;">Buah Naga</span>
                </h1>
                <p class="hero-subtitle">
                    Identifikasi serangan hama dan penyakit tanaman buah naga secara cepat, akurat, dan terukur.
                    Pilih gejala fisik yang terlihat pada tanaman, lalu sistem menelusuri kasus terdahulu yang paling relevan
                    menggunakan metode <b>Case-Based Reasoning (CBR)</b>.
                </p>
            </div>
            <div class="hero-float-icon" style="flex:0 0 auto; margin:auto;">
                <div style="width:155px; height:155px; border-radius:32px; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.28); backdrop-filter:blur(12px); display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 18px 40px rgba(0,0,0,0.35);">
                    <svg width="86" height="86" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="dfBody" x1="30" y1="20" x2="90" y2="105" gradientUnits="userSpaceOnUse">
                                <stop offset="0%" stop-color="#FB7185"/>
                                <stop offset="50%" stop-color="#E11D48"/>
                                <stop offset="100%" stop-color="#881337"/>
                            </linearGradient>
                            <linearGradient id="dfLeaf" x1="0" y1="0" x2="1" y2="1">
                                <stop offset="0%" stop-color="#6EE7B7"/>
                                <stop offset="100%" stop-color="#059669"/>
                            </linearGradient>
                        </defs>
                        <path d="M55 24C49 11 38 8 34 11C41 15 46 21 49 28L55 24Z" fill="url(#dfLeaf)"/>
                        <path d="M62 22C61 9 54 4 49 6C54 11 56 18 57 25L62 22Z" fill="url(#dfLeaf)"/>
                        <path d="M68 25C74 11 84 8 89 11C81 15 76 21 73 28L68 25Z" fill="url(#dfLeaf)"/>
                        <rect x="34" y="24" width="52" height="76" rx="26" fill="url(#dfBody)"/>
                        <path d="M35 45C24 40 19 32 21 28C27 33 32 37 37 40L35 45Z" fill="url(#dfLeaf)"/>
                        <path d="M33 65C21 62 16 54 18 49C24 54 30 57 34 60L33 65Z" fill="url(#dfLeaf)"/>
                        <path d="M85 45C96 40 101 32 99 28C93 33 88 37 83 40L85 45Z" fill="url(#dfLeaf)"/>
                        <path d="M87 65C99 62 104 54 102 49C96 54 90 57 86 60L87 65Z" fill="url(#dfLeaf)"/>
                        <path d="M55 52C49 46 46 40 48 37C53 41 56 45 58 49L55 52Z" fill="url(#dfLeaf)"/>
                        <path d="M67 68C73 62 77 56 75 53C70 57 66 61 63 65L67 68Z" fill="url(#dfLeaf)"/>
                        <circle cx="54" cy="60" r="2.2" fill="#FFF1F2"/>
                        <circle cx="65" cy="76" r="2.2" fill="#FFF1F2"/>
                        <circle cx="52" cy="80" r="2.2" fill="#FFF1F2"/>
                    </svg>
                    <span style="font-size:0.72rem; font-weight:700; color:#A7F3D0; margin-top:4px;">AI Botanical CBR</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol Aksi Cepat di bawah Hero
    cta1, cta2, _ = st.columns([1.2, 1.2, 2.2])
    with cta1:
        if st.button("🩺 Mulai Diagnosa Sekarang", key="hero_cta_diag", use_container_width=True):
            st.session_state.active_page = "Diagnosa Penyakit"
            st.rerun()
    with cta2:
        if st.button("📊 Eksplorasi Basis Data", key="hero_cta_data", use_container_width=True):
            st.session_state.active_page = "Basis Data & Kasus"
            st.rerun()

    st.markdown("<div style='height:1.1rem;'></div>", unsafe_allow_html=True)

    # Kartu Statistik Warna-Warni
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
        <div class="stat-card-magenta">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#FECDD3;">Penyakit & Hama</span>
                <span style="font-size:1.5rem;">🦠</span>
            </div>
            <div class="heading-font" style="font-size:2.6rem; font-weight:800; color:#FFFFFF; margin:0.35rem 0;">{len(PENYAKIT)}</div>
            <div style="font-size:0.84rem; color:#FFE4E6;">Kategori terklasifikasi (P1 – P7)</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="stat-card-emerald">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#A7F3D0;">Gejala Klinis</span>
                <span style="font-size:1.5rem;">🌿</span>
            </div>
            <div class="heading-font" style="font-size:2.6rem; font-weight:800; color:#FFFFFF; margin:0.35rem 0;">{len(GEJALA)}</div>
            <div style="font-size:0.84rem; color:#D1FAE5;">Indikator visual tanaman (G1 – G22)</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown(f"""
        <div class="stat-card-teal">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#99F6E4;">Basis Kasus</span>
                <span style="font-size:1.5rem;">🗂️</span>
            </div>
            <div class="heading-font" style="font-size:2.6rem; font-weight:800; color:#FFFFFF; margin:0.35rem 0;">{len(st.session_state.kasus_list)}</div>
            <div style="font-size:0.84rem; color:#CCFBF1;">Kasus referensi siap penalaran</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)

    # 4 Tahapan CBR (Tanpa Rumus Matematis Cosine Similarity)
    st.markdown("""
    <div style="margin-bottom:0.9rem;">
        <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#34D399;">Siklus Penalaran Sistem</span>
        <h2 class="heading-font" style="font-size:1.55rem; font-weight:800; color:#FFFFFF; margin:0.15rem 0 0 0;">Tahapan Case-Based Reasoning (CBR)</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    steps_info = [
        ("step-1", "1", "Retrieve", "🔍", "#34D399", "Menghitung tingkat kemiripan antara gejala kasus baru dengan seluruh kasus lama di dalam basis pengetahuan."),
        ("step-2", "2", "Reuse", "♻️", "#2DD4BF", "Mengadopsi solusi diagnosis dari kasus terdahulu yang memiliki skor kemiripan tertinggi sebagai kesimpulan awal."),
        ("step-3", "3", "Revise", "🩺", "#FB7185", "Pakar atau pengguna meninjau hasil rekomendasi sistem dan dapat mengoreksi diagnosis akhir bila diperlukan."),
        ("step-4", "4", "Retain", "💾", "#C4B5FD", "Menyimpan kasus baru yang telah tervalidasi ke dalam basis kasus agar memperkaya diagnosa berikutnya."),
    ]
    for col, (cls, num, title, ico, accent, desc) in zip([c1, c2, c3, c4], steps_info):
        with col:
            st.markdown(f"""
            <div class="cbr-step-card {cls}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.85rem;">
                    <span style="width:34px; height:34px; border-radius:11px; background:rgba(255,255,255,0.14); color:{accent}; font-weight:800; display:flex; align-items:center; justify-content:center; font-size:0.95rem;">
                        {num}
                    </span>
                    <span style="font-size:1.35rem;">{ico}</span>
                </div>
                <div class="heading-font" style="font-size:1.12rem; font-weight:800; color:#FFFFFF; margin-bottom:0.45rem;">
                    {num}. {title}
                </div>
                <p style="font-size:0.86rem; line-height:1.55; color:#E2E8F0; margin:0;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# HALAMAN 2: DIAGNOSA PENYAKIT
# ==============================================================================
elif st.session_state.active_page == "Diagnosa Penyakit":
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.25rem; border-left:5px solid #E11D48;">
        <span style="font-size:0.76rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#FB7185;">Symptom Assessment & CBR Engine</span>
        <h2 class="heading-font" style="font-size:1.65rem; font-weight:800; color:#FFFFFF; margin:0.2rem 0 0.35rem 0;">🩺 Diagnosa Kasus Baru</h2>
        <p style="font-size:0.9rem; color:#CBD5E1; margin:0;">
            Centang gejala yang terlihat pada tanaman buah naga Anda, lalu tekan tombol <b>Hitung Kemiripan</b> untuk menjalankan proses Retrieve, Reuse, Revise, dan Retain.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter Pencarian Cepat Gejala
    col_search, col_info = st.columns([2.2, 1])
    with col_search:
        search_q = st.text_input("🔎 Cari kode atau deskripsi gejala:", placeholder="Contoh: G1, busuk, layu, bercak, buah...")
    with col_info:
        selected_now = [g for g in DAFTAR_GEJALA if st.session_state.get(f"chk_{g}", False)]
        st.markdown(f"""
        <div class="glass-card" style="padding:0.75rem 1rem; text-align:center; margin-top:0.25rem;">
            <span style="font-size:0.75rem; color:#94A3B8; display:block;">Gejala Dipilih</span>
            <span class="heading-font" style="font-size:1.3rem; font-weight:800; color:#34D399;">{len(selected_now)} / {len(DAFTAR_GEJALA)}</span>
        </div>
        """, unsafe_allow_html=True)

    # Pengelompokan Gejala Berdasarkan Bagian Tanaman agar Rapi & Mudah Dipilih
    KELOMPOK_GEJALA = [
        ("🌱 Pangkal & Batang Tanaman", ["G1", "G2", "G3", "G4", "G5", "G20"]),
        ("🌿 Kondisi Umum, Cabang & Sulur", ["G6", "G7", "G8", "G9", "G10", "G11", "G12", "G19", "G21", "G22"]),
        ("🌸 Pucuk, Bunga & Buah", ["G13", "G14", "G15", "G16", "G17", "G18"]),
    ]

    q_lower = search_q.strip().lower()
    for group_title, codes in KELOMPOK_GEJALA:
        filtered_codes = [
            g for g in codes
            if not q_lower or q_lower in g.lower() or q_lower in GEJALA[g].lower()
        ]
        if not filtered_codes:
            continue

        st.markdown(f"""
        <div style="margin: 1rem 0 0.55rem 0; font-family:'Plus Jakarta Sans',sans-serif; font-weight:700; font-size:1.02rem; color:#6EE7B7;">
            {group_title}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, kode in enumerate(filtered_codes):
            with cols[i % 2]:
                st.checkbox(f"**{kode}** — {GEJALA[kode]}", key=f"chk_{kode}")

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    b1, b2, _ = st.columns([1.2, 1.0, 2.3])
    with b1:
        hitung_btn = st.button("🚀 Hitung Kemiripan", key="btn_hitung_cbr", use_container_width=True)
    with b2:
        if st.button("🔄 Kosongkan Pilihan", key="btn_reset_chk", use_container_width=True):
            for g in DAFTAR_GEJALA:
                st.session_state[f"chk_{g}"] = False
            st.session_state.last_diagnosa = None
            st.rerun()

    if hitung_btn:
        dipilih = [g for g in DAFTAR_GEJALA if st.session_state.get(f"chk_{g}", False)]
        if not dipilih:
            st.warning("⚠️ Pilih minimal satu gejala terlebih dahulu sebelum menghitung kemiripan.")
        else:
            norm_a, hasil = hitung_kemiripan(dipilih)
            tertinggi = hasil[0]["nilai"]
            pemenang = [h for h in hasil if abs(h["nilai"] - tertinggi) < 1e-9] if tertinggi > 0 else []
            st.session_state.last_diagnosa = {
                "dipilih": dipilih,
                "norm_a": norm_a,
                "hasil": hasil,
                "pemenang": pemenang,
            }

    # -------------------- Tampilan Hasil Diagnosa --------------------
    if st.session_state.last_diagnosa:
        res = st.session_state.last_diagnosa
        dipilih = res["dipilih"]
        norm_a = res["norm_a"]
        hasil = res["hasil"]
        pemenang = res["pemenang"]

        st.markdown("---")
        st.markdown("""
        <h2 class="heading-font" style="font-size:1.6rem; font-weight:800; color:#FFFFFF; margin-bottom:0.8rem;">
            📋 Laporan Hasil Diagnosa CBR
        </h2>
        """, unsafe_allow_html=True)

        # 2. REUSE: Kesimpulan Utama
        if not pemenang:
            st.markdown("""
            <div class="glass-card" style="border-left:5px solid #F59E0B; background:rgba(120,53,15,0.45); margin-bottom:1.25rem;">
                <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:#FCD34D;">2. Reuse — Kesimpulan</span>
                <h3 class="heading-font" style="font-size:1.25rem; font-weight:800; color:#FFFFFF; margin:0.25rem 0;">Tidak Ada Kasus Lama yang Cocok (0%)</h3>
                <p style="font-size:0.9rem; color:#FEF3C7; margin:0;">Semua nilai kemiripan bernilai 0. Kasus ini memerlukan pemeriksaan langsung oleh pakar pada tahap Revise.</p>
            </div>
            """, unsafe_allow_html=True)
        elif len(pemenang) > 1:
            seri_str = ", ".join([f"{h['id']} ({h['nama']})" for h in pemenang])
            st.markdown(f"""
            <div class="glass-card" style="border-left:5px solid #F59E0B; background:rgba(120,53,15,0.45); margin-bottom:1.25rem;">
                <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:#FCD34D;">2. Reuse — Hasil Seri</span>
                <h3 class="heading-font" style="font-size:1.25rem; font-weight:800; color:#FFFFFF; margin:0.25rem 0;">Kemiripan Tertinggi Seri: {pemenang[0]['persen']:.2f}%</h3>
                <p style="font-size:0.92rem; color:#FEF3C7; margin:0;">Terjadi nilai seri antara <b>{seri_str}</b>. Pakar perlu menentukan diagnosis akhir pada tahap Revise.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            top = pemenang[0]
            solusi_list = SOLUSI_PENANGANAN.get(top["penyakit"], [])
            solusi_html = "".join([f"<li style='margin-bottom:4px;'>{s}</li>" for s in solusi_list])
            st.markdown(f"""
            <div class="hero-banner" style="padding:1.8rem 2rem; margin-bottom:1.25rem;">
                <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:1rem;">
                    <div style="flex:1 1 420px;">
                        <span class="hero-badge" style="margin-bottom:0.5rem;">🏆 2. Reuse — Diagnosis Teratas</span>
                        <h3 class="heading-font" style="font-size:1.75rem; font-weight:800; color:#FFFFFF; margin:0.2rem 0 0.4rem 0;">
                            {top['penyakit']} — {top['nama']}
                        </h3>
                        <p style="font-size:0.92rem; color:#F1F5F9; margin:0;">
                            Kasus baru paling mirip dengan basis kasus <b>{top['id']}</b> berdasarkan <b>{top['dot']}</b> gejala yang beririsan.
                        </p>
                    </div>
                    <div style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.3); border-radius:20px; padding:1rem 1.5rem; text-align:center;">
                        <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.06em; color:#A7F3D0; display:block;">Tingkat Kemiripan</span>
                        <span class="heading-font" style="font-size:2.2rem; font-weight:800; color:#FFFFFF;">{top['persen']:.2f}%</span>
                    </div>
                </div>
                <div style="margin-top:1.1rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.2);">
                    <div style="font-size:0.84rem; font-weight:700; color:#FDE047; margin-bottom:0.4rem;">💡 Rekomendasi Penanganan & Pengendalian:</div>
                    <ul style="margin:0; padding-left:1.25rem; font-size:0.88rem; color:#F8FAFC; line-height:1.55;">
                        {solusi_html}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Ringkasan Kasus Baru (A)
        badges_a = " ".join([
            f"<span style='display:inline-block; padding:5px 11px; margin:3px; border-radius:10px; background:rgba(16,185,129,0.22); border:1px solid rgba(52,211,153,0.4); font-size:0.82rem; color:#ECFDF5;'><b>{g}</b>: {GEJALA[g]}</span>"
            for g in dipilih
        ])
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom:1.25rem;">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:0.5rem; margin-bottom:0.7rem;">
                <h3 class="heading-font" style="font-size:1.15rem; font-weight:800; color:#6EE7B7; margin:0;">📌 Kasus Baru (A)</h3>
                <span style="font-size:0.84rem; background:rgba(255,255,255,0.1); padding:4px 12px; border-radius:999px; color:#E2E8F0;">
                    Jumlah gejala = <b>{len(dipilih)}</b> | Panjang Vektor ‖A‖ = <b>{norm_a:.4f}</b>
                </span>
            </div>
            <div>{badges_a}</div>
        </div>
        """, unsafe_allow_html=True)

        # 1. RETRIEVE: Progress Bar & Tabel Detail Perhitungan
        st.markdown("""
        <div class="glass-card" style="margin-bottom:1.25rem;">
            <h3 class="heading-font" style="font-size:1.18rem; font-weight:800; color:#FFFFFF; margin:0 0 0.25rem 0;">
                📊 1. Retrieve — Peringkat & Rincian Kemiripan
            </h3>
            <p style="font-size:0.84rem; color:#94A3B8; margin:0 0 1rem 0;">
                Perbandingan kemiripan kasus baru terhadap seluruh basis kasus yang tersimpan.
            </p>
        """, unsafe_allow_html=True)

        for h in hasil:
            is_win = h in pemenang
            bar_cls = "sim-progress-bar-winner" if is_win else "sim-progress-bar-normal"
            badge_bg = "#E11D48" if is_win else "rgba(255,255,255,0.14)"
            crown = " 👑" if is_win else ""
            sama_txt = ", ".join(h["sama"]) if h["sama"] else "Tidak ada"
            st.markdown(f"""
            <div style="margin-bottom:0.95rem; padding:0.75rem 1rem; border-radius:14px; background:rgba(255,255,255,0.04); border:1px solid {'rgba(251,113,133,0.45)' if is_win else 'rgba(255,255,255,0.08)'};">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                    <div>
                        <span style="padding:2px 9px; border-radius:7px; background:{badge_bg}; color:#FFFFFF; font-weight:800; font-size:0.78rem; margin-right:6px;">{h['id']}</span>
                        <b style="color:#FFFFFF; font-size:0.95rem;">{h['nama']}{crown}</b>
                        <span style="font-size:0.78rem; color:#94A3B8; margin-left:8px;">(Irisan: {sama_txt})</span>
                    </div>
                    <div class="heading-font" style="font-weight:800; font-size:1rem; color:{'#FB7185' if is_win else '#34D399'};">
                        {h['persen']:.2f}% <span style="font-size:0.78rem; font-weight:500; color:#CBD5E1;">({h['nilai']:.4f})</span>
                    </div>
                </div>
                <div class="sim-progress-track">
                    <div class="{bar_cls}" style="width:{min(max(h['persen'], 0.0), 100.0):.2f}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        df_detail = pd.DataFrame([
            {
                "Kasus": h["id"],
                "Penyakit": f"{h['penyakit']} - {h['nama']}",
                "Gejala Sama": ", ".join(h["sama"]) if h["sama"] else "-",
                "A · B": h["dot"],
                "‖B‖": round(h["norm_b"], 4),
                "Skor S(A,B)": round(h["nilai"], 4),
                "Kemiripan (%)": f"{h['persen']:.2f}%",
            }
            for h in hasil
        ])
        st.dataframe(df_detail, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. REVISE & 4. RETAIN
        st.markdown("""
        <div class="glass-card" style="border-left:5px solid #10B981;">
            <h3 class="heading-font" style="font-size:1.18rem; font-weight:800; color:#6EE7B7; margin:0 0 0.25rem 0;">
                ✍️ 3. Revise & 4. Retain — Validasi Pakar & Simpan Kasus
            </h3>
            <p style="font-size:0.86rem; color:#CBD5E1; margin:0 0 0.9rem 0;">
                Pakar dapat memverifikasi atau mengoreksi diagnosis akhir sebelum menyimpannya ke dalam basis kasus aktif.
            </p>
        </div>
        """, unsafe_allow_html=True)

        opsi_penyakit = list(PENYAKIT.keys())
        default_idx = opsi_penyakit.index(pemenang[0]["penyakit"]) if pemenang else 0

        r_col1, r_col2 = st.columns([2, 1])
        with r_col1:
            pilihan_akhir = st.selectbox(
                "Pilih Diagnosis Akhir (Revise):",
                options=opsi_penyakit,
                index=default_idx,
                format_func=lambda k: f"{k} — {PENYAKIT[k]}",
                key="select_revise_penyakit",
            )
        with r_col2:
            st.markdown("<div style='height:1.72rem;'></div>", unsafe_allow_html=True)
            if st.button("💾 Simpan Kasus (Retain)", key="btn_retain_case", use_container_width=True):
                jumlah_baru = sum(1 for k in st.session_state.kasus_list if k["baru"])
                kode_baru = f"K{jumlah_baru + 1}"
                st.session_state.kasus_list.append({
                    "id": kode_baru,
                    "penyakit": pilihan_akhir,
                    "gejala": list(dipilih),
                    "baru": True,
                })
                st.success(f"✅ Kasus **{kode_baru}** berhasil disimpan sebagai **{pilihan_akhir} — {PENYAKIT[pilihan_akhir]}** dan langsung aktif untuk diagnosa berikutnya!")

# ==============================================================================
# HALAMAN 3: BASIS DATA & KASUS
# ==============================================================================
elif st.session_state.active_page == "Basis Data & Kasus":
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.25rem; border-left:5px solid #10B981;">
        <span style="font-size:0.76rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#6EE7B7;">Knowledge Base Repository</span>
        <h2 class="heading-font" style="font-size:1.65rem; font-weight:800; color:#FFFFFF; margin:0.2rem 0 0.35rem 0;">📊 Basis Data & Matriks Kasus</h2>
        <p style="font-size:0.9rem; color:#CBD5E1; margin:0;">
            Referensi data penyakit (P1–P7), gejala klinis (G1–G22), dan tabel representasi biner basis kasus dari Pratama dkk. (2022).
        </p>
    </div>
    """, unsafe_allow_html=True)

    filter_data = st.text_input("🔎 Filter data penyakit atau gejala:", placeholder="Ketik kode (P1/G5) atau kata kunci...")
    ft = filter_data.strip().lower()

    tab1, tab2, tab3 = st.tabs(["🦠 Tabel 1: Data Penyakit", "🌿 Tabel 2: Data Gejala", "🔢 Tabel 3: Matriks Basis Kasus (1/0)"])

    with tab1:
        rows_p = [
            {"Kode": k, "Nama Hama dan Penyakit": v, "Jumlah Gejala Basis": len(BASIS_KASUS[k]), "Daftar Gejala": ", ".join(BASIS_KASUS[k])}
            for k, v in PENYAKIT.items()
            if not ft or ft in k.lower() or ft in v.lower()
        ]
        st.dataframe(pd.DataFrame(rows_p), use_container_width=True, hide_index=True)

    with tab2:
        rows_g = [
            {"Kode": k, "Nama Gejala": v}
            for k, v in GEJALA.items()
            if not ft or ft in k.lower() or ft in v.lower()
        ]
        st.dataframe(pd.DataFrame(rows_g), use_container_width=True, hide_index=True)

    with tab3:
        st.caption("Keterangan: 1 = gejala muncul pada penyakit tersebut, 0 = tidak muncul.")
        matrix_rows = []
        for g in DAFTAR_GEJALA:
            if ft and ft not in g.lower() and ft not in GEJALA[g].lower():
                continue
            row = {"Kode": g, "Gejala": GEJALA[g]}
            for p in PENYAKIT:
                row[p] = 1 if g in BASIS_KASUS[p] else 0
            matrix_rows.append(row)
        st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True, hide_index=True)

# ==============================================================================
# HALAMAN 4: KASUS TERSIMPAN (RETAIN)
# ==============================================================================
elif st.session_state.active_page == "Kasus Tersimpan":
    tersimpan = [k for k in st.session_state.kasus_list if k["baru"]]

    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.25rem; border-left:5px solid #A78BFA;">
        <span style="font-size:0.76rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#C4B5FD;">Retained Case Memory</span>
        <h2 class="heading-font" style="font-size:1.65rem; font-weight:800; color:#FFFFFF; margin:0.2rem 0 0.35rem 0;">💾 Kasus Tersimpan (Retain)</h2>
        <p style="font-size:0.9rem; color:#CBD5E1; margin:0;">
            Kasus baru yang telah divalidasi pakar tersimpan selama sesi aktif dan otomatis ikut dihitung pada proses diagnosa berikutnya.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if tersimpan:
        df_saved = pd.DataFrame([
            {
                "ID Kasus": k["id"],
                "Diagnosis Penyakit": f"{k['penyakit']} — {PENYAKIT[k['penyakit']]}",
                "Jumlah Gejala": len(k["gejala"]),
                "Kode Gejala": ", ".join(k["gejala"]),
                "Rincian Gejala": "; ".join([f"{g} ({GEJALA[g]})" for g in k["gejala"]]),
            }
            for k in tersimpan
        ])
        st.dataframe(df_saved, use_container_width=True, hide_index=True)

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        c_del, _ = st.columns([1.4, 3])
        with c_del:
            if st.button("🗑️ Hapus Semua Kasus Tersimpan", key="btn_reset_retain", use_container_width=True):
                st.session_state.kasus_list = [k for k in st.session_state.kasus_list if not k["baru"]]
                st.success("Semua kasus tersimpan telah dihapus. Basis kasus kembali ke 7 kasus awal.")
                st.rerun()
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2.6rem 1.5rem;">
            <div style="font-size:2.6rem; margin-bottom:0.5rem;">📂</div>
            <h3 class="heading-font" style="font-size:1.25rem; font-weight:800; color:#FFFFFF; margin:0 0 0.4rem 0;">
                Belum Ada Kasus Baru yang Disimpan
            </h3>
            <p style="font-size:0.9rem; color:#CBD5E1; max-width:500px; margin:0 auto 1.2rem auto;">
                Lakukan proses diagnosa gejala tanaman buah naga terlebih dahulu, lalu simpan hasilnya pada tahap <b>Revise & Retain</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        _, c_go, _ = st.columns([1.5, 1.4, 1.5])
        with c_go:
            if st.button("🩺 Mulai Diagnosa Sekarang", key="btn_go_diag_from_saved", use_container_width=True):
                st.session_state.active_page = "Diagnosa Penyakit"
                st.rerun()

# ==============================================================================
# FOOTER KOMPLEKS MULTI-KOLOM (TAMPIL DI SETIAP HALAMAN)
# ==============================================================================
st.markdown("""
<div class="custom-footer">
    <div class="footer-grid">
        <!-- Kolom 1: Tentang Aplikasi & Developer -->
        <div>
            <div class="footer-title">
                <span>🐉</span>
                <span>CBR Buah Naga v3</span>
            </div>
            <p class="footer-text">
                Sistem Pakar Diagnosa Penyakit & Hama Tanaman Buah Naga berbasis <b>Case-Based Reasoning (CBR)</b>
                dengan perhitungan kemiripan <b>Cosine Similarity</b> untuk mendukung pertanian presisi modern.
            </p>
            <div style="margin-top:0.8rem; padding:0.75rem 0.95rem; border-radius:14px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; color:#6EE7B7; font-weight:700;">Dikembangkan Oleh</div>
                <div class="heading-font" style="font-size:0.95rem; font-weight:800; color:#FFFFFF; margin-top:2px;">Virdan Andi Wardana</div>
                <div style="font-size:0.8rem; color:#CBD5E1;">Mahasiswa Bisnis Informatika — Politeknik Negeri Banyuwangi</div>
            </div>
        </div>

        <!-- Kolom 2: Navigasi Cepat & Sosial Media -->
        <div>
            <div class="footer-title">
                <span>🌐</span>
                <span>Navigasi Cepat & Sosial Media</span>
            </div>
            <p class="footer-text" style="margin-bottom:0.65rem;">
                Terhubung langsung dengan pengembang melalui platform jejaring profesional dan repositori kode:
            </p>
            <a class="footer-link" href="https://github.com" target="_blank" rel="noopener noreferrer">
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11.02 11.02 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.8-.01 3.18 0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/></svg>
                <span>GitHub — github.com</span>
            </a>
            <a class="footer-link" href="https://instagram.com" target="_blank" rel="noopener noreferrer">
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5a4.25 4.25 0 0 0 4.25 4.25h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5a4.25 4.25 0 0 0-4.25-4.25h-8.5zm8.75 2.25a1 1 0 1 1 0 2 1 1 0 0 1 0-2zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z"/></svg>
                <span>Instagram — instagram.com</span>
            </a>
            <a class="footer-link" href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V23h-4V8zm7.5 0h3.8v2.05h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V23h-4v-7.9c0-1.88-.03-4.3-2.62-4.3-2.62 0-3.02 2.05-3.02 4.16V23h-4V8z"/></svg>
                <span>LinkedIn — linkedin.com</span>
            </a>
        </div>

        <!-- Kolom 3: Kontak Langsung -->
        <div>
            <div class="footer-title">
                <span>📬</span>
                <span>Kontak Langsung</span>
            </div>
            <p class="footer-text" style="margin-bottom:0.65rem;">
                Hubungi langsung untuk diskusi pengembangan sistem pakar, kolaborasi riset, maupun pertanyaan teknis:
            </p>
            <a class="footer-link" href="mailto:wardana4340@gmail.com" target="_blank" rel="noopener noreferrer">
                <span>✉️</span>
                <span>Email: wardana4340@gmail.com</span>
            </a>
            <a class="footer-link" href="https://wa.me/62881026132814" target="_blank" rel="noopener noreferrer">
                <span>💬</span>
                <span>WhatsApp: 0881026132814</span>
            </a>
            <a class="footer-link" href="tel:+62881026132814" target="_blank" rel="noopener noreferrer">
                <span>📞</span>
                <span>Telepon: +62 881-0261-32814</span>
            </a>
            <div style="display:flex; align-items:center; gap:10px; padding:7px 10px; font-size:0.86rem; color:#CBD5E1;">
                <span>📍</span>
                <span>Lokasi: Banyuwangi, Jawa Timur, Indonesia</span>
            </div>
        </div>
    </div>

    <div class="footer-bottom">
        <div>Sumber Referensi: <b>Pratama dkk. (2022)</b>, Jurnal Smart Teknologi 4(1), 77–82.</div>
        <div>© 2026 CBR Buah Naga v3 • Built with Streamlit & Python</div>
    </div>
</div>
""", unsafe_allow_html=True)
