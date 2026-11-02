# 🎓 Sistem Pengolahan Nilai dan Monitoring Akademik Siswa SMA

Aplikasi web berbasis **Python** dan **Streamlit** untuk mengolah nilai akademik **754 siswa SMA** (19 Kelas: `X-1` s.d. `X-8`, `XI-1` s.d. `XI-5`, dan `XII-1` s.d. `XII-6`), menghitung nilai akhir serta predikat secara otomatis, dan menyajikan visualisasi interaktif menggunakan **Plotly**.

---

## 📂 Struktur Project

```text
tugas_streamlit/
├── app.py                      # Aplikasi utama Streamlit
├── dataset_nilai_siswa.csv     # Dataset awal (754 siswa SMA di 19 kelas)
├── requirements.txt            # Daftar pustaka Python yang dibutuhkan
└── README.md                   # Dokumentasi instalasi dan penggunaan aplikasi
```

---

## 📊 Spesifikasi Dataset (`dataset_nilai_siswa.csv`)

- **Total Siswa:** 754 siswa (NIS 100% unik).
- **Total Kelas:** 19 kelas (~39–40 siswa per kelas):
  - **Kelas X (8 Kelas):** `X-1`, `X-2`, `X-3`, `X-4`, `X-5`, `X-6`, `X-7`, `X-8` (319 siswa)
  - **Kelas XI (5 Kelas):** `XI-1`, `XI-2`, `XI-3`, `XI-4`, `XI-5` (198 siswa)
  - **Kelas XII (6 Kelas):** `XII-1`, `XII-2`, `XII-3`, `XII-4`, `XII-5`, `XII-6` (237 siswa)
- **Proporsi Jenis Kelamin:** Seimbang/proporsional (`377` Laki-laki & `377` Perempuan, ~20 L dan ~20 P di setiap kelas).
- **Struktur Kolom:** `NIS`, `Nama`, `Jenis_Kelamin`, `Kelas`, `Mata_Pelajaran`, `Nilai_Tugas`, `Nilai_UTS`, `Nilai_UAS`, `Nilai_Akhir`, `Predikat`.

---

## ✨ Fitur Utama Aplikasi

1. **📊 Dashboard Akademik**
   - Kartu statistik: Total siswa, total kelas, proporsi jenis kelamin (L/P), rata-rata nilai akhir, dan jumlah siswa untuk setiap predikat (A, B, C, dan D).
   - Grafik interaktif menggunakan Plotly:
     - Grafik distribusi predikat siswa (Donut Chart).
     - Grafik rata-rata nilai akhir per mata pelajaran (Horizontal Bar Chart).
     - Grafik rata-rata nilai akhir per kelas dari `X-1` s.d. `XII-6` (Bar Chart).

2. **📋 Data Siswa**
   - Tabel data siswa lengkap dengan indikator progres nilai akhir.
   - Pencarian cepat berdasarkan **Nama** atau **NIS**.
   - Filter berdasarkan **Kelas**, **Mata Pelajaran**, dan **Jenis Kelamin (L/P)**.
   - Tombol **Unduh Data (CSV)** untuk mengekspor data yang sedang ditampilkan.

3. **✍️ Input Nilai Siswa**
   - Formulir input untuk memasukkan NIS, Nama, Jenis Kelamin, Kelas, Mata Pelajaran, Nilai Tugas, Nilai UTS, dan Nilai UAS.
   - Validasi rentang nilai (0 sampai 100) dan pemeriksaan keunikan NIS.
   - Perhitungan **Nilai Akhir** dan **Predikat** dilakukan secara otomatis dan langsung disimpan ke dalam `st.session_state` serta diperbarui ke berkas CSV.

4. **📈 Monitoring Akademik**
   - Daftar 10 siswa dengan nilai akhir tertinggi dan 10 siswa dengan nilai akhir terendah.
   - Daftar khusus siswa yang mendapatkan **Predikat D** (Nilai Akhir < 70) untuk kebutuhan remedial/bimbingan akademik.
   - Tabel rata-rata nilai setiap siswa.
   - Grafik perbandingan nilai akhir antar siswa.

5. **🧑‍🎓 Detail Siswa**
   - Filter per kelas dan pemilihan siswa untuk menampilkan kartu identitas akademik, nilai setiap mata pelajaran, nilai akhir, predikat, dan grafik perbandingan nilai siswa terhadap rata-rata kelasnya.

---

## 🚀 Petunjuk Instalasi dan Cara Menjalankan Aplikasi

```bash
cd tugas_streamlit
pip install -r requirements.txt
streamlit run app.py
```
