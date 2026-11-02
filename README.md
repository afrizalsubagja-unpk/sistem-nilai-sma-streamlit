# 🎓 Sistem Pengolahan Nilai dan Monitoring Akademik Siswa SMA

Aplikasi web berbasis **Python** dan **Streamlit** untuk mengolah nilai akademik siswa SMA (Kelas X, XI, dan XII), menghitung nilai akhir serta predikat secara otomatis, dan menyajikan visualisasi interaktif menggunakan **Plotly**.

---

## 📂 Struktur Project

```text
tugas_streamlit/
├── app.py                      # Aplikasi utama Streamlit
├── dataset_nilai_siswa.csv     # Dataset awal (120 data siswa fiktif SMA)
├── requirements.txt            # Daftar pustaka Python yang dibutuhkan
└── README.md                   # Dokumentasi instalasi dan penggunaan aplikasi
```

---

## ✨ Fitur Utama Aplikasi

1. **📊 Dashboard Akademik**
   - Kartu statistik: Total siswa, total kelas, rata-rata nilai akhir, dan jumlah siswa untuk setiap predikat (A, B, C, dan D).
   - Grafik interaktif menggunakan Plotly:
     - Grafik distribusi predikat siswa (Donut Chart).
     - Grafik rata-rata nilai akhir per kelas (Bar Chart).
     - Grafik rata-rata nilai akhir per mata pelajaran (Horizontal Bar Chart).

2. **📋 Data Siswa**
   - Tabel data siswa lengkap dengan indikator progres nilai akhir.
   - Pencarian cepat berdasarkan **Nama** atau **NIS**.
   - Filter multi-pilihan berdasarkan **Kelas** dan **Mata Pelajaran**.
   - Tombol **Unduh Data (CSV)** untuk mengekspor data yang sedang ditampilkan.

3. **✍️ Input Nilai Siswa**
   - Formulir input untuk memasukkan NIS, Nama, Kelas, Mata Pelajaran, Nilai Tugas, Nilai UTS, dan Nilai UAS.
   - Validasi rentang nilai (0 sampai 100) dan pemeriksaan keunikan NIS.
   - Perhitungan **Nilai Akhir** dan **Predikat** dilakukan secara otomatis dan langsung disimpan ke dalam `st.session_state` serta diperbarui ke berkas CSV.

4. **📈 Monitoring Akademik**
   - Daftar 10 siswa dengan nilai akhir tertinggi dan 10 siswa dengan nilai akhir terendah.
   - Daftar khusus siswa yang mendapatkan **Predikat D** (Nilai Akhir < 70) untuk kebutuhan remedial/bimbingan akademik.
   - Tabel rata-rata nilai setiap siswa.
   - Grafik perbandingan nilai akhir antar siswa.

5. **🧑‍🎓 Detail Siswa**
   - Pemilihan siswa untuk menampilkan kartu identitas akademik, nilai setiap mata pelajaran, nilai akhir, predikat, dan grafik perbandingan nilai siswa terhadap rata-rata kelasnya.

---

## 🧮 Rumus Perhitungan Nilai Akhir & Predikat

$$\text{Nilai Akhir} = (\text{Nilai Tugas} \times 30\%) + (\text{Nilai UTS} \times 30\%) + (\text{Nilai UAS} \times 40\%)$$

| Predikat | Rentang Nilai Akhir | Keterangan |
| :---: | :---: | :--- |
| **A** | $90 \le \text{Nilai} \le 100$ | Sangat Baik |
| **B** | $80 \le \text{Nilai} < 90$ | Baik |
| **C** | $70 \le \text{Nilai} < 80$ | Cukup |
| **D** | $\text{Nilai} < 70$ | Perlu Bimbingan / Remedial |

---

## 🚀 Petunjuk Instalasi dan Cara Menjalankan Aplikasi

### 1. Persiapan Lingkungan Python
Pastikan **Python 3.9+** telah terpasang di komputer Anda. Buka terminal atau Command Prompt / PowerShell, lalu masuk ke direktori `tugas_streamlit`:

```bash
cd tugas_streamlit
```

### 2. Instalasi Pustaka (Dependencies)
Instal seluruh pustaka yang dibutuhkan melalui berkas `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi Streamlit
Jalankan aplikasi dengan perintah berikut:

```bash
streamlit run app.py
```

Setelah perintah dijalankan, aplikasi akan terbuka secara otomatis di peramban (browser) pada alamat:
`http://localhost:8501`

