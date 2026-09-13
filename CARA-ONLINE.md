# Cara Membuat Website Prestasi Online (Gratis)

Ada 2 pilihan:

---

## Opsi A — Paling Mudah (Frontend saja)
**Cocok jika:** setiap orang menyimpan datanya sendiri di browser masing-masing.

### Cara 1: Netlify Drop (paling cepat, tanpa akun wajib)

1. Buka: https://app.netlify.com/drop
2. Drag & drop file **index.html** ke halaman tersebut
3. Tunggu beberapa detik → muncul link online (contoh: `https://random-name.netlify.app`)
4. Bagikan link itu ke teman/guru

> Catatan: Data tersimpan di browser masing-masing pengunjung (localStorage).

### Cara 2: GitHub Pages (permanen & gratis)

1. Buat akun di https://github.com (gratis)
2. Buat repository baru (contoh: `prestasi-siswa`)
3. Upload file `index.html`
4. Settings → Pages → Source: Deploy from branch `main`
5. Link akan jadi: `https://username.github.io/prestasi-siswa`

---

## Opsi B — Multi-user + Database Bersama (Recommended untuk sekolah)

Semua orang melihat & menambah data yang sama.

### Platform gratis yang disarankan:

| Platform | Link | Keterangan |
|----------|------|------------|
| **Railway** | https://railway.app | Mudah deploy Python + SQLite |
| **Render** | https://render.com | Free tier, cocok untuk backend |
| **Fly.io** | https://fly.io | Performa bagus |
| **PythonAnywhere** | https://www.pythonanywhere.com | Khusus Python, mudah |

### Langkah singkat di Railway:

1. Daftar di https://railway.app (pakai GitHub)
2. New Project → Deploy from GitHub / Upload
3. Upload folder `backend/` + `index.html` + `uploads/`
4. Set Start Command: `python server.py`
5. Railway akan kasih URL publik otomatis

---

## Opsi C — Tunnel Sementara (untuk demo cepat)

Jika server sudah jalan di komputer Anda (`python3 server.py`):

```bash
npx localtunnel --port 3000
```

Akan muncul link seperti: `https://xxxx.loca.lt`  
Link ini **sementara** (hilang jika komputer dimatikan).

---

## Rekomendasi

- **Demo / pribadi** → pakai **Netlify Drop** (Opsi A)
- **Sekolah / banyak user** → pakai **Railway** atau **Render** (Opsi B)

Setelah online, bagikan link-nya ke siapa saja.
