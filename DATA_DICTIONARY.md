# Data Dictionary — Corporate Rate Hotel Pertamina 2026

## Kolom asli

| Kolom | Deskripsi |
|---|---|
| No | Nomor/kode internal dari data sumber. |
| Group/ Non Group | Kategori hotel apakah masuk group atau non group. |
| Nama Group/ Non Group | Nama jaringan/group hotel atau individu/non group. |
| City | Wilayah/provinsi lokasi hotel. |
| Nama Hotel | Nama hotel. |
| Email | Kontak email hotel. |
| Publish Rate | Harga publish rate hotel. |
| Offering Corporate Rate 2026 | Harga corporate rate yang ditawarkan untuk 2026. |
| Nilai Selisih | Selisih antara publish rate dan corporate rate. Nilai positif berarti corporate rate lebih murah. |
| Result | Status rekomendasi dari hasil perbandingan rate. |
| Next Action | Tindak lanjut yang harus dilakukan. |
| Checking Remarks | Catatan checking atau tipe kamar. |
| Status | Status pengerjaan data. |

## Kolom turunan di dashboard

| Kolom Turunan | Logika |
|---|---|
| Result Raw | Salinan mentah kolom Result sebelum cleaning. |
| Next Action Raw | Salinan mentah kolom Next Action sebelum cleaning. |
| Result | Hasil normalisasi kategori, misalnya `Recommend ` menjadi `Recommend`. |
| Next Action | Hasil normalisasi action, misalnya `Sign Kontrak`, `Done`, `Review Rate`. |
| Email Missing | True jika email kosong, blank, dash, atau karakter tersembunyi. |
| Remarks Missing | True jika Checking Remarks kosong. |
| Is Recommend | True jika Result = Recommend. |
| Is Revise | True jika Result = Revise. |
| Is Sign Kontrak | True jika Next Action = Sign Kontrak. |
| Corporate Status | Corporate Lebih Murah, Corporate Lebih Mahal, atau Sama dengan Publish. |
| Gap Band | Negatif, Sama, 0-100rb, 100-300rb, 300-500rb, >500rb. |
| Discount vs Publish % | Nilai Selisih / Publish Rate. |
| Corporate Rate Ratio | Offering Corporate Rate 2026 / Publish Rate. |
| Priority | P1 - Urgent Negative, P2 - Revise Positive, P3 - Sign Kontrak, Maintain High Opportunity, Maintain Rate, Review Manual. |
| SLA Status | Indikator tracking sederhana: Critical, On Track, Completed. |
| Latitude / Longitude | Koordinat perkiraan wilayah untuk visualisasi peta. |
