# LEGACY — Wisata Batam Django Backend (tidak digunakan)

> **Repository ini adalah arsip kode eksperimen lama, BUKAN backend produksi Hallo Batam AI.**
>
> Status pada 11 November 2026: Django sudah tidak dipakai. Jangan deploy kode ini ke hosting, jangan menjalankan Procfile/manage.py sebagai layanan Hallo Batam, dan jangan mengandalkan data Chroma lokal untuk website saat ini.

## Backend yang sekarang digunakan

- Website: https://github.com/fahmifaldi61-tech/wisatabatam
- Backend: Supabase Edge Function `chat` (Deno/TypeScript)
- Database: Supabase PostgreSQL, dengan RLS dan prosedur SQL untuk pencarian dokumen wisata, sesi, riwayat chat, dan pembatasan pemakaian
- Hosting frontend: Vercel
- Peta arsitektur: https://github.com/fahmifaldi61-tech/wisatabatam/blob/main/docs/ARCHITECTURE.md (akan tersedia setelah PR dokumentasi disetujui)

## Apa isi repo lama ini?

- `backend_pariwisata/` — konfigurasi Django dan routing WSGI/ASGI.
- `api/views.py` — eksperimen API Django/DRF dengan Groq, Gemini, dan Chroma.
- `ingest.py` dan `isi_data.py` — skrip memasukkan data ke penyimpanan lokal lama.
- `Procfile` — perintah startup Gunicorn lama.

Kode ini **tidak lagi terhubung ke frontend maupun database produksi**. Ada default konfigurasi pengembangan lama di `settings.py` seperti mode DEBUG dan kunci development; **jangan pernah gunakan untuk server publik**.

## Proses pengarsipan

README ini hanya menandai repository sebagai legacy untuk menghindari penggunaan tidak sengaja. Agar **benar-benar read-only di GitHub**, setelah review/merge PR ini buka repo **Settings → Danger Zone → Archive this repository**. Tindakan archive bisa dibatalkan (unarchive); kode historis tetap ada. Jangan hapus repository karena berguna untuk referensi migrasi.
