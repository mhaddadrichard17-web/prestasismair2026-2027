# Deploy ke Railway (Data Bisa Dilihat Semua User)

Ikuti langkah berikut satu per satu.

---

## Langkah 1 — Siapkan Akun

1. Buka **https://railway.app**
2. Klik **Login** → pilih **Login with GitHub**
3. Izinkan akses GitHub

---

## Langkah 2 — Upload Project ke GitHub

1. Buka **https://github.com/new**
2. Repository name: `prestasi-siswa` (boleh diganti)
3. Pilih **Public**
4. Klik **Create repository**
5. Upload semua file project ini:
   - `index.html`
   - `backend/` (folder)
   - `uploads/` (folder)
   - `Procfile`
   - `requirements.txt`
   - `railway.toml`
   - `runtime.txt`

### Cara upload cepat (di GitHub):
- Klik **uploading an existing file**
- Drag semua file & folder di atas
- Commit

---

## Langkah 3 — Deploy di Railway

1. Di Railway dashboard, klik **New Project**
2. Pilih **Deploy from GitHub repo**
3. Pilih repository `prestasi-siswa`
4. Railway akan otomatis detect dan deploy
5. Tunggu sampai status **Success** (hijau)

---

## Langkah 4 — Dapatkan Link Online

1. Klik project yang baru dibuat
2. Klik tab **Settings** → **Networking**
3. Klik **Generate Domain**
4. Copy link yang muncul, contoh:
   ```
   https://prestasi-siswa-production-xxxx.up.railway.app
   ```
5. **Bagikan link itu** ke teman / guru / siswa

---

## Langkah 5 — Cek

1. Buka link di browser
2. Pastikan muncul **✅ Database Connected**
3. Tambah data prestasi
4. Buka dari HP / komputer lain → data harus muncul sama

---

## Catatan Penting

- **Free tier Railway** cukup untuk demo & sekolah kecil
- Database SQLite tersimpan di server Railway
- Semua user melihat data yang sama
- Jika redeploy total, data SQLite bisa hilang (tambah Volume di Settings jika ingin permanen)

---

## Alternatif jika Railway penuh

Gunakan **Render.com**:
1. New → Web Service
2. Connect GitHub repo yang sama
3. Start Command: `python backend/server.py`
4. Generate free URL

---

Selesai! Website Anda sekarang online dan data bisa dilihat bersama.
