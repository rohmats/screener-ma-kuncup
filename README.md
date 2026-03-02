# Screener MA Kuncup

Screener saham otomatis untuk mendeteksi pola **MA Kuncup / MA Ketat** di Bursa Efek Indonesia (BEI).

Berdasarkan artikel **[@ikhwanuddin](https://x.com/ikhwanuddin/status/2028329791657541637)** yang merujuk teknik **Pak T [@TradingDiary2](https://x.com/TradingDiary2)**.

---

## Tentang Pola MA Kuncup / MA Ketat

Pola MA Kuncup (atau MA Ketat) terjadi ketika beberapa *Moving Average* dengan periode berbeda saling berdekatan atau menyatu (*menguncup*). Kondisi ini mengindikasikan konsolidasi harga dengan volatilitas rendah — seringkali menjadi tanda awal sebelum pergerakan harga yang signifikan.

Artikel referensi: [Singkap Rahasia Pola MA Ketat — Chart Visual Jadi Pertidaksamaan Matematis](https://x.com/ikhwanuddin/status/2028329791657541637)

---

## Kriteria Matematis

### Moving Average yang Digunakan

- **MA3**, **MA5**, **MA10**, **MA20**, **MA50** — MA jangka pendek & menengah
- **Close (C)** — harga penutupan hari ini
- **MA100** — MA tren jangka panjang (filter sinyal)

### Tick Size BEI

| Harga (Rp)       | Fraksi Harga (Tick) |
|------------------|---------------------|
| ≤ 200            | 1                   |
| 201 – 500        | 2                   |
| 501 – 2.000      | 5                   |
| 2.001 – 5.000    | 10                  |
| > 5.000          | 25                  |

### Kondisi MA Menguncup (`ma_tight`)

```
ma_tight = True jika:
    range_ticks < 6
    DAN vol_pct < 3.8%
```

### Sinyal Final Siap Entry

```
signal = True jika:
    ma_tight = True
    DAN Volume > 1.000.000
    DAN MA100 ≤ Close
```

---

## UI Dashboard

Screener ini dilengkapi dengan antarmuka web berbasis **Streamlit** yang interaktif.

### Cara Menjalankan UI

```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan UI
streamlit run app.py
```

UI akan terbuka di browser pada `http://localhost:8501`.

### Fitur Dashboard

| Halaman        | Fitur                                                                 |
|----------------|-----------------------------------------------------------------------|
| 🏠 Dashboard   | Parameter tuning, jalankan screener, tabel hasil, download CSV        |
| 📈 Detail Saham | Chart harga + MA interaktif (Plotly), tabel indikator per saham      |
| 📅 Riwayat     | Hasil scan historis, tren sinyal antar tanggal                        |

### Parameter yang Bisa Di-tuning (Sidebar)

| Parameter              | Default    | Range         |
|------------------------|------------|---------------|
| Range Ticks Threshold  | 6          | 1 – 20        |
| Volatilitas Threshold  | 3.8%       | 0.5% – 10%    |
| Volume Minimum         | 1.000.000  | 0 – 10.000.000|

---

## Instalasi & Cara Menjalankan (CLI)

### 1. Clone repository

```bash
git clone https://github.com/rohmats/screener-ma-kuncup.git
cd screener-ma-kuncup
```

### 2. Install dependensi

```bash
pip install -r requirements.txt
```

### 3. Jalankan screener (CLI)

```bash
python main.py
```

### 4. Jalankan UI

```bash
streamlit run app.py
```

---

## Docker

```bash
docker build -t screener-ma-kuncup .
docker run -p 8501:8501 screener-ma-kuncup
```

---

## Struktur Project

```
screener-ma-kuncup/
├── app.py                      # Entry point Streamlit UI
├── main.py                     # Entry point CLI
├── requirements.txt
├── stocks.csv                  # Daftar saham populer BEI
├── Dockerfile
├── .streamlit/
│   └── config.toml             # Konfigurasi tema Streamlit
├── screener/
│   ├── __init__.py
│   ├── config.py               # Parameter & threshold
│   ├── tick_size.py            # Aturan fraksi harga BEI
│   ├── indicators.py           # MA, range_ticks, volatilitas
│   ├── screener.py             # Logika deteksi sinyal
│   └── data.py                 # Pengambilan data dari yfinance
├── ui/
│   ├── __init__.py
│   ├── components.py           # Komponen UI reusable
│   ├── styles.py               # Custom CSS
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py        # Halaman utama
│       ├── stock_detail.py     # Detail per saham
│       └── history.py          # Riwayat hasil
├── data/
│   └── results/                # Hasil scan harian (dari GitHub Actions)
└── tests/
    ├── __init__.py
    ├── test_tick_size.py
    ├── test_indicators.py
    └── test_screener.py
```

---

## Menjalankan Tests

```bash
python -m pytest tests/
```

---

## Kredit

- **[@ikhwanuddin](https://x.com/ikhwanuddin)** — Artikel *"Singkap Rahasia Pola MA Ketat — Chart Visual Jadi Pertidaksamaan Matematis"*
- **Pak T [@TradingDiary2](https://x.com/TradingDiary2)** — Teknik MA Kuncup / MA Ketat

---

## Disclaimer

Screener ini dibuat untuk tujuan edukasi dan riset. **Bukan merupakan rekomendasi investasi.** Keputusan beli/jual saham sepenuhnya menjadi tanggung jawab masing-masing investor. Selalu lakukan riset mandiri (*due diligence*) sebelum mengambil keputusan investasi.