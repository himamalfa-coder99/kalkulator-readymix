import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Kalkulator Kelayakan Harga Readymix",
    page_icon="🏗️",
    layout="wide"
)

# Styling CSS
st.markdown("""
<style>
    .metric-card {
        background: #f8fafc;
        border-radius: 10px;
        padding: 16px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 12px;
    }
    .info-table {
        width: 100%;
        max-width: 650px;
        border-collapse: collapse;
        color: #1e3a8a;
        font-size: 15px;
        line-height: 1.8;
    }
    .info-table td.label-col {
        width: 160px;
        font-weight: 600;
        vertical-align: top;
    }
    .info-table td.sep-col {
        width: 20px;
        font-weight: 600;
        text-align: center;
        vertical-align: top;
    }
    .info-table td.val-col {
        vertical-align: top;
        font-weight: 500;
    }
    .info-box-wrapper {
        background-color: #f0f7ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 20px;
    }
    .invoice-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px 24px;
        margin-top: 10px;
    }
    .terbilang-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        margin-top: 15px;
        font-style: italic;
        color: #1e3a8a;
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
            formatted = f"{val:,.{decimal}f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return formatted
        return f"{round(val):,.0f}".replace(",", ".")
    except:
        return "-"

def terbilang(n):
    satuan = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]
    n = int(round(n))
    if n < 12:
        return satuan[n]
    elif n < 20:
        return terbilang(n - 10) + " Belas"
    elif n < 100:
        return terbilang(n // 10) + " Puluh " + terbilang(n % 10)
    elif n < 200:
        return "Seratus " + terbilang(n - 100)
    elif n < 1000:
        return terbilang(n // 100) + " Ratus " + terbilang(n % 100)
    elif n < 2000:
        return "Seribu " + terbilang(n - 1000)
    elif n < 1000000:
        return terbilang(n // 1000) + " Ribu " + terbilang(n % 1000)
    elif n < 1000000000:
        return terbilang(n // 1000000) + " Juta " + terbilang(n % 1000000)
    elif n < 1000000000000:
        return terbilang(n // 1000000000) + " Milyar " + terbilang(n % 1000000000)
    else:
        return terbilang(n // 1000000000000) + " Triliun " + terbilang(n % 1000000000000)

MASTER_DATABASE = {
    'B0 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Lantai Kerja, Jalan Setapak, Dasar Lantai, Trotoar',
        'cogm': 920000.0, 'efisiensi': 12000.0
    },
    'K100 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Lantai Kerja, Jalan Setapak, Dasar Lantai',
        'cogm': 987208.0, 'efisiensi': 14000.0
    },
    'K125 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Lantai Kerja, Jalan Setapak, Dasar Lantai',
        'cogm': 1010000.0, 'efisiensi': 15000.0
    },
    'K150 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1035000.0, 'efisiensi': 16000.0
    },
    'K175 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1055000.0, 'efisiensi': 18000.0
    },
    'K200 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1075000.0, 'efisiensi': 19000.0
    },
    'K225 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1085000.0, 'efisiensi': 20000.0
    },
    'K250 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1095193.0, 'efisiensi': 21500.0
    },
    'K275 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Pelat lantai, kolom, balok rumah tinggal',
        'cogm': 1125000.0, 'efisiensi': 20000.0
    },
    'K300 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Beton bertulang, beton pracetak',
        'cogm': 1150000.0, 'efisiensi': 19500.0
    },
    'K325 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Beton bertulang, beton pracetak',
        'cogm': 1170000.0, 'efisiensi': 19000.0
    },
    'K350 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Beton bertulang, beton pracetak',
        'cogm': 1192256.0, 'efisiensi': 19000.0
    },
    'K400 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Beton bertulang, beton pracetak',
        'cogm': 1205000.0, 'efisiensi': 18000.0
    },
    'K500 Slump 12 ± 2': {
        'jenis_beton': 'Beton Normal',
        'jenis_struktur': 'Beton bertulang, beton pracetak',
        'cogm': 1209193.0, 'efisiensi': 17000.0
    },
    'Fs 45 Umur 3 Hari': {
        'jenis_beton': 'Beton Fast Track',
        'jenis_struktur': 'Jalan Utama',
        'cogm': 1350000.0, 'efisiensi': 15000.0
    },
    'Fs 45 Umur 7 Hari': {
        'jenis_beton': 'Beton Fast Track',
        'jenis_struktur': 'Jalan Utama',
        'cogm': 1280000.0, 'efisiensi': 15000.0
    }
}

daftar_mutu_lengkap = list(MASTER_DATABASE.keys())

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

if 'plant_params' not in st.session_state:
    st.session_state.plant_params = DEFAULT_PLANT_PARAMS.copy()

if 'master_produk' not in st.session_state:
    st.session_state.master_produk = MASTER_DATABASE.copy()

if 'selected_order_mutu' not in st.session_state:
    st.session_state.selected_order_mutu = [
        'K100 Slump 12 ± 2',
        'K250 Slump 12 ± 2',
        'K350 Slump 12 ± 2',
        'K500 Slump 12 ± 2'
    ]

# Header
st.title("🏗️ Kalkulator & Evaluasi Kelayakan Harga Jual Readymix")
st.caption("Batching Plant Retail & Project Financial Calculator")

# Sidebar Reset
with st.sidebar:
    st.markdown("### 🔄 Kontrol Sesi")
    if st.button("Reset ke Nilai Kertas Kerja Excel"):
        st.session_state.plant_params = DEFAULT_PLANT_PARAMS.copy()
        st.session_state.master_produk = MASTER_DATABASE.copy()
        st.session_state.selected_order_mutu = [
            'K100 Slump 12 ± 2',
            'K250 Slump 12 ± 2',
            'K350 Slump 12 ± 2',
            'K500 Slump 12 ± 2'
        ]
        st.rerun()

tab_setting, tab_evaluasi, tab_customer_report = st.tabs([
    "⚙️ Parameter & Acuan Batching Plant",
    "📊 Evaluasi Penawaran Proyek",
    "📄 Surat Penawaran Pelanggan"
])

p = st.session_state.plant_params

# ==============================================================================
# TAB 1: ACUAN BATCHING PLANT
# ==============================================================================
with tab_setting:
    st.subheader("⚙️ Parameter Acuan Batching Plant")
    st.caption("Ubah parameter acuan dasar batching plant dan master biaya produk di sini.")
    
    with st.form("form_plant"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("##### 🏢 Biaya Tetap & Kapasitas Plant")
            nama_bp = st.text_input("Unit BP", value=p['nama_bp'])
            kap_prod = st.number_input("Kapasitas Produksi (m³)", value=float(p['kapasitas']), step=100.0)
            st.caption(f"💡 Terbaca: **{format_angka(kap_prod)} m³**")
            fc = st.number_input("Biaya Tetap / Fixed Cost (Rp)", value=float(p['fixed_cost']), step=1000000.0)
            st.caption(f"💡 Terbaca: **{rupiah(fc)}**")
            margin_def = st.number_input("Default Target Margin (%)", value=float(p['margin_std']), step=0.5)
            st.caption(f"💡 Terbaca: **{margin_def:.1f}%**")
            
        with col_s2:
            st.markdown("##### 🚛 Parameter Pengiriman & BBM Solar")
            std_jarak = st.number_input("Standar Jarak Supply (km)", value=float(p['jarak_std']), step=1.0)
            st.caption(f"💡 Terbaca: **{format_angka(std_jarak, 1)} km**")
            koef_jrk = st.number_input("Koef. Solar Jarak (Liter/km)", value=float(p['koef_solar_jarak']), format="%.2f", step=0.01)
            koef_muat = st.number_input("Koef. Solar Muatan (Rp/m³)", value=float(p['koef_solar_muatan']), format="%.2f", step=100.0)
            st.caption(f"💡 Terbaca: **{rupiah(koef_muat)}**")
            hrg_solar = st.number_input("Harga Solar (Rp/Ltr)", value=float(p['harga_solar']), step=500.0)
            st.caption(f"💡 Terbaca: **{rupiah(hrg_solar)}**")
            kap_tm = st.number_input("Kapasitas Normal TM (m³)", value=float(p['kapasitas_tm_std']), step=1.0)
            st.caption(f"💡 Terbaca: **{format_angka(kap_tm)} m³**")

        st.markdown("---")
        st.markdown("##### 🧱 Master Biaya Variabel (COGM) & Efisiensi per Mutu Beton")
        
        temp_master = {}
        cols_hdr = st.columns([3, 2, 2, 3])
        cols_hdr[0].markdown("**Mutu Beton**")
        cols_hdr[1].markdown("**Jenis Beton**")
        cols_hdr[2].markdown("**Biaya COGM (Rp/m³)**")
        cols_hdr[3].markdown("**Efisiensi (Rp/m³)**")

        for prod_name in daftar_mutu_lengkap:
            vals = st.session_state.master_produk.get(prod_name, MASTER_DATABASE[prod_name])
            c_prod, c_type, c_cogm, c_eff = st.columns([3, 2, 2, 3])
            c_prod.write(f"**{prod_name}**")
            c_type.caption(f"`{vals['jenis_beton']}`")
            
            new_cogm = c_cogm.number_input(f"COGM {prod_name}", value=float(vals['cogm']), step=1000.0, key=f"cfg_c_{prod_name}", label_visibility="collapsed")
            new_eff = c_eff.number_input(f"Efisiensi {prod_name}", value=float(vals['efisiensi']), step=500.0, key=f"cfg_e_{prod_name}", label_visibility="collapsed")
            
            temp_master[prod_name] = {
                'jenis_beton': vals['jenis_beton'],
                'jenis_struktur': vals['jenis_struktur'],
                'cogm': new_cogm,
                'efisiensi': new_eff
            }

        simpan = st.form_submit_button("💾 Simpan Semua Perubahan Acuan")
        if simpan:
            st.session_state.plant_params.update({
                'nama_bp': nama_bp, 'kapasitas': kap_prod, 'fixed_cost': fc,
                'margin_std': margin_def, 'jarak_std': std_jarak,
                'koef_solar_jarak': koef_jrk, 'koef_solar_muatan': koef_muat,
                'harga_solar': hrg_solar, 'kapasitas_tm_std': kap_tm
            })
            st.session_state.master_produk = temp_master
            st.success("Semua parameter acuan dan master mutu beton berhasil disimpan!")

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
    with st.expander("📝 1. Input Informasi Proyek & Kondisi Pengiriman", expanded=True):
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

    # Deviasi Biaya (A, B, C)
    selisih_jarak = max(0.0, jarak_proyek - p['jarak_std'])
    biaya_tambah_jarak = round((selisih_jarak * p['koef_solar_jarak'] * p['harga_solar']) / 100.0) * 100.0

    selisih_slump = max(0.0, slump_req - p['slump_std'])
    biaya_tambah_slump = round(selisih_slump * 20000.0)

    selisih_muatan = max(0.0, p['kapasitas_tm_std'] - muatan_req)
    biaya_tambah_muatan = round(selisih_muatan * p['koef_solar_muatan'])

    with st.container():
        st.markdown("##### 📌 Komponen Biaya Tambahan Deviasi:")
        c1, c2, c3 = st.columns(3)
        c1.metric("Biaya Solar Jarak (A)", rupiah(biaya_tambah_jarak), f"+{selisih_jarak:.1f} km dari standar")
        c2.metric("Biaya Bahan Slump (B)", rupiah(biaya_tambah_slump), f"+{selisih_slump:.0f} cm dari standar")
        c3.metric("Biaya Selisih Muatan TM (C)", rupiah(biaya_tambah_muatan), f"-{selisih_muatan:.1f} m³/rit dari normal")

    st.markdown("---")
    st.markdown("#### 📋 2. Rincian Order, Spesifikasi Struktur & Penentuan Harga")
    
    pilihan_mutu = st.multiselect(
        "Pilih Mutu Beton yang Dipesan pada Proyek Ini:",
        options=daftar_mutu_lengkap,
        default=st.session_state.selected_order_mutu
    )
    st.session_state.selected_order_mutu = pilihan_mutu

    mode_harga = st.radio("Metode Penentuan Harga:", ["Otomatis (Standar Margin Target %)", "Kustom / Negosiasi Harga Manual"], horizontal=True)

    if pilihan_mutu:
        cols_grid = st.columns([3, 2, 2, 2, 2])
        cols_grid[0].markdown("**Mutu & Jenis Beton**")
        cols_grid[1].markdown("**Jenis Struktur**")
        cols_grid[2].markdown("**Vol Order (m³)**")
        cols_grid[3].markdown("**Margin (%) / Harga Jual**")
        cols_grid[4].markdown("**HPP (Rp/m³)**")

        default_vol_map = {
            'K100 Slump 12 ± 2': 500.0,
            'K250 Slump 12 ± 2': 700.0,
            'K350 Slump 12 ± 2': 600.0,
            'K500 Slump 12 ± 2': 1000.0
        }
        default_price_map = {
            'K100 Slump 12 ± 2': 1150000.0,
            'K250 Slump 12 ± 2': 1250000.0,
            'K350 Slump 12 ± 2': 1395000.0,
            'K500 Slump 12 ± 2': 1415000.0
        }

        list_opsi_struktur = [
            'Lantai Kerja, Jalan Setapak, Dasar Lantai, Trotoar',
            'Lantai Kerja, Jalan Setapak, Dasar Lantai',
            'Pelat lantai, kolom, balok rumah tinggal',
            'Beton bertulang, beton pracetak',
            'Jalan Utama',
            'Struktur Khusus / Lainnya'
        ]

        item_no = 1
        for prod_name in pilihan_mutu:
            prod_info = st.session_state.master_produk.get(prod_name, MASTER_DATABASE[prod_name])
            c = prod_info['cogm']
            d = prod_info['efisiensi']
            hpp = c + biaya_tambah_jarak + biaya_tambah_slump + biaya_tambah_muatan - d

            col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 2, 2, 2])
            
            with col_a:
                st.markdown(f"**{prod_name}**")
                st.caption(f"Tipe: `{prod_info['jenis_beton']}`")

            with col_b:
                default_struct = prod_info['jenis_struktur']
                opsi_final = list_opsi_struktur if default_struct in list_opsi_struktur else [default_struct] + list_opsi_struktur
                idx_struct = opsi_final.index(default_struct) if default_struct in opsi_final else 0
                selected_struktur = st.selectbox(
                    f"Struktur {prod_name}",
                    options=opsi_final,
                    index=idx_struct,
                    key=f"str_{prod_name}",
                    label_visibility="collapsed"
                )

            with col_c:
                init_vol = default_vol_map.get(prod_name, 100.0)
                vol = st.number_input(f"Vol {prod_name}", min_value=0.0, value=init_vol, step=10.0, key=f"v_{prod_name}", label_visibility="collapsed")

            with col_d:
                if mode_harga == "Otomatis (Standar Margin Target %)":
                    margin_input = st.number_input(f"Margin {prod_name}", value=p['margin_std'], step=0.5, key=f"m_{prod_name}", label_visibility="collapsed")
                    harga_jual = round(hpp / (1 - (margin_input / 100.0)) / 1000.0) * 1000.0 if (1 - (margin_input / 100.0)) > 0 else 0
                    st.caption(f"💡 Terhitung: **{rupiah(harga_jual)}**")
                else:
                    init_price = default_price_map.get(prod_name, round(hpp * 1.08, -3))
                    harga_jual = st.number_input(f"Harga Custom {prod_name}", value=init_price, step=5000.0, key=f"hc_{prod_name}", label_visibility="collapsed")
                    margin_input = ((harga_jual - hpp) / harga_jual * 100.0) if harga_jual > 0 else 0.0
                    st.caption(f"💡 Terbaca: **{rupiah(harga_jual)}** ({margin_input:.1f}%)")

            with col_e:
                st.write(rupiah(hpp))

            if vol > 0:
                margin_kontribusi = harga_jual - hpp
                total_mk = vol * margin_kontribusi
                proporsional_fc = (p['fixed_cost'] / p['kapasitas']) * vol
                laba_prop = total_mk - proporsional_fc
                
                if harga_jual <= hpp:
                    status = "❌ Tolak / Rugi Variabel"
                elif laba_prop >= 0:
                    status = "✅ Sangat Layak (Laba Penuh)"
                else:
                    status = "⚠️ Layak (Bantu Biaya Tetap)"

                bep_vol = (p['fixed_cost'] / margin_kontribusi) if margin_kontribusi > 0 else 0
                pendapatan = vol * harga_jual
                biaya_var = vol * hpp

                order_records.append({
                    'No.': item_no,
                    'Jenis Beton': prod_info['jenis_beton'],
                    'Jenis Struktur': selected_struktur,
                    'Mutu Beton': prod_name,
                    'HPP': hpp,
                    'Margin (%)': margin_input,
                    'Vol Order (m³)': vol,
                    'Harga Jual': harga_jual,
                    'Total Margin Kontribusi': total_mk,
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
            tot_biaya = df_order['Total Biaya Variabel'].sum() + p['fixed_cost']
            laba_bersih = tot_pendapatan - tot_biaya

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total Pendapatan", rupiah(tot_pendapatan), f"Volume: {format_angka(tot_vol)} m³")
            k2.metric("Total Margin Kontribusi", rupiah(tot_mk), f"{(tot_mk/tot_pendapatan*100):.1f}% Omzet")
            k3.metric("Laba Operasi", rupiah(laba_bersih))
            k4.metric("Status Kelayakan", "Sangat Layak" if laba_bersih >= 0 else ("Layak (Bantu FC)" if tot_mk > 0 else "Tolak"))

            st.markdown("##### Tabel Evaluasi Kelayakan per Produk:")
            df_view = df_order[[
                'No.', 
                'Jenis Beton',
                'Jenis Struktur',
                'Mutu Beton', 
                'Vol Order (m³)', 
                'HPP', 
                'Harga Jual', 
                'Margin (%)', 
                'Total Margin Kontribusi', 
                'Laba Operasi Proporsional Proyek (Rp)', 
                'Status', 
                'BEP Volume (m³)', 
                'Total Pendapatan (Rp)'
            ]].copy()

            df_view['Vol Order (m³)'] = df_view['Vol Order (m³)'].apply(lambda x: f"{format_angka(x)} m³")
            df_view['HPP'] = df_view['HPP'].apply(rupiah)
            df_view['Harga Jual'] = df_view['Harga Jual'].apply(rupiah)
            df_view['Total Margin Kontribusi'] = df_view['Total Margin Kontribusi'].apply(rupiah)
            df_view['Laba Operasi Proporsional Proyek (Rp)'] = df_view['Laba Operasi Proporsional Proyek (Rp)'].apply(rupiah)
            df_view['Margin (%)'] = df_view['Margin (%)'].apply(lambda x: f"{x:.1f}%")
            df_view['BEP Volume (m³)'] = df_view['BEP Volume (m³)'].apply(lambda x: f"{format_angka(x)} m³")
            df_view['Total Pendapatan (Rp)'] = df_view['Total Pendapatan (Rp)'].apply(rupiah)
            
            st.dataframe(df_view, use_container_width=True, hide_index=True)
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

        # Bangun Dokumen HTML Cetak Resmi yang otomatis memicu print/save as PDF
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
    .sub {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
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
        <div class="sub">Batching Plant: {p['nama_bp']} | Sistem Kelayakan Penawaran Retail & Proyek</div>
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
        <tbody>
            {rows_html}
        </tbody>
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
            <li>Pembayaran dapat dilakukan dengan transfer ke nomor rekening: <b>0710201400001</b> a.n. <b>PT. Waskita Beton Precast Tbk</b>, <b>Bank BJB Jabar dan Banten</b>.</li>
        </ol>
    </div>
</body>
</html>"""

        with col_head2:
            st.download_button(
                label="📥 Unduh Surat Penawaran (PDF / Cetak)",
                data=html_quotation.encode('utf-8'),
                file_name=f"Penawaran_Readymix_{nama_cust}.html",
                mime="text/html",
                help="Klik untuk mengunduh penawaran. Buka filenya, menu cetak & Simpan ke PDF akan otomatis muncul!"
            )

        # Header Info Tabel di Layar
        st.markdown(f"""
        <div class="info-box-wrapper">
            <table class="info-table">
                <tr>
                    <td class="label-col">Customer</td>
                    <td class="sep-col">:</td>
                    <td class="val-col">{nama_cust} ({hp_cust})</td>
                </tr>
                <tr>
                    <td class="label-col">Proyek</td>
                    <td class="sep-col">:</td>
                    <td class="val-col">{nama_proyek}</td>
                </tr>
                <tr>
                    <td class="label-col">Unit BP</td>
                    <td class="sep-col">:</td>
                    <td class="val-col">{p['nama_bp']}</td>
                </tr>
                <tr>
                    <td class="label-col">Jarak Tempuh</td>
                    <td class="sep-col">:</td>
                    <td class="val-col">{format_angka(jarak_proyek, 1)} km</td>
                </tr>
                <tr>
                    <td class="label-col">Cara Pembayaran</td>
                    <td class="sep-col">:</td>
                    <td class="val-col">{cara_bayar}</td>
                </tr>
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
        st.warning("Belum ada data pemesanan yang aktif. Silakan pilih mutu beton dan isi volume di tab Evaluasi Penawaran Proyek.")