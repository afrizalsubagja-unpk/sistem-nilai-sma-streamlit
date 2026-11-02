import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Sistem Pengolahan Nilai & Monitoring Akademik SMA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# GAYA KUSTOM (CSS) UNTUK TAMPILAN PROFESIONAL
# ==========================================
st.markdown("""
<style>
    /* Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 700;
        color: #ffffff !important;
    }
    .main-header p {
        margin: 0.4rem 0 0 0;
        font-size: 0.95rem;
        color: #e2e8f0;
    }

    /* Kartu Statistik (KPI Cards) */
    .kpi-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 1.2rem 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        border-left: 5px solid #2563eb;
        margin-bottom: 1rem;
        transition: transform 0.15s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #475569;
        margin-top: 0.25rem;
    }

    /* Kartu Identitas Siswa */
    .profile-card {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Badge Predikat */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-A { background-color: #dcfce7; color: #166534; }
    .badge-B { background-color: #dbeafe; color: #1e40af; }
    .badge-C { background-color: #fef9c3; color: #854d0e; }
    .badge-D { background-color: #fee2e2; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# KONSTANTA & PALET WARNA
# ==========================================
FILE_DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_nilai_siswa.csv")

DAFTAR_KELAS = ["X-1", "X-2", "XI-1", "XI-2", "XII-1", "XII-2"]
DAFTAR_MAPEL = ["Informatika", "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "IPA"]

WARNA_PREDIKAT = {
    "A": "#10b981",  # Hijau Emerald
    "B": "#3b82f6",  # Biru Royal
    "C": "#f59e0b",  # Kuning Amber
    "D": "#ef4444"   # Merah Coral
}

# ==========================================
# FUNGSI PERHITUNGAN & PENGOLAHAN DATA
# ==========================================
def hitung_nilai_akhir(nilai_tugas: float, nilai_uts: float, nilai_uas: float) -> float:
    """
    Menghitung Nilai Akhir menggunakan bobot:
    30% Nilai Tugas + 30% Nilai UTS + 40% Nilai UAS.
    """
    nilai_akhir = (float(nilai_tugas) * 0.30) + (float(nilai_uts) * 0.30) + (float(nilai_uas) * 0.40)
    return round(nilai_akhir, 2)


def tentukan_predikat(nilai_akhir: float) -> str:
    """
    Menentukan kategori predikat berdasarkan Nilai Akhir:
    - A: 90 - 100
    - B: 80 - <90
    - C: 70 - <80
    - D: <70
    """
    if nilai_akhir >= 90:
        return "A"
    elif nilai_akhir >= 80:
        return "B"
    elif nilai_akhir >= 70:
        return "C"
    else:
        return "D"


def muat_dataset_awal() -> pd.DataFrame:
    """Membaca dataset CSV menggunakan Pandas dan memastikan format kolom konsisten."""
    if os.path.exists(FILE_DATASET):
        df = pd.read_csv(FILE_DATASET, dtype={"NIS": str})
        # Pastikan perhitungan nilai akhir dan predikat konsisten
        df["Nilai_Tugas"] = pd.to_numeric(df["Nilai_Tugas"], errors="coerce").fillna(0)
        df["Nilai_UTS"] = pd.to_numeric(df["Nilai_UTS"], errors="coerce").fillna(0)
        df["Nilai_UAS"] = pd.to_numeric(df["Nilai_UAS"], errors="coerce").fillna(0)
        df["Nilai_Akhir"] = df.apply(
            lambda r: hitung_nilai_akhir(r["Nilai_Tugas"], r["Nilai_UTS"], r["Nilai_UAS"]),
            axis=1
        )
        df["Predikat"] = df["Nilai_Akhir"].apply(tentukan_predikat)
        return df
    else:
        return pd.DataFrame(columns=[
            "NIS", "Nama", "Kelas", "Mata_Pelajaran",
            "Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir", "Predikat"
        ])


def inisialisasi_state():
    """Menyimpan dan mengelola dataset di dalam Streamlit Session State."""
    if "df_nilai" not in st.session_state:
        st.session_state["df_nilai"] = muat_dataset_awal()


def simpan_ke_csv(df: pd.DataFrame):
    """Menyimpan perubahan DataFrame kembali ke file CSV lokal."""
    try:
        df.to_csv(FILE_DATASET, index=False, encoding="utf-8")
    except Exception:
        pass


def buat_kartu_kpi(judul: str, nilai: str, subteks: str = "", warna_garis: str = "#2563eb"):
    """Merender kartu statistik modern menggunakan HTML."""
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {warna_garis};">
        <div class="kpi-title">{judul}</div>
        <div class="kpi-value">{nilai}</div>
        <div class="kpi-sub">{subteks}</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HALAMAN A: DASHBOARD UTAMA
# ==========================================
def tampilkan_dashboard(df: pd.DataFrame):
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard Akademik Siswa SMA</h1>
        <p>Ringkasan eksekutif pengolahan nilai, distribusi predikat, dan capaian akademik per kelas serta mata pelajaran.</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Dataset masih kosong. Silakan tambahkan data nilai siswa terlebih dahulu.")
        return

    # Metrik Utama
    total_siswa = df["NIS"].nunique()
    total_data = len(df)
    total_kelas = df["Kelas"].nunique()
    rata_nilai_akhir = df["Nilai_Akhir"].mean()

    jml_a = int((df["Predikat"] == "A").sum())
    jml_b = int((df["Predikat"] == "B").sum())
    jml_c = int((df["Predikat"] == "C").sum())
    jml_d = int((df["Predikat"] == "D").sum())

    # Baris 1: Statistik Umum
    st.subheader("📌 Ringkasan Statistik Utama")
    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        buat_kartu_kpi("Total Siswa", f"{total_siswa} Siswa", f"Total {total_data} entri nilai akademik", "#1e40af")
    with kol2:
        buat_kartu_kpi("Total Kelas", f"{total_kelas} Kelas", "Jenjang Kelas X, XI, dan XII", "#0284c7")
    with kol3:
        buat_kartu_kpi("Rata-rata Nilai Akhir", f"{rata_nilai_akhir:.2f}", "Skala penilaian 0 - 100", "#0d9488")

    # Baris 2: Jumlah Siswa per Predikat
    st.subheader("🏅 Distribusi Jumlah Predikat")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        persen_a = (jml_a / total_data * 100) if total_data else 0
        buat_kartu_kpi("Predikat A (Sangat Baik)", f"{jml_a} Siswa", f"{persen_a:.1f}% (Nilai 90 - 100)", WARNA_PREDIKAT["A"])
    with p2:
        persen_b = (jml_b / total_data * 100) if total_data else 0
        buat_kartu_kpi("Predikat B (Baik)", f"{jml_b} Siswa", f"{persen_b:.1f}% (Nilai 80 - <90)", WARNA_PREDIKAT["B"])
    with p3:
        persen_c = (jml_c / total_data * 100) if total_data else 0
        buat_kartu_kpi("Predikat C (Cukup)", f"{jml_c} Siswa", f"{persen_c:.1f}% (Nilai 70 - <80)", WARNA_PREDIKAT["C"])
    with p4:
        persen_d = (jml_d / total_data * 100) if total_data else 0
        buat_kartu_kpi("Predikat D (Perlu Bimbingan)", f"{jml_d} Siswa", f"{persen_d:.1f}% (Nilai < 70)", WARNA_PREDIKAT["D"])

    st.markdown("---")

    # Baris 3: Grafik Visualisasi Interaktif
    g_kol1, g_kol2 = st.columns(2)

    with g_kol1:
        # 1. Grafik Distribusi Predikat
        df_predikat = (
            df["Predikat"]
            .value_counts()
            .reindex(["A", "B", "C", "D"], fill_value=0)
            .reset_index()
        )
        df_predikat.columns = ["Predikat", "Jumlah Siswa"]

        fig_predikat = px.pie(
            df_predikat,
            names="Predikat",
            values="Jumlah Siswa",
            hole=0.45,
            color="Predikat",
            color_discrete_map=WARNA_PREDIKAT,
            category_orders={"Predikat": ["A", "B", "C", "D"]},
            title="<b>Distribusi Predikat Nilai Siswa</b>"
        )
        fig_predikat.update_traces(
            textposition="inside",
            textinfo="percent+label+value",
            hovertemplate="<b>Predikat %{label}</b><br>Jumlah: %{value} siswa (%{percent})<extra></extra>"
        )
        fig_predikat.update_layout(
            margin=dict(t=50, b=20, l=20, r=20),
            legend_title_text="Kategori Predikat"
        )
        st.plotly_chart(fig_predikat, use_container_width=True)

    with g_kol2:
        # 2. Grafik Rata-rata Nilai per Kelas
        df_kelas = (
            df.groupby("Kelas", as_index=False)["Nilai_Akhir"]
            .mean()
            .sort_values("Kelas")
        )
        df_kelas["Nilai_Akhir"] = df_kelas["Nilai_Akhir"].round(2)

        fig_kelas = px.bar(
            df_kelas,
            x="Kelas",
            y="Nilai_Akhir",
            text="Nilai_Akhir",
            color="Kelas",
            color_discrete_sequence=px.colors.qualitative.Safe,
            title="<b>Rata-rata Nilai Akhir per Kelas</b>",
            labels={"Nilai_Akhir": "Rata-rata Nilai Akhir", "Kelas": "Kelas"}
        )
        fig_kelas.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            hovertemplate="<b>Kelas %{x}</b><br>Rata-rata Nilai: %{y:.2f}<extra></extra>"
        )
        fig_kelas.update_layout(
            yaxis_range=[0, 108],
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_kelas, use_container_width=True)

    # Baris 4: Grafik Rata-rata Nilai per Mata Pelajaran
    df_mapel = (
        df.groupby("Mata_Pelajaran", as_index=False)[["Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir"]]
        .mean()
        .sort_values("Nilai_Akhir", ascending=True)
    )
    df_mapel["Nilai_Akhir"] = df_mapel["Nilai_Akhir"].round(2)

    fig_mapel = px.bar(
        df_mapel,
        x="Nilai_Akhir",
        y="Mata_Pelajaran",
        orientation="h",
        text="Nilai_Akhir",
        color="Nilai_Akhir",
        color_continuous_scale="Blues",
        title="<b>Rata-rata Nilai Akhir per Mata Pelajaran</b>",
        labels={"Nilai_Akhir": "Rata-rata Nilai Akhir", "Mata_Pelajaran": "Mata Pelajaran"}
    )
    fig_mapel.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Rata-rata Nilai Akhir: %{x:.2f}<extra></extra>"
    )
    fig_mapel.update_layout(
        xaxis_range=[0, 108],
        coloraxis_showscale=False,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_mapel, use_container_width=True)


# ==========================================
# HALAMAN B: DATA SISWA
# ==========================================
def tampilkan_data_siswa(df: pd.DataFrame):
    st.markdown("""
    <div class="main-header">
        <h1>📋 Data Nilai Siswa</h1>
        <p>Kelola, cari, saring berdasarkan kelas atau mata pelajaran, dan unduh laporan nilai siswa dalam format CSV.</p>
    </div>
    """, unsafe_allow_html=True)

    # Panel Filter & Pencarian
    kol_cari, kol_kelas, kol_mapel = st.columns([2, 1.5, 1.5])

    with kol_cari:
        kata_kunci = st.text_input(
            "🔍 Cari Nama atau NIS Siswa",
            placeholder="Ketik nama siswa atau nomor induk (NIS)..."
        ).strip()

    with kol_kelas:
        pilihan_kelas = sorted(df["Kelas"].unique().tolist())
        filter_kelas = st.multiselect(
            "🏫 Filter Kelas",
            options=pilihan_kelas,
            default=[],
            placeholder="Semua Kelas"
        )

    with kol_mapel:
        pilihan_mapel = sorted(df["Mata_Pelajaran"].unique().tolist())
        filter_mapel = st.multiselect(
            "📚 Filter Mata Pelajaran",
            options=pilihan_mapel,
            default=[],
            placeholder="Semua Mata Pelajaran"
        )

    # Terapkan Filter
    df_tampil = df.copy()

    if kata_kunci:
        mask_cari = (
            df_tampil["Nama"].astype(str).str.contains(kata_kunci, case=False, na=False) |
            df_tampil["NIS"].astype(str).str.contains(kata_kunci, case=False, na=False)
        )
        df_tampil = df_tampil[mask_cari]

    if filter_kelas:
        df_tampil = df_tampil[df_tampil["Kelas"].isin(filter_kelas)]

    if filter_mapel:
        df_tampil = df_tampil[df_tampil["Mata_Pelajaran"].isin(filter_mapel)]

    # Baris Info & Tombol Unduh CSV
    info_kol, unduh_kol = st.columns([3, 1])
    with info_kol:
        st.markdown(f"Menampilkan **{len(df_tampil)}** dari total **{len(df)}** data nilai siswa.")
    with unduh_kol:
        csv_bytes = df_tampil.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Data (CSV)",
            data=csv_bytes,
            file_name="data_nilai_siswa_sma.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Tabel Data Rapi dengan Konfigurasi Kolom
    st.dataframe(
        df_tampil.reset_index(drop=True),
        use_container_width=True,
        height=480,
        column_config={
            "NIS": st.column_config.TextColumn("NIS", width="small"),
            "Nama": st.column_config.TextColumn("Nama Lengkap Siswa", width="medium"),
            "Kelas": st.column_config.TextColumn("Kelas", width="small"),
            "Mata_Pelajaran": st.column_config.TextColumn("Mata Pelajaran", width="medium"),
            "Nilai_Tugas": st.column_config.NumberColumn("Nilai Tugas (30%)", format="%.1f"),
            "Nilai_UTS": st.column_config.NumberColumn("Nilai UTS (30%)", format="%.1f"),
            "Nilai_UAS": st.column_config.NumberColumn("Nilai UAS (40%)", format="%.1f"),
            "Nilai_Akhir": st.column_config.ProgressColumn(
                "Nilai Akhir",
                format="%.2f",
                min_value=0,
                max_value=100
            ),
            "Predikat": st.column_config.TextColumn("Predikat", width="small"),
        }
    )


# ==========================================
# HALAMAN C: INPUT NILAI SISWA
# ==========================================
def tampilkan_input_nilai():
    st.markdown("""
    <div class="main-header">
        <h1>✍️ Input Nilai Siswa</h1>
        <p>Formulir penambahan nilai akademik siswa dengan perhitungan Nilai Akhir dan Predikat secara otomatis.</p>
    </div>
    """, unsafe_allow_html=True)

    df_saat_ini = st.session_state["df_nilai"]

    kol_form, kol_info = st.columns([2, 1])

    with kol_info:
        st.info("""
        **📌 Ketentuan Perhitungan Otomatis:**
        - **Rumus Nilai Akhir:**
          `(Tugas × 30%) + (UTS × 30%) + (UAS × 40%)`
        - **Kategori Predikat:**
          - **A:** 90 – 100
          - **B:** 80 – < 90
          - **C:** 70 – < 80
          - **D:** Di bawah 70
        - **Validasi:**
          Rentang nilai yang diizinkan adalah **0 hingga 100**.
        """)

    with kol_form:
        with st.form("form_input_nilai", clear_on_submit=False):
            st.subheader("📝 Formulir Data & Komponen Nilai")
            f_kol1, f_kol2 = st.columns(2)
            with f_kol1:
                nis_input = st.text_input("NIS (Nomor Induk Siswa) *", placeholder="Contoh: 20241125")
                nama_input = st.text_input("Nama Lengkap Siswa *", placeholder="Contoh: Raka Pratama")
            with f_kol2:
                kelas_opsi = sorted(list(set(DAFTAR_KELAS + df_saat_ini["Kelas"].unique().tolist())))
                mapel_opsi = sorted(list(set(DAFTAR_MAPEL + df_saat_ini["Mata_Pelajaran"].unique().tolist())))
                kelas_input = st.selectbox("Kelas *", options=kelas_opsi)
                mapel_input = st.selectbox("Mata Pelajaran *", options=mapel_opsi)

            st.markdown("##### Komponen Penilaian (Rentang 0 - 100)")
            n_kol1, n_kol2, n_kol3 = st.columns(3)
            with n_kol1:
                nilai_tugas = st.number_input(
                    "Nilai Tugas (30%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    step=1.0
                )
            with n_kol2:
                nilai_uts = st.number_input(
                    "Nilai UTS (30%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    step=1.0
                )
            with n_kol3:
                nilai_uas = st.number_input(
                    "Nilai UAS (40%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    step=1.0
                )

            opsi_perbarui = st.checkbox(
                "Perbarui data jika NIS dan Mata Pelajaran yang sama sudah terdaftar",
                value=False
            )

            tombol_simpan = st.form_submit_button("💾 Simpan & Hitung Nilai Otomatis", use_container_width=True)

        if tombol_simpan:
            nis_bersih = nis_input.strip()
            nama_bersih = nama_input.strip()

            # Validasi Kelengkapan dan Rentang Nilai
            if not nis_bersih or not nama_bersih:
                st.error("⚠️ Mohon lengkapi **NIS** dan **Nama Lengkap Siswa** terlebih dahulu.")
            elif not (0 <= nilai_tugas <= 100 and 0 <= nilai_uts <= 100 and 0 <= nilai_uas <= 100):
                st.error("⚠️ Nilai Tugas, UTS, dan UAS harus berada dalam rentang 0 sampai 100.")
            else:
                nilai_akhir_hitung = hitung_nilai_akhir(nilai_tugas, nilai_uts, nilai_uas)
                predikat_hitung = tentukan_predikat(nilai_akhir_hitung)

                cek_nis_ada = df_saat_ini["NIS"].astype(str) == nis_bersih
                cek_mapel_sama = df_saat_ini["Mata_Pelajaran"] == mapel_input

                if (cek_nis_ada & cek_mapel_sama).any() and not opsi_perbarui:
                    st.warning(
                        f"⚠️ Siswa dengan NIS **{nis_bersih}** pada mata pelajaran **{mapel_input}** sudah ada. "
                        "Centang opsi perbarui jika ingin memperbarui nilai siswa tersebut."
                    )
                elif cek_nis_ada.any() and not (
                    df_saat_ini.loc[cek_nis_ada, "Nama"].iloc[0].lower() == nama_bersih.lower()
                ) and not opsi_perbarui:
                    nama_terdaftar = df_saat_ini.loc[cek_nis_ada, "Nama"].iloc[0]
                    st.error(
                        f"⚠️ NIS **{nis_bersih}** sudah digunakan oleh siswa bernama **{nama_terdaftar}**. "
                        "Gunakan NIS yang unik untuk siswa baru."
                    )
                else:
                    baris_baru = pd.DataFrame([{
                        "NIS": nis_bersih,
                        "Nama": nama_bersih,
                        "Kelas": kelas_input,
                        "Mata_Pelajaran": mapel_input,
                        "Nilai_Tugas": round(float(nilai_tugas), 2),
                        "Nilai_UTS": round(float(nilai_uts), 2),
                        "Nilai_UAS": round(float(nilai_uas), 2),
                        "Nilai_Akhir": nilai_akhir_hitung,
                        "Predikat": predikat_hitung
                    }])

                    if (cek_nis_ada & cek_mapel_sama).any() and opsi_perbarui:
                        idx = df_saat_ini[cek_nis_ada & cek_mapel_sama].index
                        for kol in baris_baru.columns:
                            st.session_state["df_nilai"].loc[idx, kol] = baris_baru[kol].values[0]
                        pesan_aksi = "diperbarui"
                    else:
                        st.session_state["df_nilai"] = pd.concat(
                            [st.session_state["df_nilai"], baris_baru],
                            ignore_index=True
                        )
                        pesan_aksi = "ditambahkan"

                    simpan_ke_csv(st.session_state["df_nilai"])

                    st.success(
                        f"✅ Data nilai **{nama_bersih}** (NIS: {nis_bersih}) berhasil {pesan_aksi}! "
                        f"**Nilai Akhir: {nilai_akhir_hitung:.2f}** | **Predikat: {predikat_hitung}**"
                    )

    st.markdown("---")
    st.subheader("🕒 5 Data Nilai Terakhir yang Tersimpan")
    st.dataframe(
        st.session_state["df_nilai"].tail(5).iloc[::-1].reset_index(drop=True),
        use_container_width=True
    )


# ==========================================
# HALAMAN D: MONITORING AKADEMIK
# ==========================================
def tampilkan_monitoring_akademik(df: pd.DataFrame):
    st.markdown("""
    <div class="main-header">
        <h1>📈 Monitoring Akademik & Evaluasi Capaian Siswa</h1>
        <p>Pemantauan siswa berprestasi tertinggi, nilai terendah, rata-rata nilai setiap siswa, serta deteksi dini siswa dengan Predikat D.</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Data nilai belum tersedia.")
        return

    # 1. Daftar Siswa Nilai Tertinggi & Terendah
    kol_atas, kol_bawah = st.columns(2)

    with kol_atas:
        st.subheader("🏆 10 Siswa dengan Nilai Akhir Tertinggi")
        df_tertinggi = (
            df.sort_values(by=["Nilai_Akhir", "Nilai_UAS"], ascending=[False, False])
            .head(10)
            .reset_index(drop=True)
        )
        df_tertinggi.index = df_tertinggi.index + 1
        st.dataframe(
            df_tertinggi[["NIS", "Nama", "Kelas", "Mata_Pelajaran", "Nilai_Akhir", "Predikat"]],
            use_container_width=True
        )

    with kol_bawah:
        st.subheader("📉 10 Siswa dengan Nilai Akhir Terendah")
        df_terendah = (
            df.sort_values(by=["Nilai_Akhir", "Nilai_UAS"], ascending=[True, True])
            .head(10)
            .reset_index(drop=True)
        )
        df_terendah.index = df_terendah.index + 1
        st.dataframe(
            df_terendah[["NIS", "Nama", "Kelas", "Mata_Pelajaran", "Nilai_Akhir", "Predikat"]],
            use_container_width=True
        )

    st.markdown("---")

    # 2. Siswa dengan Predikat D (Perlu Bimbingan / Remedial)
    st.subheader("🚨 Daftar Siswa yang Mendapatkan Predikat D (Nilai < 70)")
    df_predikat_d = df[df["Predikat"] == "D"].sort_values(by="Nilai_Akhir", ascending=True).reset_index(drop=True)

    if df_predikat_d.empty:
        st.success("🎉 Tidak ada siswa yang mendapatkan Predikat D saat ini.")
    else:
        st.warning(
            f"Terdapat **{len(df_predikat_d)} data siswa** dengan **Predikat D** (Nilai Akhir di bawah 70) "
            "yang direkomendasikan untuk mengikuti program remedial atau bimbingan akademik."
        )
        st.dataframe(
            df_predikat_d,
            use_container_width=True,
            column_config={
                "Nilai_Akhir": st.column_config.NumberColumn("Nilai Akhir", format="%.2f"),
            }
        )

    st.markdown("---")

    # 3. Rata-rata Nilai Setiap Siswa
    st.subheader("📊 Rekapitulasi Rata-rata Nilai Setiap Siswa")
    df_rata_siswa = (
        df.groupby(["NIS", "Nama", "Kelas"], as_index=False)
        .agg(
            Jumlah_Mapel=("Mata_Pelajaran", "count"),
            Rata_Tugas=("Nilai_Tugas", "mean"),
            Rata_UTS=("Nilai_UTS", "mean"),
            Rata_UAS=("Nilai_UAS", "mean"),
            Rata_Nilai_Akhir=("Nilai_Akhir", "mean")
        )
        .sort_values(by="Rata_Nilai_Akhir", ascending=False)
        .reset_index(drop=True)
    )
    df_rata_siswa["Rata_Tugas"] = df_rata_siswa["Rata_Tugas"].round(2)
    df_rata_siswa["Rata_UTS"] = df_rata_siswa["Rata_UTS"].round(2)
    df_rata_siswa["Rata_UAS"] = df_rata_siswa["Rata_UAS"].round(2)
    df_rata_siswa["Rata_Nilai_Akhir"] = df_rata_siswa["Rata_Nilai_Akhir"].round(2)
    df_rata_siswa["Predikat_Rata"] = df_rata_siswa["Rata_Nilai_Akhir"].apply(tentukan_predikat)

    st.dataframe(
        df_rata_siswa,
        use_container_width=True,
        height=360,
        column_config={
            "NIS": "NIS",
            "Nama": "Nama Siswa",
            "Kelas": "Kelas",
            "Jumlah_Mapel": "Jml Mapel",
            "Rata_Tugas": st.column_config.NumberColumn("Rata-rata Tugas", format="%.2f"),
            "Rata_UTS": st.column_config.NumberColumn("Rata-rata UTS", format="%.2f"),
            "Rata_UAS": st.column_config.NumberColumn("Rata-rata UAS", format="%.2f"),
            "Rata_Nilai_Akhir": st.column_config.ProgressColumn(
                "Rata-rata Nilai Akhir",
                format="%.2f",
                min_value=0,
                max_value=100
            ),
            "Predikat_Rata": "Predikat"
        }
    )

    st.markdown("---")

    # 4. Grafik Perbandingan Nilai Siswa Interaktif
    st.subheader("📊 Grafik Perbandingan Nilai Siswa")
    kol_opsi1, kol_opsi2 = st.columns([1.5, 2.5])

    with kol_opsi1:
        filter_kelas_grafik = st.selectbox(
            "Pilih Kelas untuk Perbandingan:",
            options=["Semua Kelas"] + sorted(df["Kelas"].unique().tolist())
        )
    with kol_opsi2:
        jumlah_tampil = st.slider(
            "Jumlah Siswa yang Ditampilkan pada Grafik:",
            min_value=5,
            max_value=min(40, len(df_rata_siswa)),
            value=min(15, len(df_rata_siswa)),
            step=5
        )

    df_grafik_siswa = df_rata_siswa.copy()
    if filter_kelas_grafik != "Semua Kelas":
        df_grafik_siswa = df_grafik_siswa[df_grafik_siswa["Kelas"] == filter_kelas_grafik]

    df_grafik_siswa = df_grafik_siswa.head(jumlah_tampil)

    fig_perbandingan = px.bar(
        df_grafik_siswa,
        x="Nama",
        y="Rata_Nilai_Akhir",
        color="Predikat_Rata",
        text="Rata_Nilai_Akhir",
        color_discrete_map=WARNA_PREDIKAT,
        category_orders={"Predikat_Rata": ["A", "B", "C", "D"]},
        hover_data=["NIS", "Kelas", "Rata_Tugas", "Rata_UTS", "Rata_UAS"],
        title=f"<b>Perbandingan Nilai Akhir Siswa ({filter_kelas_grafik})</b>",
        labels={
            "Nama": "Nama Siswa",
            "Rata_Nilai_Akhir": "Nilai Akhir",
            "Predikat_Rata": "Predikat"
        }
    )
    fig_perbandingan.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )
    fig_perbandingan.update_layout(
        yaxis_range=[0, 108],
        xaxis_tickangle=-30,
        margin=dict(t=50, b=80, l=20, r=20)
    )
    st.plotly_chart(fig_perbandingan, use_container_width=True)


