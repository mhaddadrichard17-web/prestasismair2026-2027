# Sistem Prestasi Siswa

Website manajemen prestasi siswa dengan **backend database SQLite**.

## Fitur

- ✅ Dashboard statistik + grafik
- ✅ CRUD data prestasi (No, Nama, Kelas, Kategori Lomba, Juara, Total, Tanggal, Pembimbing)
- ✅ Upload sertifikat (JPG/PNG/PDF max 2MB)
- ✅ Filter & pencarian
- ✅ 6 jenis grafik (Kategori, Juara, Kelas, Bulan, Pembimbing, Total Poin)
- ✅ Export CSV
- ✅ Database SQLite (data persistent)

## Cara Menjalankan

### 1. Jalankan Backend Server

```bash
cd backend
python3 server.py
```

Server akan berjalan di: **http://localhost:3000**

### 2. Buka Browser

Buka: [http://localhost:3000](http://localhost:3000)

## Struktur Folder

```
artifacts/
├── index.html          # Frontend
├── backend/
│   ├── server.py       # Backend API (Python + SQLite)
│   └── prestasi.db     # Database (otomatis dibuat)
├── uploads/            # File sertifikat tersimpan di sini
└── README.md
```

## API Endpoints

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| GET    | /api/prestasi | Ambil semua data (support filter) |
| GET    | /api/prestasi/:id | Ambil satu data |
| POST   | /api/prestasi | Tambah data + upload file |
| DELETE | /api/prestasi/:id | Hapus satu data |
| DELETE | /api/prestasi | Hapus semua data |
| GET    | /api/stats | Statistik + data grafik |
| GET    | /api/filters | Opsi filter dropdown |

## Teknologi

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Python 3 (stdlib only) + SQLite
- **Tidak perlu** Node.js / npm / pip install tambahan

## Catatan

- Data tersimpan di file `backend/prestasi.db`
- File sertifikat tersimpan di folder `uploads/`
- Server harus tetap berjalan saat menggunakan website
