# Screener MA Kuncup

Screener saham otomatis untuk mendeteksi pola MA Kuncup / MA Ketat di Bursa Efek Indonesia (BEI).

Berdasarkan artikel [@ikhwanuddin](https://x.com/ikhwanuddin/status/2028329791657541637) yang merujuk teknik Pak T [@TradingDiary2](https://x.com/TradingDiary2).

---

## Cara Penggunaan

### Instalasi

```bash
pip install -r requirements.txt
```

### Jalankan Manual

```bash
# Scan saham dari stocks.csv (30 saham populer), tampilkan di terminal
python main.py

# Scan semua saham BEI
python main.py --all

# Scan semua saham BEI dan simpan hasil ke data/results/
python main.py --all --save

# Scan stocks.csv dan simpan hasil
python main.py --save
```

---

## Otomasi dengan GitHub Actions

Screener ini berjalan **otomatis setiap Senin–Jumat jam 17:00 WIB (10:00 UTC)** menggunakan GitHub Actions.

Workflow yang berjalan:
1. Mengambil daftar semua saham yang terdaftar di BEI
2. Menjalankan screener MA Kuncup untuk setiap saham
3. Menyimpan hasil ke folder `data/results/`
4. Meng-commit dan men-push hasil ke repository secara otomatis

### Trigger Manual

Workflow juga bisa dijalankan secara manual melalui tab **Actions** di GitHub, lalu pilih workflow **Daily MA Kuncup Screener** dan klik **Run workflow**.

---

## Hasil Screener

Hasil screener tersimpan di folder `data/results/` dengan format nama file:

| File | Keterangan |
|------|-----------|
| `data/results/YYYY-MM-DD_screener.csv` | Semua saham yang diproses beserta indikatornya |
| `data/results/YYYY-MM-DD_signals.csv` | Hanya saham yang memenuhi sinyal MA Kuncup |

### Kolom Output

| Kolom | Keterangan |
|-------|-----------|
| `Ticker` | Kode saham (e.g. `BBCA.JK`) |
| `Price` | Harga penutupan terakhir |
| `MA_Spread_Pct` | Selisih MA tertinggi dan terendah sebagai % harga |
| `MA_Tight` | `True` jika spread ≤ 3% (MA Kuncup terdeteksi) |
| `Signal` | `True` jika sinyal aktif |
| `MA5`–`MA200` | Nilai masing-masing moving average |

---

## Struktur Project

```
screener-ma-kuncup/
├── main.py                        # Entry point utama
├── requirements.txt
├── stocks.csv                     # Daftar saham populer (default)
├── data/
│   ├── all_stocks.csv             # Daftar semua saham BEI
│   └── results/                   # Hasil screener harian
│       └── YYYY-MM-DD_screener.csv
├── screener/
│   ├── fetch_bei_stocks.py        # Fetch daftar saham BEI
│   ├── ma_screener.py             # Logika MA Kuncup
│   └── save_results.py            # Simpan hasil ke CSV
└── .github/
    └── workflows/
        └── daily_screener.yml     # Workflow GitHub Actions
```