# ==========================================
# HALAMAN E: DETAIL SISWA
# ==========================================
def tampilkan_detail_siswa(df: pd.DataFrame):
    st.markdown("""
    <div class="main-header">
        <h1>🧑‍🎓 Detail & Rapor Akademik Siswa</h1>
        <p>Lihat profil lengkap siswa, rincian nilai setiap mata pelajaran, nilai akhir, predikat, dan grafik komparasi nilai.</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Data siswa belum tersedia.")
        return

    # Buat daftar pilihan siswa unik berdasarkan NIS dan Nama
    df_siswa_unik = (
        df[["NIS", "Nama", "Kelas"]]
        .drop_duplicates(subset=["NIS"])
        .sort_values(by=["Kelas", "Nama"])
    )
    opsi_siswa = [
        f"{baris['NIS']} - {baris['Nama']} ({baris['Kelas']})"
        for _, baris in df_siswa_unik.iterrows()
    ]

    pilihan = st.selectbox("🔎 Pilih Siswa (Berdasarkan NIS / Nama / Kelas):", options=opsi_siswa)
    nis_terpilih = pilihan.split(" - ")[0]

    df_detail = df[df["NIS"].astype(str) == nis_terpilih].reset_index(drop=True)
    nama_siswa = df_detail["Nama"].iloc[0]
    kelas_siswa = df_detail["Kelas"].iloc[0]
    rata_akhir_siswa = df_detail["Nilai_Akhir"].mean()
    predikat_utama = tentukan_predikat(rata_akhir_siswa)

    # Identitas Siswa & Kartu Ringkasan
    st.markdown(f"""
    <div class="profile-card">
        <h3 style="margin-top:0; color:#1e3a8a;">🪪 Identitas Akademik Siswa</h3>
        <table style="width:100%; border-collapse: collapse; font-size:0.98rem;">
            <tr>
                <td style="padding: 6px 0; width: 180px; color:#475569;"><b>Nomor Induk Siswa (NIS)</b></td>
                <td style="padding: 6px 0;">: <b>{nis_terpilih}</b></td>
                <td style="padding: 6px 0; width: 180px; color:#475569;"><b>Rata-rata Nilai Akhir</b></td>
                <td style="padding: 6px 0;">: <b>{rata_akhir_siswa:.2f}</b></td>
            </tr>
            <tr>
                <td style="padding: 6px 0; color:#475569;"><b>Nama Lengkap</b></td>
                <td style="padding: 6px 0;">: <b>{nama_siswa}</b></td>
                <td style="padding: 6px 0; color:#475569;"><b>Predikat Akademik</b></td>
                <td style="padding: 6px 0;">: <span class="badge badge-{predikat_utama}">Predikat {predikat_utama}</span></td>
            </tr>
            <tr>
                <td style="padding: 6px 0; color:#475569;"><b>Kelas</b></td>
                <td style="padding: 6px 0;">: <b>{kelas_siswa}</b></td>
                <td style="padding: 6px 0; color:#475569;"><b>Jumlah Mata Pelajaran</b></td>
                <td style="padding: 6px 0;">: <b>{len(df_detail)} Mata Pelajaran</b></td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Kartu Metrik Komponen Siswa
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        buat_kartu_kpi("Rata-rata Nilai Tugas", f"{df_detail['Nilai_Tugas'].mean():.2f}", "Bobot 30%", "#3b82f6")
    with k2:
        buat_kartu_kpi("Rata-rata Nilai UTS", f"{df_detail['Nilai_UTS'].mean():.2f}", "Bobot 30%", "#6366f1")
    with k3:
        buat_kartu_kpi("Rata-rata Nilai UAS", f"{df_detail['Nilai_UAS'].mean():.2f}", "Bobot 40%", "#8b5cf6")
    with k4:
        buat_kartu_kpi(
            "Nilai Akhir & Predikat",
            f"{rata_akhir_siswa:.2f} ({predikat_utama})",
            "Hasil Evaluasi Keseluruhan",
            WARNA_PREDIKAT[predikat_utama]
        )

    # Tabel Nilai Setiap Mata Pelajaran
    st.subheader("📚 Rincian Nilai Setiap Mata Pelajaran")
    st.dataframe(
        df_detail[["Mata_Pelajaran", "Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir", "Predikat"]],
        use_container_width=True,
        column_config={
            "Mata_Pelajaran": "Mata Pelajaran",
            "Nilai_Tugas": st.column_config.NumberColumn("Nilai Tugas (30%)", format="%.1f"),
            "Nilai_UTS": st.column_config.NumberColumn("Nilai UTS (30%)", format="%.1f"),
            "Nilai_UAS": st.column_config.NumberColumn("Nilai UAS (40%)", format="%.1f"),
            "Nilai_Akhir": st.column_config.ProgressColumn(
                "Nilai Akhir",
                format="%.2f",
                min_value=0,
                max_value=100
            ),
            "Predikat": "Predikat"
        }
    )

    # Grafik Nilai Siswa
    st.subheader("📊 Grafik Visualisasi Nilai Siswa")
    g1, g2 = st.columns(2)

    with g1:
        # Grafik Batang Komponen Nilai per Mata Pelajaran
        df_melt = df_detail.melt(
            id_vars=["Mata_Pelajaran"],
            value_vars=["Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir"],
            var_name="Komponen",
            value_name="Nilai"
        )
        df_melt["Komponen"] = df_melt["Komponen"].str.replace("_", " ")

        fig_komponen = px.bar(
            df_melt,
            x="Mata_Pelajaran",
            y="Nilai",
            color="Komponen",
            barmode="group",
            text="Nilai",
            color_discrete_sequence=["#60a5fa", "#818cf8", "#34d399", "#1e3a8a"],
            title=f"<b>Rincian Nilai Komponen — {nama_siswa}</b>"
        )
        fig_komponen.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_komponen.update_layout(
            yaxis_range=[0, 110],
            margin=dict(t=50, b=30, l=20, r=20),
            legend_title_text="Komponen Nilai"
        )
        st.plotly_chart(fig_komponen, use_container_width=True)

    with g2:
        # Grafik Perbandingan Nilai Siswa vs Rata-rata Kelas
        rata_kelas = df[df["Kelas"] == kelas_siswa][["Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir"]].mean()
        rata_siswa = df_detail[["Nilai_Tugas", "Nilai_UTS", "Nilai_UAS", "Nilai_Akhir"]].mean()

        komponen_label = ["Nilai Tugas", "Nilai UTS", "Nilai UAS", "Nilai Akhir"]
        fig_banding = go.Figure()
        fig_banding.add_trace(go.Bar(
            name=nama_siswa,
            x=komponen_label,
            y=rata_siswa.values,
            text=[f"{v:.2f}" for v in rata_siswa.values],
            textposition="outside",
            marker_color="#2563eb"
        ))
        fig_banding.add_trace(go.Bar(
            name=f"Rata-rata Kelas {kelas_siswa}",
            x=komponen_label,
            y=rata_kelas.values,
            text=[f"{v:.2f}" for v in rata_kelas.values],
            textposition="outside",
            marker_color="#94a3b8"
        ))
        fig_banding.update_layout(
            barmode="group",
            title=f"<b>Perbandingan Nilai Siswa vs Rata-rata Kelas {kelas_siswa}</b>",
            yaxis_range=[0, 110],
            yaxis_title="Nilai",
            margin=dict(t=50, b=30, l=20, r=20)
        )
        st.plotly_chart(fig_banding, use_container_width=True)


# ==========================================
# NAVIGASI SIDEBAR & PROGRAM UTAMA
# ==========================================
def main():
    inisialisasi_state()
    df = st.session_state["df_nilai"]

    with st.sidebar:
        st.markdown("## 🎓 SIAKAD Nilai SMA")
        st.caption("Sistem Pengolahan Nilai & Monitoring Akademik Siswa SMA")
        st.markdown("---")

        menu = st.radio(
            "🧭 Navigasi Menu Utama",
            options=[
                "📊 Dashboard",
                "📋 Data Siswa",
                "✍️ Input Nilai Siswa",
                "📈 Monitoring Akademik",
                "🧑‍🎓 Detail Siswa"
            ]
        )

        st.markdown("---")
        st.markdown("### 📌 Ringkasan Cepat")
        st.write(f"- **Total Siswa:** {df['NIS'].nunique()} Siswa")
        st.write(f"- **Total Kelas:** {df['Kelas'].nunique()} Kelas")
        st.write(f"- **Rata-rata Nilai:** {df['Nilai_Akhir'].mean():.2f}")

        st.markdown("---")
        if st.button("🔄 Muat Ulang Dataset Awal", use_container_width=True):
            st.session_state["df_nilai"] = muat_dataset_awal()
            st.rerun()

        st.caption("© 2026 Program Magister Ilmu Komputer")

    # Routing Halaman
    if menu == "📊 Dashboard":
        tampilkan_dashboard(df)
    elif menu == "📋 Data Siswa":
        tampilkan_data_siswa(df)
    elif menu == "✍️ Input Nilai Siswa":
        tampilkan_input_nilai()
    elif menu == "📈 Monitoring Akademik":
        tampilkan_monitoring_akademik(df)
    elif menu == "🧑‍🎓 Detail Siswa":
        tampilkan_detail_siswa(df)


if __name__ == "__main__":
    main()

