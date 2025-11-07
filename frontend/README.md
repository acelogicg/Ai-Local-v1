# AI Local Frontend (React + Tailwind)

Frontend sederhana untuk berkomunikasi dengan backend Flask AI lokal.

## Jalankan

```bash
cd frontend
npm install
npm run dev
# buka http://localhost:5173
```

## Konfigurasi

Atur base URL API jika backend tidak di `http://localhost:5000`:

Buat `.env`:
```
VITE_API_BASE=http://localhost:5000
```

## Endpoint yang digunakan
- POST `/newchat` → buat percakapan baru
- POST `/chat` → kirim pesan {conversation_id, prompt}
- GET `/conversations` → daftar percakapan
- GET `/history/:id` → riwayat pesan
