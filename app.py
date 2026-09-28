import streamlit as st
import pandas as pd
import math
import base64
import os
from datetime import datetime

st.set_page_config(
    page_title="Kalkulator Kelayakan Harga Jual Retail Beton Readymix",
    page_icon="🚛",
    layout="wide"
)

# ==============================================================================
# FUNGSI MEMBACA GAMBAR & BACKGROUND
# ==============================================================================
def find_image_file(candidates):
    for filename in candidates:
        if os.path.exists(filename):
            return filename
    return None

def get_base64_image(image_path):
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def set_background(image_file):
    encoded_string = get_base64_image(image_file)
    if encoded_string:
        ext = image_file.split('.')[-1].lower()
        if ext == 'jpg': ext = 'jpeg'
        st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                    url("data:image/{ext};base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(248, 250, 252, 0.95) !important;
    }}
</style>
""", unsafe_allow_html=True)

FILE_BG = find_image_file(["background.jpg", "background.png", "background.jpeg", "bg.jpg", "bg.png"])
if FILE_BG:
    set_background(FILE_BG)

FILE_LOGO = find_image_file([
    "logo_mixer.png", "logo_mixer.jpg", "logo_mixer.jpeg", 
    "logo.png", "logo.jpg", "mixer.png", "mixer.jpg", 
    "truk.png", "truk.jpg", "truk_mixer.png", "truk_mixer.jpg"
])

logo_base64 = get_base64_image(FILE_LOGO)

# ==============================================================================
# PROTEKSI LOGIN
# ==============================================================================
def check_password():
    PASSWORD_RAHASIA = "waskita123"
    if st.session_state.get("authenticated", False):
        return True

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    col_kiri, col_tengah, col_kanan = st.columns([1, 1.2, 1])
    
    with col_tengah:
        logo_html = ""
        if logo_base64 and FILE_LOGO:
            ext_l = FILE_LOGO.split('.')[-1].lower()
            if ext_l == 'jpg': ext_l = 'jpeg'
            logo_html = f"<div style='text-align: center; margin-bottom: 12px;'><img src='data:image/{ext_l};base64,{logo_base64}' style='height: 75px; object-fit: contain;'></div>"
        
        box_card_html = f"""<div style='background: rgba(255, 255, 255, 0.98); border: 1px solid #cbd5e1; border-radius: 12px; padding: 24px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 15px;'>
{logo_html}
<h3 style='text-align: center; color: #1e3a8a; margin: 0 0 6px 0; font-size: 1.3rem;'>🔒 Akses Terbatas</h3>
<p style='text-align: center; color: #475569; font-size: 13.5px; margin: 0;'>Silakan masukkan password untuk membuka Kalkulator Kelayakan Harga Readymix</p>
</div>"""
        st.markdown(box_card_html, unsafe_allow_html=True)
        
        with st.form("form_login"):
            input_pwd = st.text_input("Password", type="password", placeholder="Masukkan password...")
            submit_login = st.form_submit_button("Masuk / Buka Kalkulator", use_container_width=True)
            
            if submit_login:
                if input_pwd == PASSWORD_RAHASIA:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Password salah! Silakan coba lagi.")
                    
    return False

if not check_password():
    st.stop()

# ==============================================================================
# STYLING CSS
# ==============================================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 96% !important;
    }
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    .stNumberInput input, .stTextInput input {
        height: 42px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-weight: 600 !important;
        border: 1px solid #cbd5e1 !important;
    }
    .stNumberInput button {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    .stNumberInput label, .stTextInput label, .stSelectbox label, .stMultiSelect label {
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] > div {
        font-size: 1.35rem !important;
        white-space: normal !important;
        text-overflow: unset !important;
        word-break: break-word !important;
        font-weight: 700 !important;
    }
    .info-table {
        width: 100%;
        max-width: 650px;
        border-collapse: collapse;
        color: #1e3a8a;
        font-size: 14px;
        line-height: 1.6;
    }
    .info-table td.label-col { width: 160px; font-weight: 600; vertical-align: top; }
    .info-table td.sep-col { width: 20px; font-weight: 600; text-align: center; vertical-align: top; }
    .info-table td.val-col { vertical-align: top; font-weight: 500; }
    .info-box-wrapper {
        background-color: rgba(240, 247, 255, 0.95);
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 15px;
    }
    .invoice-box {
        background-color: rgba(248, 250, 252, 0.95);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 10px;
        color: #0f172a !important;
    }
    .terbilang-box {
        background-color: rgba(239, 246, 255, 0.95);
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 4px;
        margin-top: 10px;
        font-style: italic;
        color: #1e3a8a;
    }
    .val-helper {
        font-size: 12px;
        color: #0284c7;
        font-weight: 600;
        margin-top: 3px;
        margin-bottom: 6px;
    }
    .main-title-text {
        font-size: 1.95rem;
        font-weight: 800;
        line-height: 1.25;
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

def rupiah(val):
    try:
        return f"Rp {round(val):,.0f}".replace(",", ".")
    except:
        return "-"

def format_angka(val, decimal=0):
    try:
        if decimal > 0:
            return f"{val:,.{decimal}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{round(val):,.0f}".replace(",", ".")
    except:
        return "-"

def terbilang(n):
    satuan = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]
    n = int(round(n))
    if n < 12: return satuan[n]
    elif n < 20: return terbilang(n - 10) + " Belas"
    elif n < 100: return terbilang(n // 10) + " Puluh " + terbilang(n % 10)
    elif n < 200: return "Seratus " + terbilang(n - 100)
    elif n < 1000: return terbilang(n // 100) + " Ratus " + terbilang(n % 100)
    elif n < 2000: return "Seribu " + terbilang(n - 1000)
    elif n < 1000000: return terbilang(n // 1000) + " Ribu " + terbilang(n % 1000)
    elif n < 1000000000: return terbilang(n // 1000000) + " Juta " + terbilang(n % 1000000)
    elif n < 1000000000000: return terbilang(n // 1000000000) + " Milyar " + terbilang(n % 1000000000)
    else: return terbilang(n // 1000000000000) + " Triliun " + terbilang(n % 1000000000000)

LIST_MUTU_OPTIONS = [
    'B0 Slump 12 ± 2', 'K100 Slump 12 ± 2', 'K125 Slump 12 ± 2', 'K150 Slump 12 ± 2',
    'K175 Slump 12 ± 2', 'K200 Slump 12 ± 2', 'K225 Slump 12 ± 2', 'K250 Slump 12 ± 2',
    'K275 Slump 12 ± 2', 'K300 Slump 12 ± 2', 'K325 Slump 12 ± 2', 'K350 Slump 12 ± 2',
    'K400 Slump 12 ± 2', 'K500 Slump 12 ± 2', 'Fs 45 Umur 3 Hari', 'Fs 45 Umur 7 Hari'
]

LIST_JENIS_BETON = ['Beton Normal', 'Beton Fast Track', 'Beton Khusus']

LIST_PERUNTUKAN = [
    'Lantai Kerja, Jalan Setapak, Dasar Lantai, Trotoar',
    'Lantai Kerja, Jalan Setapak, Dasar Lantai',
    'Pelat lantai, kolom, balok rumah tinggal',
    'Beton bertulang, beton pracetak',
    'Jalan Utama',
    'Struktur Khusus / Lainnya'
]

DEFAULT_MASTER_LIST = [
    {'No.': 1, 'Mutu Beton': 'B0 Slump 12 ± 2', 'COGM (Rp/m³)': 920000.0, 'Efisiensi (Rp/m³)': 12000.0},
    {'No.': 2, 'Mutu Beton': 'K100 Slump 12 ± 2', 'COGM (Rp/m³)': 987208.0, 'Efisiensi (Rp/m³)': 14000.0},
    {'No.': 3, 'Mutu Beton': 'K125 Slump 12 ± 2', 'COGM (Rp/m³)': 1010000.0, 'Efisiensi (Rp/m³)': 15000.0},
    {'No.': 4, 'Mutu Beton': 'K150 Slump 12 ± 2', 'COGM (Rp/m³)': 1035000.0, 'Efisiensi (Rp/m³)': 16000.0},
    {'No.': 5, 'Mutu Beton': 'K175 Slump 12 ± 2', 'COGM (Rp/m³)': 1055000.0, 'Efisiensi (Rp/m³)': 18000.0},
    {'No.': 6, 'Mutu Beton': 'K200 Slump 12 ± 2', 'COGM (Rp/m³)': 1075000.0, 'Efisiensi (Rp/m³)': 19000.0},
    {'No.': 7, 'Mutu Beton': 'K225 Slump 12 ± 2', 'COGM (Rp/m³)': 1085000.0, 'Efisiensi (Rp/m³)': 20000.0},
    {'No.': 8, 'Mutu Beton': 'K250 Slump 12 ± 2', 'COGM (Rp/m³)': 1095193.0, 'Efisiensi (Rp/m³)': 21500.0},
    {'No.': 9, 'Mutu Beton': 'K275 Slump 12 ± 2', 'COGM (Rp/m³)': 1125000.0, 'Efisiensi (Rp/m³)': 20000.0},
    {'No.': 10, 'Mutu Beton': 'K300 Slump 12 ± 2', 'COGM (Rp/m³)': 1150000.0, 'Efisiensi (Rp/m³)': 19500.0},
    {'No.': 11, 'Mutu Beton': 'K325 Slump 12 ± 2', 'COGM (Rp/m³)': 1170000.0, 'Efisiensi (Rp/m³)': 19000.0},
    {'No.': 12, 'Mutu Beton': 'K350 Slump 12 ± 2', 'COGM (Rp/m³)': 1192256.0, 'Efisiensi (Rp/m³)': 19000.0},
    {'No.': 13, 'Mutu Beton': 'K400 Slump 12 ± 2', 'COGM (Rp/m³)': 1205000.0, 'Efisiensi (Rp/m³)': 18000.0},
    {'No.': 14, 'Mutu Beton': 'K500 Slump 12 ± 2', 'COGM (Rp/m³)': 1209193.0, 'Efisiensi (Rp/m³)': 17000.0},
    {'No.': 15, 'Mutu Beton': 'Fs 45 Umur 3 Hari', 'COGM (Rp/m³)': 1350000.0, 'Efisiensi (Rp/m³)': 15000.0},
    {'No.': 16, 'Mutu Beton': 'Fs 45 Umur 7 Hari', 'COGM (Rp/m³)': 1280000.0, 'Efisiensi (Rp/m³)': 15000.0}
]

DEFAULT_STRUCT_HINT = {
    'B0 Slump 12 ± 2': ('Beton Normal', 'Lantai Kerja, Jalan Setapak, Dasar Lantai, Trotoar'),
    'K100 Slump 12 ± 2': ('Beton Normal', 'Lantai Kerja, Jalan Setapak, Dasar Lantai'),
    'K125 Slump 12 ± 2': ('Beton Normal', 'Lantai Kerja, Jalan Setapak, Dasar Lantai'),
    'K150 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K175 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K200 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K225 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K250 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K275 Slump 12 ± 2': ('Beton Normal', 'Pelat lantai, kolom, balok rumah tinggal'),
    'K300 Slump 12 ± 2': ('Beton Normal', 'Beton bertulang, beton pracetak'),
    'K325 Slump 12 ± 2': ('Beton Normal', 'Beton bertulang, beton pracetak'),
    'K350 Slump 12 ± 2': ('Beton Normal', 'Beton bertulang, beton pracetak'),
    'K400 Slump 12 ± 2': ('Beton Normal', 'Beton bertulang, beton pracetak'),
    'K500 Slump 12 ± 2': ('Beton Normal', 'Beton bertulang, beton pracetak'),
    'Fs 45 Umur 3 Hari': ('Beton Fast Track', 'Jalan Utama'),
    'Fs 45 Umur 7 Hari': ('Beton Fast Track', 'Jalan Utama')
}

DEFAULT_PLANT_PARAMS = {
    'nama_bp': 'BP Pegangsaan',
    'kapasitas': 7392.0,
    'fixed_cost': 668523832.0,
    'slump_std': 14.0,
    'margin_std': 8.0,
    'komponen_s': 1.0,
    'jarak_std': 20.0,
    'koef_solar_jarak': 0.63,
    'koef_solar_muatan': 33923.0,
    'harga_solar': 16800.0,
    'kapasitas_tm_std': 6.0
}

# Inisialisasi Session State
if 'plant_params' not in st.session_state:
    st.session_state.plant_params = DEFAULT_PLANT_PARAMS.copy()

if 'master_table_data' not in st.session_state:
    st.session_state.master_table_data = [dict(x) for x in DEFAULT_MASTER_LIST]

if 'selected_order_mutu' not in st.session_state:
    st.session_state.selected_order_mutu = [
        'K100 Slump 12 ± 2',
        'K250 Slump 12 ± 2',
        'K350 Slump 12 ± 2',
        'K500 Slump 12 ± 2'
    ]

# DATABASE ORDER DEAL (BOOKING KAPASITAS)
if 'database_deal' not in st.session_state:
    st.session_state.database_deal = []

# Hitung Total Volume yang Sudah Deal & Sisa Kapasitas BP
vol_deal_terpakai = sum(item['Total Volume (m³)'] for item in st.session_state.database_deal)
kapasitas_awal = float(st.session_state.plant_params['kapasitas'])
sisa_kapasitas_tersedia = max(0.0, kapasitas_awal - vol_deal_terpakai)

# ==============================================================================
# HEADER
# ==============================================================================
if FILE_LOGO:
    c_logo, c_title = st.columns([1.2, 10])
    with c_logo:
        st.image(FILE_LOGO, width=110)
    with c_title:
        st.markdown("<h1 class='main-title-text' style='margin-top: 8px;'>Kalkulator Kelayakan Harga Jual Retail Beton Readymix</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 class='main-title-text'>🚛 Kalkulator Kelayakan Harga Jual Retail Beton Readymix</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏭 Status Kapasitas Batching Plant")
    st.metric("Kapasitas Terpasang", f"{format_angka(kapasitas_awal)} m³")
    st.metric("Total Ter-booking (Deal)", f"{format_angka(vol_deal_terpakai)} m³", delta=f"{len(st.session_state.database_deal)} Customer")
    st.metric("Sisa Kapasitas Tersedia", f"{format_angka(sisa_kapasitas_tersedia)} m³", delta_color="normal")
    st.markdown("---")
    
    st.markdown("### 🔄 Kontrol Sesi")
    if st.button("Reset ke Nilai Kertas Kerja Excel", use_container_width=True):
        st.session_state.plant_params = DEFAULT_PLANT_PARAMS.copy()
        st.session_state.master_table_data = [dict(x) for x in DEFAULT_MASTER_LIST]
        st.session_state.selected_order_mutu = [
            'K100 Slump 12 ± 2',
            'K250 Slump 12 ± 2',
            'K350 Slump 12 ± 2',
            'K500 Slump 12 ± 2'
        ]
        st.rerun()

    if st.button("🚪 Logout / Kunci Aplikasi", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# 4 TABS LENGKAP
tab_setting, tab_evaluasi, tab_customer_report, tab_database_deal = st.tabs([
    "⚙️ Parameter & Acuan Batching Plant",
    "📊 Evaluasi Penawaran Proyek",
    "📄 Surat Penawaran Pelanggan",
    f"📁 Database Order Deal ({len(st.session_state.database_deal)})"
])

p = st.session_state.plant_params

# ==============================================================================
# TAB 1: ACUAN BATCHING PLANT
# ==============================================================================
with tab_setting:
    st.markdown("#### 🏢 Parameter Dasar Batching Plant")
    
    with st.form("form_plant"):
        c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.4, 1.0, 1.1])
        nama_bp = c1.text_input("Unit Batching Plant", value=p['nama_bp'])
        kap_prod = c2.number_input("Kapasitas Dasar (m³)", value=float(p['kapasitas']), step=100.0)
        c2.markdown(f"<div class='val-helper'>🔍 {format_angka(kap_prod)} m³</div>", unsafe_allow_html=True)

        fc = c3.number_input("Biaya Tetap / FC (Rp)", value=float(p['fixed_cost']), step=1000000.0)
        c3.markdown(f"<div class='val-helper'>🔍 {rupiah(fc)}</div>", unsafe_allow_html=True)

        margin_def = c4.number_input("Margin (%)", value=float(p['margin_std']), step=0.5)
        komp_s = c5.number_input("Komponen S (%)", value=float(p.get('komponen_s', 1.0)), step=0.1, format="%.1f")

        d1, d2, d3, d4, d5 = st.columns([1.1, 1.3, 1.4, 1.2, 1.1])
        std_jarak = d1.number_input("Std Jarak (km)", value=float(p['jarak_std']), step=1.0)
        koef_jrk = d2.number_input("Koef. Solar Jarak (L/km)", value=float(p['koef_solar_jarak']), format="%.2f", step=0.01)
        koef_muat = d3.number_input("Koef. Solar Muatan (Rp/m³)", value=float(p['koef_solar_muatan']), step=100.0)
        d3.markdown(f"<div class='val-helper'>🔍 {rupiah(koef_muat)}</div>", unsafe_allow_html=True)

        hrg_solar = d4.number_input("Harga Solar (Rp/L)", value=float(p['harga_solar']), step=500.0)
        d4.markdown(f"<div class='val-helper'>🔍 {rupiah(hrg_solar)}</div>", unsafe_allow_html=True)

        kap_tm = d5.number_input("Kapasitas TM (m³)", value=float(p['kapasitas_tm_std']), step=1.0)

        simpan_params = st.form_submit_button("💾 Simpan Parameter Dasar BP")
        if simpan_params:
            st.session_state.plant_params.update({
                'nama_bp': nama_bp, 'kapasitas': kap_prod, 'fixed_cost': fc,
                'margin_std': margin_def, 'komponen_s': komp_s, 'jarak_std': std_jarak,
                'koef_solar_jarak': koef_jrk, 'koef_solar_muatan': koef_muat,
                'harga_solar': hrg_solar, 'kapasitas_tm_std': kap_tm
            })
            st.success("Parameter Batching Plant berhasil disimpan!")

    st.markdown("---")
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown("#### 🧱 Master Biaya COGM & Efisiensi per Mutu Beton")
    with col_t2:
        if st.button("➕ Tambah 1 Baris Baru"):
            new_no = len(st.session_state.master_table_data) + 1
            st.session_state.master_table_data.append({
                'No.': new_no,
                'Mutu Beton': None,
                'COGM (Rp/m³)': 0.0,
                'Efisiensi (Rp/m³)': 0.0
            })
            st.rerun()

    df_editor_source = pd.DataFrame(st.session_state.master_table_data)
    cols_to_display = ['No.', 'Mutu Beton', 'COGM (Rp/m³)', 'Efisiensi (Rp/m³)']
    for col in cols_to_display:
        if col not in df_editor_source.columns:
            df_editor_source[col] = 0.0 if 'Rp' in col else None
    df_editor_source = df_editor_source[cols_to_display]
    df_editor_source['No.'] = range(1, len(df_editor_source) + 1)

    edited_master_df = st.data_editor(
        df_editor_source,
        use_container_width=True,
        height=320,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            'No.': st.column_config.NumberColumn(label="No.", width=45, disabled=True),
            'Mutu Beton': st.column_config.SelectboxColumn(label="Mutu Beton", width="large", options=LIST_MUTU_OPTIONS),
            'COGM (Rp/m³)': st.column_config.NumberColumn(label="COGM (Rp/m³)", format="Rp %,d", width="small", step=1000),
            'Efisiensi (Rp/m³)': st.column_config.NumberColumn(label="Efisiensi (Rp/m³)", format="Rp %,d", width="small", step=500)
        }
    )

    if st.button("💾 Simpan Perubahan Tabel Master Beton"):
        cleaned_df = edited_master_df.copy()
        cleaned_df['No.'] = range(1, len(cleaned_df) + 1)
        st.session_state.master_table_data = cleaned_df.to_dict('records')
        st.success("Tabel Master Mutu Beton berhasil diperbarui!")

active_master_dict = {}
for r in st.session_state.master_table_data:
    if r.get('Mutu Beton'):
        active_master_dict[r['Mutu Beton']] = {
            'cogm': float(r.get('COGM (Rp/m³)') or 0.0),
            'efisiensi': float(r.get('Efisiensi (Rp/m³)') or 0.0)
        }
daftar_mutu_aktif = list(active_master_dict.keys())

# ==============================================================================
# TAB 2: EVALUASI PENAWARAN PROYEK
# ==============================================================================
order_records = []
nama_proyek = ""
nama_cust = ""
hp_cust = ""
cara_bayar = ""
jarak_proyek = p['jarak_std']

with tab_evaluasi:
    with st.expander("📝 1. Informasi Proyek & Kondisi Pengiriman", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            nama_proyek = st.text_input("Nama Proyek", value="Pengecoran Jalan Lingkungan Perumahan Artha Gading")
            nama_cust = st.text_input("Nama Customer", value="Agus")
            hp_cust = st.text_input("No HP Customer", value="0812-3456-9876")
        with col2:
            jenis_proyek = st.selectbox("Jenis Proyek", ["B2C", "B2B"])
            kategori_proyek = st.selectbox("Kategori Proyek", ["Rumah Tinggal", "Kantor/Ruko", "Pabrik/Gudang", "Jalan Utama", "Jalan Perumahan", "Kolam Renang", "Lainnya"], index=4)
            cara_bayar = st.selectbox("Cara Pembayaran", ["Cash Before Delivery", "Term of Payment (TOP)", "Cash On Delivery"])
        with col3:
            jarak_proyek = st.number_input("Jarak ke Lokasi (km)", min_value=0.0, value=21.0, step=1.0)
            slump_req = st.number_input("Slump Diminta (cm)", min_value=0.0, value=15.0, step=1.0)
            muatan_req = st.number_input("Muatan per Rit (m³)", min_value=1.0, max_value=10.0, value=4.0, step=1.0)

    selisih_jarak = max(0.0, jarak_proyek - p['jarak_std'])
    biaya_tambah_jarak = selisih_jarak * p['koef_solar_jarak'] * p['harga_solar']

    selisih_slump = max(0.0, slump_req - p['slump_std'])
    biaya_tambah_slump = selisih_slump * 20000.0

    selisih_muatan = max(0.0, p['kapasitas_tm_std'] - muatan_req)
    biaya_tambah_muatan = selisih_muatan * p['koef_solar_muatan']

    c1, c2, c3 = st.columns(3)
    c1.metric("Biaya Solar Jarak (A)", rupiah(biaya_tambah_jarak), f"+{selisih_jarak:.1f} km dari std")
    c2.metric("Biaya Bahan Slump (B)", rupiah(biaya_tambah_slump), f"+{selisih_slump:.0f} cm dari std")
    c3.metric("Biaya Selisih Muatan TM (C)", rupiah(biaya_tambah_muatan), f"-{selisih_muatan:.1f} m³/rit")

    st.markdown("---")
    st.markdown("#### 📋 2. Rincian Order, Spesifikasi & Penentuan Harga")
    
    valid_defaults = [x for x in st.session_state.selected_order_mutu if x in daftar_mutu_aktif]
    pilihan_mutu = st.multiselect(
        "Pilih Mutu Beton yang Dipesan:",
        options=daftar_mutu_aktif,
        default=valid_defaults
    )
    st.session_state.selected_order_mutu = pilihan_mutu

    mode_harga = st.radio("Metode Penentuan Harga:", ["Otomatis (Standar Margin Target %)", "Kustom / Negosiasi Harga Manual"], horizontal=True)

    if pilihan_mutu:
        cols_grid = st.columns([2.5, 2.0, 2.5, 1.5, 2.0, 1.5])
        cols_grid[0].markdown("**Mutu Beton**")
        cols_grid[1].markdown("**Jenis Beton**")
        cols_grid[2].markdown("**Peruntukan Struktur**")
        cols_grid[3].markdown("**Vol (m³)**")
        cols_grid[4].markdown("**Margin / Harga**")
        cols_grid[5].markdown("**HPP (Rp/m³)**")

        default_vol_map = {
            'K100 Slump 12 ± 2': 1000.0, 'K250 Slump 12 ± 2': 1000.0,
            'K350 Slump 12 ± 2': 1000.0, 'K500 Slump 12 ± 2': 1000.0
        }
        default_price_map = {
            'K100 Slump 12 ± 2': 1165000.0, 'K250 Slump 12 ± 2': 1275000.0,
            'K350 Slump 12 ± 2': 1383000.0, 'K500 Slump 12 ± 2': 1403000.0
        }

        persen_komp_s = p.get('komponen_s', 1.0) / 100.0
        item_no = 1
        for prod_name in pilihan_mutu:
            prod_info = active_master_dict.get(prod_name, {'cogm': 1000000.0, 'efisiensi': 15000.0})
            c = prod_info['cogm']
            d = prod_info['efisiensi']
            hpp = c + biaya_tambah_jarak + biaya_tambah_slump + biaya_tambah_muatan - d

            col_a, col_b, col_c, col_d, col_e, col_f = st.columns([2.5, 2.0, 2.5, 1.5, 2.0, 1.5])
            with col_a: st.markdown(f"**{prod_name}**")

            hint_jenis, hint_struct = DEFAULT_STRUCT_HINT.get(prod_name, ('Beton Normal', 'Beton bertulang, beton pracetak'))
            with col_b:
                idx_jns = LIST_JENIS_BETON.index(hint_jenis) if hint_jenis in LIST_JENIS_BETON else 0
                selected_jenis = st.selectbox(f"Jenis {prod_name}", LIST_JENIS_BETON, index=idx_jns, key=f"jns_{prod_name}", label_visibility="collapsed")
            with col_c:
                idx_struct = LIST_PERUNTUKAN.index(hint_struct) if hint_struct in LIST_PERUNTUKAN else 0
                selected_struktur = st.selectbox(f"Struktur {prod_name}", LIST_PERUNTUKAN, index=idx_struct, key=f"str_{prod_name}", label_visibility="collapsed")
            with col_d:
                init_vol = default_vol_map.get(prod_name, 500.0)
                vol = st.number_input(f"Vol {prod_name}", min_value=0.0, value=init_vol, step=10.0, key=f"v_{prod_name}", label_visibility="collapsed")
            with col_e:
                if mode_harga == "Otomatis (Standar Margin Target %)":
                    margin_input = st.number_input(f"Margin {prod_name}", value=p['margin_std'], step=0.5, key=f"m_{prod_name}", label_visibility="collapsed")
                    raw_harga = (hpp / (1 - (margin_input / 100.0))) if (1 - (margin_input / 100.0)) > 0 else 0
                    harga_jual = math.ceil(raw_harga / 1000.0) * 1000.0
                    st.caption(f"💡 {rupiah(harga_jual)}")
                else:
                    init_price = default_price_map.get(prod_name, round(hpp * 1.08, -3))
                    harga_jual = st.number_input(f"Harga Custom {prod_name}", value=init_price, step=1000.0, key=f"hc_{prod_name}", label_visibility="collapsed")
                    margin_input = ((harga_jual - hpp) / harga_jual * 100.0) if harga_jual > 0 else 0.0
                    st.caption(f"💡 {rupiah(harga_jual)} ({margin_input:.1f}%)")
            with col_f:
                st.write(rupiah(hpp))

            if vol > 0:
                margin_kontribusi = harga_jual - hpp
                total_mk = vol * margin_kontribusi
                biaya_komp_s = persen_komp_s * harga_jual * vol
                proporsional_fc = (p['fixed_cost'] / p['kapasitas']) * vol
                laba_prop = total_mk - proporsional_fc - biaya_komp_s
                
                if harga_jual <= hpp: status = "❌ Tolak / Rugi Variabel"
                elif laba_prop >= 0: status = "✅ Sangat Layak (Laba Penuh)"
                else: status = "⚠️ Layak (Bantu Biaya Tetap)"

                bep_vol = (p['fixed_cost'] / margin_kontribusi) if margin_kontribusi > 0 else 0
                pendapatan = vol * harga_jual
                biaya_var = vol * hpp

                order_records.append({
                    'No.': item_no,
                    'Jenis Beton': selected_jenis,
                    'Jenis Struktur': selected_struktur,
                    'Mutu Beton': prod_name,
                    'HPP': hpp,
                    'Margin (%)': margin_input,
                    'Vol Order (m³)': vol,
                    'Harga Jual': harga_jual,
                    'Margin Kontribusi (Rp/m³)': margin_kontribusi,
                    'Total Margin Kontribusi': total_mk,
                    'Biaya Komponen S (Rp)': biaya_komp_s,
                    'Laba Operasi Proporsional Proyek (Rp)': laba_prop,
                    'Status': status,
                    'BEP Volume (m³)': bep_vol,
                    'Total Pendapatan (Rp)': pendapatan,
                    'Total Biaya Variabel': biaya_var
                })
                item_no += 1

        df_order = pd.DataFrame(order_records)

        st.markdown("---")
        st.markdown("#### 📊 Hasil Evaluasi Finansial Proyek")

        if not df_order.empty:
            tot_vol = df_order['Vol Order (m³)'].sum()
            tot_pendapatan = df_order['Total Pendapatan (Rp)'].sum()
            tot_mk = df_order['Total Margin Kontribusi'].sum()
            tot_var = df_order['Total Biaya Variabel'].sum()
            tot_komp_s = df_order['Biaya Komponen S (Rp)'].sum()
            tot_biaya = tot_var + p['fixed_cost'] + tot_komp_s
            laba_bersih = tot_pendapatan - tot_biaya

            # ==================================================================
            # MONITORING KELAYAKAN SISA KAPASITAS BATCHING PLANT
            # ==================================================================
            if tot_vol > sisa_kapasitas_tersedia:
                st.error(f"🚨 **PERINGATAN KAPASITAS PABRIK MELEBIHI BATAS!**\n\nVolume yang diminta pelanggan ini (**{format_angka(tot_vol)} m³**) melebihi sisa kapasitas batching plant yang tersedia (**{format_angka(sisa_kapasitas_tersedia)} m³** dari kapasitas total {format_angka(kapasitas_awal)} m³).")
            else:
                st.success(f"✅ **Kapasitas BP Mencukupi:** Volume order (**{format_angka(tot_vol)} m³**) masih dalam batas sisa kapasitas tersedia (**{format_angka(sisa_kapasitas_tersedia)} m³**).")

            k1, k2, k3, k4, k5 = st.columns([1.3, 1.2, 1.2, 1.2, 1.1])
            k1.metric("Total Pendapatan", rupiah(tot_pendapatan), f"Volume: {format_angka(tot_vol)} m³")
            k2.metric("Margin Kontribusi", rupiah(tot_mk), f"{(tot_mk/tot_pendapatan*100):.1f}% Omzet")
            k3.metric("Biaya Komponen S", rupiah(tot_komp_s), f"{p.get('komponen_s', 1.0):.1f}% Omzet")
            k4.metric("Laba Operasi", rupiah(laba_bersih))
            k5.metric("Kelayakan", "Sangat Layak" if laba_bersih >= 0 else ("Layak (Bantu FC)" if tot_mk > 0 else "Tolak"))

            st.markdown("##### Tabel Evaluasi Kelayakan per Produk:")
            df_view = df_order[['No.', 'Jenis Beton', 'Jenis Struktur', 'Mutu Beton', 'Vol Order (m³)', 'HPP', 'Harga Jual', 'Margin (%)', 'Total Margin Kontribusi', 'Biaya Komponen S (Rp)', 'Laba Operasi Proporsional Proyek (Rp)', 'Status', 'BEP Volume (m³)', 'Total Pendapatan (Rp)']].copy()
            df_view['Vol Order (m³)'] = df_view['Vol Order (m³)'].apply(lambda x: f"{format_angka(x)} m³")
            df_view['HPP'] = df_view['HPP'].apply(rupiah)
            df_view['Harga Jual'] = df_view['Harga Jual'].apply(rupiah)
            df_view['Total Margin Kontribusi'] = df_view['Total Margin Kontribusi'].apply(rupiah)
            df_view['Biaya Komponen S (Rp)'] = df_view['Biaya Komponen S (Rp)'].apply(rupiah)
            df_view['Laba Operasi Proporsional Proyek (Rp)'] = df_view['Laba Operasi Proporsional Proyek (Rp)'].apply(rupiah)
            df_view['Margin (%)'] = df_view['Margin (%)'].apply(lambda x: f"{x:.1f}%")
            df_view['BEP Volume (m³)'] = df_view['BEP Volume (m³)'].apply(lambda x: f"{format_angka(x)} m³")
            df_view['Total Pendapatan (Rp)'] = df_view['Total Pendapatan (Rp)'].apply(rupiah)
            st.dataframe(df_view, use_container_width=True, hide_index=True)

            # TOMBOL SIMPAN KE DATABASE DEAL
            st.markdown("---")
            col_save1, col_save2 = st.columns([2, 1])
            with col_save1:
                st.markdown("##### 🤝 Simpan Transaksi ke Database Order Deal")
                st.caption(f"Jika customer **{nama_cust}** deal membeli dengan volume **{format_angka(tot_vol)} m³**, klik tombol di sebelah kanan untuk membukukan order ini dan mengurangi sisa kapasitas BP.")
            with col_save2:
                if st.button("💾 Simpan Order Ini Sebagai DEAL", use_container_width=True, type="primary"):
                    st.session_state.database_deal.append({
                        'Waktu Deal': datetime.now().strftime("%d-%m-%Y %H:%M"),
                        'Nama Customer': nama_cust,
                        'Nama Proyek': nama_proyek,
                        'Total Volume (m³)': float(tot_vol),
                        'Total Nilai Deal (Rp)': float(tot_pendapatan),
                        'Margin Kontribusi (Rp)': float(tot_mk),
                        'Laba Operasi (Rp)': float(laba_bersih),
                        'Detail Produk': ", ".join([f"{r['Mutu Beton']} ({format_angka(r['Vol Order (m³)'])} m³)" for _, r in df_order.iterrows()])
                    })
                    st.success(f"🎉 Order an. {nama_cust} ({format_angka(tot_vol)} m³) berhasil disimpan ke Database Deal!")
                    st.rerun()
    else:
        st.info("Pilih minimal satu mutu beton di atas untuk melakukan kalkulasi order.")

# ==============================================================================
# TAB 3: SURAT PENAWARAN PELANGGAN
# ==============================================================================
with tab_customer_report:
    df_order = pd.DataFrame(order_records)
    col_head1, col_head2 = st.columns([2.5, 1.5])
    with col_head1:
        st.subheader("📑 Surat Penawaran Harga (Customer Quotation)")
    
    if not df_order.empty:
        total_dpp = df_order['Total Pendapatan (Rp)'].sum()
        ppn_11 = total_dpp * 0.11
        grand_total = total_dpp + ppn_11
        teks_terbilang = f"{terbilang(grand_total).strip()} Rupiah"

        rows_html = ""
        for _, r in df_order.iterrows():
            rows_html += f"""
            <tr style="border-bottom: 1px solid #cbd5e1; text-align: left;">
                <td style="padding: 10px 8px; text-align: center;">{r['No.']}</td>
                <td style="padding: 10px 8px;">{r['Jenis Beton']}</td>
                <td style="padding: 10px 8px;">{r['Jenis Struktur']}</td>
                <td style="padding: 10px 8px;"><b>{r['Mutu Beton']}</b></td>
                <td style="padding: 10px 8px; text-align: right;">{format_angka(r['Vol Order (m³)'])} m³</td>
                <td style="padding: 10px 8px; text-align: right;">{rupiah(r['Harga Jual'])}</td>
                <td style="padding: 10px 8px; text-align: right;"><b>{rupiah(r['Total Pendapatan (Rp)'])}</b></td>
            </tr>
            """

        html_quotation = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Surat Penawaran - {nama_proyek}</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #1e293b; line-height: 1.5; }}
    .header {{ border-bottom: 2px solid #2563eb; padding-bottom: 12px; margin-bottom: 24px; }}
    .title {{ font-size: 22px; font-weight: bold; color: #1e3a8a; margin: 0; }}
    table.meta {{ margin-bottom: 24px; font-size: 14px; border-collapse: collapse; }}
    table.meta td {{ padding: 3px 0; }}
    table.items {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px; }}
    table.items th {{ background-color: #f1f5f9; padding: 10px 8px; border-bottom: 2px solid #cbd5e1; text-align: left; }}
    .summary-box {{ float: right; width: 340px; margin-bottom: 20px; font-size: 14px; }}
    .summary-box table {{ width: 100%; border-collapse: collapse; }}
    .summary-box td {{ padding: 6px 0; }}
    .terbilang {{ clear: both; background: #f8fafc; border-left: 4px solid #3b82f6; padding: 12px 16px; margin: 20px 0; font-style: italic; color: #1e3a8a; }}
    .notes {{ font-size: 12px; color: #475569; margin-top: 25px; }}
    @media print {{ body {{ margin: 0; }} }}
</style>
</head>
<body onload="window.print()">
    <div class="header">
        <h1 class="title">SURAT PENAWARAN HARGA BETON READYMIX</h1>
    </div>

    <table class="meta">
        <tr><td style="width: 150px;"><b>Customer</b></td><td style="width: 15px;">:</td><td>{nama_cust} ({hp_cust})</td></tr>
        <tr><td><b>Nama Proyek</b></td><td>:</td><td>{nama_proyek}</td></tr>
        <tr><td><b>Unit BP</b></td><td>:</td><td>{p['nama_bp']}</td></tr>
        <tr><td><b>Jarak Tempuh</b></td><td>:</td><td>{format_angka(jarak_proyek, 1)} km</td></tr>
        <tr><td><b>Cara Pembayaran</b></td><td>:</td><td>{cara_bayar}</td></tr>
    </table>

    <table class="items">
        <thead>
            <tr>
                <th style="width: 30px; text-align: center;">No.</th>
                <th>Jenis Beton</th>
                <th>Peruntukan Struktur</th>
                <th>Spesifikasi Mutu</th>
                <th style="text-align: right;">Volume</th>
                <th style="text-align: right;">Harga Satuan (Rp/m³)</th>
                <th style="text-align: right;">Jumlah Harga (Rp)</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>

    <div class="summary-box">
        <table>
            <tr style="border-bottom: 1px solid #e2e8f0;"><td><b>Jumlah Harga (DPP)</b></td><td style="text-align: right;"><b>{rupiah(total_dpp)}</b></td></tr>
            <tr style="border-bottom: 1px solid #e2e8f0;"><td>PPN 11%</td><td style="text-align: right;">{rupiah(ppn_11)}</td></tr>
            <tr style="font-size: 16px; color: #1e3a8a;"><td style="padding-top: 8px;"><b>Total Harga</b></td><td style="text-align: right; padding-top: 8px;"><b>{rupiah(grand_total)}</b></td></tr>
        </table>
    </div>

    <div class="terbilang">
        <b>Terbilang :</b><br>
        {teks_terbilang}
    </div>

    <div class="notes">
        <b>Catatan:</b>
        <ol style="margin-top: 5px; padding-left: 20px;">
            <li>Harga beton di atas sudah termasuk pajak PPN 11%.</li>
            <li>Pihak pembeli bertanggung jawab terhadap kelayakan jalan, keamanan untuk dilalui truk mixer.</li>
            <li>Pembuatan benda uji dilakukan sesuai standar Batching Plant.</li>
            <li>Pembayaran dapat dilakukan dengan transfer ke nomor rekening: **0710201400001** a.n. **PT. Waskita Beton Precast Tbk**, **Bank BJB Jabar dan Banten**.</li>
        </ol>
    </div>
</body>
</html>"""

        with col_head2:
            st.download_button(
                label="📥 Unduh Surat Penawaran (PDF / Cetak)",
                data=html_quotation.encode('utf-8'),
                file_name=f"Penawaran_Readymix_{nama_cust}.html",
                mime="text/html"
            )

        st.markdown(f"""
        <div class="info-box-wrapper">
            <table class="info-table">
                <tr><td class="label-col">Customer</td><td class="sep-col">:</td><td class="val-col">{nama_cust} ({hp_cust})</td></tr>
                <tr><td class="label-col">Nama Proyek</td><td class="sep-col">:</td><td class="val-col">{nama_proyek}</td></tr>
                <tr><td class="label-col">Unit BP</td><td class="sep-col">:</td><td class="val-col">{p['nama_bp']}</td></tr>
                <tr><td class="label-col">Jarak Tempuh</td><td class="sep-col">:</td><td class="val-col">{format_angka(jarak_proyek, 1)} km</td></tr>
                <tr><td class="label-col">Cara Pembayaran</td><td class="sep-col">:</td><td class="val-col">{cara_bayar}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        df_inv = df_order[['No.', 'Jenis Beton', 'Jenis Struktur', 'Mutu Beton', 'Vol Order (m³)', 'Harga Jual', 'Total Pendapatan (Rp)']].copy()
        df_inv.columns = ['No.', 'Jenis Beton', 'Peruntukan Struktur', 'Spesifikasi Mutu', 'Volume', 'Harga Satuan (Rp/m³)', 'Jumlah Harga (Rp)']
        df_inv['Volume'] = df_inv['Volume'].apply(lambda x: f"{format_angka(x)} m³")
        df_inv['Harga Satuan (Rp/m³)'] = df_inv['Harga Satuan (Rp/m³)'].apply(rupiah)
        df_inv['Jumlah Harga (Rp)'] = df_inv['Jumlah Harga (Rp)'].apply(rupiah)
        st.table(df_inv)

        c_left, c_right = st.columns([1.2, 1])
        with c_right:
            st.markdown(f"""
            <div class="invoice-box">
                <table style="width:100%; border-collapse: collapse; font-size: 15px;">
                    <tr style="border-bottom: 1px solid #e2e8f0; height: 32px;">
                        <td><b>Jumlah Harga (DPP)</b></td>
                        <td style="text-align: right;"><b>{rupiah(total_dpp)}</b></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0; height: 32px;">
                        <td>PPN 11%</td>
                        <td style="text-align: right;">{rupiah(ppn_11)}</td>
                    </tr>
                    <tr style="height: 42px; font-size: 18px; color: #1e3a8a;">
                        <td><b>Total Harga</b></td>
                        <td style="text-align: right;"><b>{rupiah(grand_total)}</b></td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="terbilang-box">
            <b>Terbilang :</b><br>
            {teks_terbilang}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        **Catatan:**
        1. Harga beton di atas sudah termasuk pajak PPN 11%.
        2. Pihak pembeli bertanggung jawab terhadap kelayakan jalan, keamanan untuk dilalui truk mixer.
        3. Pembuatan benda uji dilakukan sesuai standar Batching Plant.
        4. Pembayaran dapat dilakukan dengan transfer ke nomor rekening: **0710201400001** a.n. **PT. Waskita Beton Precast Tbk**, **Bank BJB Jabar dan Banten**.
        """)
    else:
        st.warning("Belum ada data pemesanan yang aktif.")

# ==============================================================================
# TAB 4: DATABASE ORDER DEAL & TRACKING KAPASITAS (BARU)
# ==============================================================================
with tab_database_deal:
    st.subheader("📁 Database Penjualan Deal & Kontrol Kapasitas Produksi")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric("Kapasitas Terpasang BP", f"{format_angka(kapasitas_awal)} m³")
    col_d2.metric("Total Kapasitas Terpakai", f"{format_angka(vol_deal_terpakai)} m³", f"{(vol_deal_terpakai/kapasitas_awal*100):.1f}% Utilisasi")
    col_d3.metric("Sisa Kapasitas Siap Jual", f"{format_angka(sisa_kapasitas_tersedia)} m³", delta=f"{format_angka(sisa_kapasitas_tersedia)} m³ sisa", delta_color="normal")

    st.markdown("---")

    if st.session_state.database_deal:
        df_deal_display = pd.DataFrame(st.session_state.database_deal)
        
        # Format tampilan tabel deal
        df_show = df_deal_display.copy()
        df_show['No.'] = range(1, len(df_show) + 1)
        df_show['Total Volume (m³)'] = df_show['Total Volume (m³)'].apply(lambda x: f"{format_angka(x)} m³")
        df_show['Total Nilai Deal (Rp)'] = df_show['Total Nilai Deal (Rp)'].apply(rupiah)
        df_show['Margin Kontribusi (Rp)'] = df_show['Margin Kontribusi (Rp)'].apply(rupiah)
        df_show['Laba Operasi (Rp)'] = df_show['Laba Operasi (Rp)'].apply(rupiah)

        st.dataframe(df_show[['No.', 'Waktu Deal', 'Nama Customer', 'Nama Proyek', 'Total Volume (m³)', 'Total Nilai Deal (Rp)', 'Margin Kontribusi (Rp)', 'Laba Operasi (Rp)', 'Detail Produk']], use_container_width=True, hide_index=True)

        st.markdown("#### 🗑️ Batalkan / Hapus Transaksi Deal")
        cust_list = [f"{i+1}. {item['Nama Customer']} - {item['Nama Proyek']} ({format_angka(item['Total Volume (m³)'])} m³)" for i, item in enumerate(st.session_state.database_deal)]
        pilih_hapus = st.selectbox("Pilih Order yang ingin dibatalkan / dihapus:", cust_list)
        
        if st.button("❌ Batalkan Order Ini & Kembalikan Kapasitas"):
            idx_del = cust_list.index(pilih_hapus)
            cust_name_del = st.session_state.database_deal[idx_del]['Nama Customer']
            del st.session_state.database_deal[idx_del]
            st.success(f"Order an. {cust_name_del} berhasil dihapus. Sisa kapasitas BP bertambah kembali!")
            st.rerun()
    else:
        st.info("💡 Belum ada customer yang berstatus DEAL. Ketika penawaran pada Tab 2 disepakati pembeli, klik tombol **'Simpan Order Ini Sebagai DEAL'** untuk otomatis mengurangi kuota kapasitas produksi BP.")
