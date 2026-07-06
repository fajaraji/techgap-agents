# DNA Proyek: TechGap AI
Ini adalah panduan instruksi inti yang berlaku untuk semua agen (Parser, Auditor, dan Analyzer) agar mencegah halusinasi dan memastikan perilaku Agentic Engineering yang aman.

## 1. Kebijakan Anti-Halusinasi (Strict Evidence-Based)
- **TIDAK BOLEH** menyimpulkan bahwa seorang pengguna memiliki skill tertentu (misal: "Pandai Python") HANYA dari bio profil atau deskripsi singkat repositori mereka.
- Agen (khususnya `skill-github-auditor`) **WAJIB** melihat ke dalam struktur file, membaca `requirements.txt`, `package.json`, atau isi kode aktual yang relevan untuk memvalidasi keberadaan skill tersebut.
- Jika tidak ada bukti di repositori yang dapat diverifikasi, agen HARUS menandai skill tersebut sebagai `[BELUM DIMILIKI]` dengan jujur.

## 2. Penggunaan Memori & Spesifikasi (Spec-Driven)
- Agen harus selalu merujuk ke file `specs/skill_taxonomy.yaml` saat mencoba mengkategorikan skill dari Job Description (JD). 
- Jika ada skill di JD yang tidak ada persis di YAML, agen harus memetakannya ke kategori yang paling dekat secara teknis.

## 3. Context Hygiene & Privasi
- Jangan pernah membocorkan `GITHUB_TOKEN` atau `GEMINI_API_KEY` ke output console atau logs.
- Sebelum memproses profil GitHub atau CV pengguna (jika ada), samarkan (mask) informasi PII seperti email pengguna, nomor HP, atau token API yang tidak sengaja ter-*commit* di dalam repo.

## 4. Pelaporan Objektif
- Rekomendasi proyek portofolio di akhir proses HARUS bersifat spesifik dan menyasar langsung gap yang ditemukan.
- *Contoh Buruk*: "Buatlah proyek menggunakan Python."
- *Contoh Baik*: "Berdasarkan gap yang kami temukan (kurangnya pengalaman API Design), buatlah proyek RESTful API sederhana menggunakan FastAPI (Python) yang melakukan operasi CRUD ke database SQLite."
