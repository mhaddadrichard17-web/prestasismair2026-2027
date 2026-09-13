#!/usr/bin/env python3
"""
Sistem Prestasi Siswa - Backend API
Menggunakan Python stdlib + SQLite (tanpa dependency eksternal)
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mimetypes
import re

PORT = int(__import__('os').environ.get('PORT', 3000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, 'prestasi.db')
UPLOADS_DIR = os.path.join(ROOT_DIR, 'uploads')

os.makedirs(UPLOADS_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prestasi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tingkat TEXT DEFAULT 'Kabupaten',
            juara TEXT NOT NULL,
            total REAL,
            tanggal TEXT NOT NULL,
            pembimbing TEXT NOT NULL,
            sertifikat_filename TEXT,
            sertifikat_mimetype TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        conn.execute("ALTER TABLE prestasi ADD COLUMN tingkat TEXT DEFAULT 'Kabupaten'")
        conn.commit()
    except Exception:
        pass
    conn.commit()
    conn.close()
    print(f"✅ Database siap: {DB_PATH}")

def row_to_dict(row):
    return dict(row) if row else None

class PrestasiHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def send_file_response(self, filepath, content_type=None):
        if not os.path.exists(filepath):
            self.send_error(404)
            return
        if content_type is None:
            content_type, _ = mimetypes.guess_type(filepath)
            content_type = content_type or 'application/octet-stream'
        with open(filepath, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(data))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # API routes
        if path == '/api/prestasi':
            self.handle_get_prestasi(qs)
        elif path.startswith('/api/prestasi/'):
            pid = path.split('/')[-1]
            self.handle_get_one(pid)
        elif path == '/api/stats':
            self.handle_stats()
        elif path == '/api/filters':
            self.handle_filters()
        elif path.startswith('/uploads/'):
            filename = path[9:]  # remove /uploads/
            filepath = os.path.join(UPLOADS_DIR, filename)
            self.send_file_response(filepath)
        elif path in ('/', '/index.html'):
            self.send_file_response(os.path.join(ROOT_DIR, 'index.html'), 'text/html; charset=utf-8')
        else:
            # Static files from root
            safe_path = os.path.normpath(path.lstrip('/'))
            filepath = os.path.join(ROOT_DIR, safe_path)
            if os.path.isfile(filepath) and filepath.startswith(ROOT_DIR):
                self.send_file_response(filepath)
            else:
                self.send_file_response(os.path.join(ROOT_DIR, 'index.html'), 'text/html; charset=utf-8')

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/prestasi':
            self.handle_post_prestasi()
        else:
            self.send_json({'success': False, 'message': 'Not found'}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == '/api/prestasi':
            self.handle_delete_all()
        elif path.startswith('/api/prestasi/'):
            pid = path.split('/')[-1]
            self.handle_delete_one(pid)
        else:
            self.send_json({'success': False, 'message': 'Not found'}, 404)

    def handle_get_prestasi(self, qs):
        try:
            conn = get_db()
            sql = 'SELECT * FROM prestasi WHERE 1=1'
            params = []

            search = qs.get('search', [None])[0]
            kelas = qs.get('kelas', [None])[0]
            kategori = qs.get('kategori', [None])[0]
            juara = qs.get('juara', [None])[0]

            if search:
                sql += ' AND (nama LIKE ? OR kelas LIKE ? OR kategori LIKE ? OR pembimbing LIKE ?)'
                s = f'%{search}%'
                params.extend([s, s, s, s])
            if kelas:
                sql += ' AND kelas = ?'
                params.append(kelas)
            if kategori:
                sql += ' AND kategori = ?'
                params.append(kategori)
            if juara:
                sql += ' AND juara = ?'
                params.append(juara)
            tingkat_f = qs.get('tingkat', [None])[0]
            if tingkat_f:
                sql += ' AND tingkat = ?'
                params.append(tingkat_f)

            sql += ' ORDER BY tanggal DESC, id DESC'
            rows = conn.execute(sql, params).fetchall()
            conn.close()
            data = [row_to_dict(r) for r in rows]
            self.send_json({'success': True, 'data': data})
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def handle_get_one(self, pid):
        try:
            conn = get_db()
            row = conn.execute('SELECT * FROM prestasi WHERE id = ?', (pid,)).fetchone()
            conn.close()
            if not row:
                self.send_json({'success': False, 'message': 'Data tidak ditemukan'}, 404)
                return
            self.send_json({'success': True, 'data': row_to_dict(row)})
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def handle_stats(self):
        try:
            conn = get_db()
            total = conn.execute('SELECT COUNT(*) as c FROM prestasi').fetchone()['c']
            juara1 = conn.execute("SELECT COUNT(*) as c FROM prestasi WHERE juara = '1'").fetchone()['c']
            kategori = conn.execute('SELECT COUNT(DISTINCT kategori) as c FROM prestasi').fetchone()['c']
            siswa = conn.execute('SELECT COUNT(DISTINCT nama) as c FROM prestasi').fetchone()['c']

            by_kategori = [dict(r) for r in conn.execute(
                'SELECT kategori, COUNT(*) as count FROM prestasi GROUP BY kategori ORDER BY count DESC').fetchall()]
            by_juara = [dict(r) for r in conn.execute(
                'SELECT juara, COUNT(*) as count FROM prestasi GROUP BY juara').fetchall()]
            by_kelas = [dict(r) for r in conn.execute(
                'SELECT kelas, COUNT(*) as count FROM prestasi GROUP BY kelas ORDER BY count DESC').fetchall()]
            by_pembimbing = [dict(r) for r in conn.execute(
                'SELECT pembimbing, COUNT(*) as count FROM prestasi GROUP BY pembimbing ORDER BY count DESC').fetchall()]
            by_bulan = [dict(r) for r in conn.execute(
                "SELECT strftime('%Y-%m', tanggal) as bulan, COUNT(*) as count FROM prestasi GROUP BY strftime('%Y-%m', tanggal) ORDER BY bulan").fetchall()]
            by_total = [dict(r) for r in conn.execute(
                'SELECT nama, SUM(COALESCE(total, 0)) as total_poin FROM prestasi GROUP BY nama ORDER BY total_poin DESC LIMIT 10').fetchall()]
            by_tingkat = [dict(r) for r in conn.execute(
                "SELECT COALESCE(tingkat, 'Kabupaten') as tingkat, COUNT(*) as count FROM prestasi GROUP BY COALESCE(tingkat, 'Kabupaten') ORDER BY count DESC").fetchall()]

            conn.close()
            self.send_json({
                'success': True,
                'stats': {'total': total, 'juara1': juara1, 'kategori': kategori, 'siswa': siswa},
                'charts': {
                    'byKategori': by_kategori,
                    'byJuara': by_juara,
                    'byKelas': by_kelas,
                    'byPembimbing': by_pembimbing,
                    'byBulan': by_bulan,
                    'byTotal': by_total,
                    'byTingkat': by_tingkat
                }
            })
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def handle_filters(self):
        try:
            conn = get_db()
            kelas = [r['kelas'] for r in conn.execute('SELECT DISTINCT kelas FROM prestasi ORDER BY kelas').fetchall()]
            kategori = [r['kategori'] for r in conn.execute('SELECT DISTINCT kategori FROM prestasi ORDER BY kategori').fetchall()]
            conn.close()
            self.send_json({'success': True, 'data': {'kelas': kelas, 'kategori': kategori}})
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def parse_multipart(self):
        """Parse multipart/form-data tanpa dependency eksternal"""
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            return {}, None

        # Extract boundary
        match = re.search(r'boundary=(.+)', content_type)
        if not match:
            return {}, None
        boundary = match.group(1).strip()
        if boundary.startswith('"') and boundary.endswith('"'):
            boundary = boundary[1:-1]

        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)

        fields = {}
        file_info = None

        parts = raw.split(('--' + boundary).encode())
        for part in parts:
            if not part or part == b'--\r\n' or part == b'--':
                continue
            if part.startswith(b'\r\n'):
                part = part[2:]
            if part.endswith(b'\r\n'):
                part = part[:-2]

            header_end = part.find(b'\r\n\r\n')
            if header_end == -1:
                continue
            headers_raw = part[:header_end].decode('utf-8', errors='ignore')
            body = part[header_end + 4:]

            name_match = re.search(r'name="([^"]+)"', headers_raw)
            if not name_match:
                continue
            name = name_match.group(1)

            filename_match = re.search(r'filename="([^"]*)"', headers_raw)
            if filename_match and filename_match.group(1):
                filename = filename_match.group(1)
                # Save file
                ext = os.path.splitext(filename)[1].lower()
                allowed = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf'}
                if ext not in allowed:
                    continue
                if len(body) > 2 * 1024 * 1024:
                    continue
                new_name = f"{uuid.uuid4().hex}{ext}"
                filepath = os.path.join(UPLOADS_DIR, new_name)
                with open(filepath, 'wb') as f:
                    f.write(body)
                ctype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                file_info = {'filename': new_name, 'mimetype': ctype, 'original': filename}
            else:
                fields[name] = body.decode('utf-8', errors='ignore').strip()

        return fields, file_info

    def handle_post_prestasi(self):
        try:
            fields, file_info = self.parse_multipart()

            nama = fields.get('nama', '').strip()
            kelas = fields.get('kelas', '').strip()
            kategori = fields.get('kategori', '').strip()
            tingkat = fields.get('tingkat', 'Kabupaten').strip() or 'Kabupaten'
            juara = fields.get('juara', '').strip()
            total = fields.get('total', '').strip()
            tanggal = fields.get('tanggal', '').strip()
            pembimbing = fields.get('pembimbing', '').strip()

            if not all([nama, kelas, kategori, juara, tanggal, pembimbing]):
                if file_info:
                    fp = os.path.join(UPLOADS_DIR, file_info['filename'])
                    if os.path.exists(fp):
                        os.remove(fp)
                self.send_json({'success': False, 'message': 'Field wajib belum lengkap'}, 400)
                return

            total_val = float(total) if total else None

            conn = get_db()
            cur = conn.execute('''
                INSERT INTO prestasi (nama, kelas, kategori, tingkat, juara, total, tanggal, pembimbing, sertifikat_filename, sertifikat_mimetype)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nama, kelas, kategori, tingkat, juara, total_val, tanggal, pembimbing,
                file_info['filename'] if file_info else None,
                file_info['mimetype'] if file_info else None
            ))
            conn.commit()
            new_id = cur.lastrowid
            row = conn.execute('SELECT * FROM prestasi WHERE id = ?', (new_id,)).fetchone()
            conn.close()

            self.send_json({'success': True, 'message': 'Prestasi berhasil disimpan', 'data': row_to_dict(row)}, 201)
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def handle_delete_one(self, pid):
        try:
            conn = get_db()
            row = conn.execute('SELECT * FROM prestasi WHERE id = ?', (pid,)).fetchone()
            if not row:
                conn.close()
                self.send_json({'success': False, 'message': 'Data tidak ditemukan'}, 404)
                return

            if row['sertifikat_filename']:
                fp = os.path.join(UPLOADS_DIR, row['sertifikat_filename'])
                if os.path.exists(fp):
                    os.remove(fp)

            conn.execute('DELETE FROM prestasi WHERE id = ?', (pid,))
            conn.commit()
            conn.close()
            self.send_json({'success': True, 'message': 'Data berhasil dihapus'})
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)

    def handle_delete_all(self):
        try:
            conn = get_db()
            rows = conn.execute('SELECT sertifikat_filename FROM prestasi WHERE sertifikat_filename IS NOT NULL').fetchall()
            for r in rows:
                fp = os.path.join(UPLOADS_DIR, r['sertifikat_filename'])
                if os.path.exists(fp):
                    os.remove(fp)
            conn.execute('DELETE FROM prestasi')
            conn.commit()
            conn.close()
            self.send_json({'success': True, 'message': 'Semua data berhasil dihapus'})
        except Exception as e:
            self.send_json({'success': False, 'message': str(e)}, 500)


def main():
    init_db()
    server = HTTPServer(('0.0.0.0', PORT), PrestasiHandler)
    print(f"\n✅ Server Prestasi berjalan di http://localhost:{PORT}")
    print(f"📁 Database : {DB_PATH}")
    print(f"📂 Uploads  : {UPLOADS_DIR}")
    print("Tekan Ctrl+C untuk berhenti\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        server.server_close()


if __name__ == '__main__':
    main()
