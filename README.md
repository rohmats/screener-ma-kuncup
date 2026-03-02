# Screener MA Kuncup

Screener saham otomatis untuk mendeteksi pola **MA Kuncup / MA Ketat** di Bursa Efek Indonesia (BEI).

Berdasarkan artikel [@ikhwanuddin](https://x.com/ikhwanuddin/status/2028329791657541637) yang merujuk teknik **Pak T [@TradingDiary2](https://x.com/TradingDiary2)**.

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

```
MA_n(t) = (1/n) × Σ(i=0 to n-1) C(t-i)
```

### Tick Size BEI

| Harga (Rp)       | Fraksi Harga (Tick) |
|------------------|---------------------|
| ≤ 200            | 1                   |
| 201 – 500        | 2                   |
| 501 – 2.000      | 5                   |
| 2.001 – 5.000    | 10                  |
| > 5.000          | 25                  |

### Rentang MA dalam Tick

```
MA_max(t) = max(C, MA3, MA5, MA10, MA20, MA50)
MA_min(t) = min(C, MA3, MA5, MA10, MA20, MA50)
range_ticks(t) = (MA_max - MA_min) / tick_size(C)
```

### Volatilitas (Rolling 10 Hari)

```
vol_pct(t) = std_dev((C(t) - C(t-1)) / C(t-1), rolling 10 hari) × 100%
```

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

## Instalasi & Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/rohmats/screener-ma-kuncup.git
cd screener-ma-kuncup
```

### 2. Install dependensi

```bash
pip install -r requirements.txt
```

### 3. Jalankan screener

```bash
python main.py
```

Screener akan membaca daftar saham dari `stocks.csv`, mengambil data historis dari Yahoo Finance, menghitung semua indikator, lalu menampilkan tabel hasil beserta saham-saham yang memenuhi sinyal MA Kuncup.

---

## Struktur Project

```
screener-ma-kuncup/
├── README.md
├── requirements.txt
├── screener/
│   ├── __init__.py
│   ├── config.py        # Parameter & threshold yang bisa di-tuning
│   ├── tick_size.py     # Aturan fraksi harga BEI
│   ├── indicators.py    # Perhitungan MA, range_ticks, volatilitas
│   ├── screener.py      # Logika deteksi sinyal
│   └── data.py          # Pengambilan data dari yfinance
├── stocks.csv           # Daftar saham BEI yang di-screen
├── main.py              # Entry point
└── tests/
    ├── __init__.py
    ├── test_tick_size.py
    ├── test_indicators.py
    └── test_screener.py
```

---

## Parameter yang Bisa Di-tuning (`screener/config.py`)

| Parameter              | Default | Keterangan                                    |
|------------------------|---------|-----------------------------------------------|
| `RANGE_TICKS_THRESHOLD`| `6`     | Batas maksimum rentang MA dalam tick          |
| `VOL_PCT_THRESHOLD`    | `3.8`   | Batas maksimum volatilitas harian (%)         |
| `MIN_VOLUME`           | `1e6`   | Volume minimum untuk sinyal valid             |
| `MA_PERIODS`           | `[3,5,10,20,50]` | Periode MA yang digunakan           |
| `MA_TREND_PERIOD`      | `100`   | Periode MA tren (MA100)                       |
| `VOL_ROLLING_PERIOD`   | `10`    | Periode rolling untuk kalkulasi volatilitas   |
| `DATA_PERIOD`          | `"1y"`  | Periode historis data yang diambil            |

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
