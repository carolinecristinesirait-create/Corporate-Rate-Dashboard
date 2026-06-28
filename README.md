# Dashboard Corporate Rate Hotel Pertamina 2026

Dashboard ini dibuat dengan **Python + Streamlit + Plotly** untuk menganalisis dataset Excel `corporate_rate_hotel_pertamina_2026.xlsx`.

Tema visual dibuat dengan nuansa **biru, merah, hijau, dan kuning** agar terasa seperti dashboard korporat Pertamina: sidebar gelap, kartu KPI, chart interaktif, filter global, export data, dan 10 halaman analisis.

## Struktur repository

```text
pertamina_streamlit_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── run_local.bat
├── .gitignore
├── .streamlit/
│   └── config.toml
└── data/
    └── corporate_rate_hotel_pertamina_2026.xlsx
```

## Halaman dashboard

1. **Executive Overview**  
   KPI utama, komposisi Result, top city, top group, distribusi selisih, snapshot hotel.

2. **Regional Analysis**  
   Analisis wilayah/provinsi, peta interaktif, top provinsi, kinerja wilayah, provinsi revise tertinggi.

3. **Group Performance**  
   Scorecard group, top group, bubble chart total selisih vs revise, komposisi result per group.

4. **Top Opportunity Hotels**  
   Hotel dengan nilai selisih tertinggi, hotel selisih negatif, opportunity list, highlight hotel.

5. **Price Gap Analytics**  
   Scatter publish vs corporate rate, kategori nilai selisih, waterfall kontribusi band harga, boxplot wilayah.

6. **Revise Priority**  
   Prioritas negosiasi P1/P2, provinsi revise tertinggi, group revise tertinggi, daftar prioritas hotel.

7. **Action Tracker**  
   Status next action, pipeline tindak lanjut, hotel yang masih perlu action, action berdasarkan result.

8. **Hotel Explorer**  
   Direktori hotel, pencarian, detail hotel profile, perbandingan beberapa hotel, export filtered data.

9. **Data Quality**  
   Missing email, missing checking remarks, completeness, data yang perlu dilengkapi, quality checklist.

10. **Executive Recommendations**  
   Ringkasan temuan, rekomendasi tindak lanjut, impact-effort matrix, 30-60-90 day plan, target focus.

## Cara menjalankan lokal

### Opsi 1 — Windows cepat

Klik dua kali:

```text
run_local.bat
```

### Opsi 2 — Manual

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# atau Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Buka URL lokal yang muncul, biasanya:

```text
http://localhost:8501
```

## Cara deploy ke Streamlit Community Cloud dari GitHub

1. Buat repository baru di GitHub, misalnya `pertamina-hotel-dashboard`.
2. Upload semua isi folder ini ke repository.
3. Pastikan file berikut ada di root repository:
   - `app.py`
   - `requirements.txt`
   - folder `data/` berisi file Excel
4. Buka Streamlit Community Cloud.
5. Pilih **New app**.
6. Pilih repository GitHub yang sudah dibuat.
7. Isi:
   - Branch: `main`
   - Main file path: `app.py`
8. Klik **Deploy**.

## Dataset

Dashboard otomatis membaca file:

```text
data/corporate_rate_hotel_pertamina_2026.xlsx
```

Jika ingin mengganti dataset tanpa mengubah repository, gunakan fitur **Upload Excel baru** di sidebar dashboard.

## Catatan cleaning data

Dashboard melakukan cleaning otomatis:

- menghapus spasi ganda dan karakter tersembunyi,
- menormalisasi kategori `Result`, misalnya `Recommend ` menjadi `Recommend`,
- menormalisasi `Next Action`,
- mengonversi nilai rate menjadi numerik,
- menandai missing `Email` dan `Checking Remarks`,
- membuat kolom turunan seperti `Corporate Status`, `Gap Band`, `Priority`, `Discount vs Publish %`, dan koordinat wilayah untuk peta.

Karena ada cleaning kategori, jumlah `Recommend` bisa berbeda sedikit dari tampilan contoh jika contoh tersebut memakai kategori mentah yang masih mengandung spasi.

## Kolom utama yang digunakan

- `No`
- `Group/ Non Group`
- `Nama Group/ Non Group`
- `City`
- `Nama Hotel`
- `Email`
- `Publish Rate`
- `Offering Corporate Rate 2026`
- `Nilai Selisih`
- `Result`
- `Next Action`
- `Checking Remarks`
- `Status`

## Tips modifikasi

- Ubah warna di dictionary `COLORS` pada `app.py`.
- Tambahkan halaman baru pada list `PAGE_OPTIONS`, lalu buat fungsi page-nya.
- Untuk mengganti file default, letakkan file Excel baru di folder `data/` dan sesuaikan `DEFAULT_DATA_PATH` di `app.py`.


## Catatan Versi No Upload

Versi ini tidak menampilkan uploader Excel di sidebar. Dataset otomatis dibaca dari `data/corporate_rate_hotel_pertamina_2026.xlsx`. Jika folder data tidak ikut terunggah ke GitHub, aplikasi tetap memakai fallback dataset bawaan yang sudah tertanam di `app.py`.
