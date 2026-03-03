# Screener MA Kuncup - Complete Project

A comprehensive stock screener application for detecting MA Kuncup patterns in Indonesian stocks (BEI). This project includes:

1. **Python Backend** (`/` root directory) - Original Streamlit application and screener logic
2. **Vercel/Next.js Frontend** (`./vercel-screener-ma/`) - Modern web application for Vercel deployment

## 📁 Project Structure

```
screener-ma-kuncup/
├── screener/                      # Python package with core logic
│   ├── config.py                  # Configuration (thresholds)
│   ├── data.py                    # Data fetching (yfinance)
│   ├── indicators.py              # Technical indicators
│   ├── screener.py                # Core screener logic
│   ├── tick_size.py               # BEI tick size rules
│   └── ...
├── ui/                            # Streamlit UI (original)
│   └── pages/
├── tests/                         # Python tests
├── data/                          # Test data and results
├── app.py                         # Streamlit application
├── main.py                        # CLI entry point
├── requirements.txt               # Python dependencies
└── vercel-screener-ma/           # ✨ NEW: Next.js Vercel app
    ├── app/                       # Next.js app directory
    │   ├── api/                   # API routes (backend)
    │   ├── detail/[ticker]/       # Stock detail page
    │   ├── history/               # History page
    │   └── page.tsx               # Dashboard
    ├── components/                # React components
    │   ├── CandlestickChart.tsx   # TradingView chart
    │   ├── VolumeChart.tsx        # Volume chart
    │   ├── ScreenerTable.tsx      # Results table
    │   ├── ScreenerControls.tsx   # Parameter controls
    │   └── Navigation.tsx         # Navigation bar
    ├── lib/                       # TypeScript utilities
    │   ├── config.ts              # Config constants
    │   ├── data.ts                # Data fetching
    │   ├── indicators.ts          # Indicators calculation
    │   ├── screener.ts            # Screener logic
    │   ├── tickSize.ts            # Tick size calculation
    │   └── utils.ts               # Helper functions
    ├── package.json               # npm dependencies
    ├── tsconfig.json              # TypeScript config
    ├── next.config.js             # Next.js config
    ├── tailwind.config.ts         # Tailwind CSS config
    ├── postcss.config.js          # PostCSS config
    ├── README.md                  # Next.js app README
    ├── DEPLOYMENT.md              # Deployment guide
    ├── CONTRIBUTING.md            # Contributing guide
    ├── LICENSE                    # MIT License
    └── ...
```

## 🚀 Quick Start

### Python Application (Streamlit)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Or use CLI
python main.py --source bei --save
```

### Next.js Application (Vercel)

```bash
cd vercel-screener-ma

# Install dependencies
npm install

# Run development server
npm run dev
# → Open http://localhost:3000

# Build for production
npm run build
npm start
```

## 🌐 Deployment

### Vercel Deployment (Recommended)

The Next.js application is ready for Vercel deployment:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy to Vercel**
   ```bash
   cd vercel-screener-ma
   npm install -g vercel
   vercel --prod
   ```

3. **Or use Vercel Web Dashboard**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import Git repository
   - Set root directory: `vercel-screener-ma`
   - Click "Deploy"

See [vercel-screener-ma/DEPLOYMENT.md](vercel-screener-ma/DEPLOYMENT.md) for detailed instructions.

### Docker Deployment

```bash
cd vercel-screener-ma
docker build -t screener-ma-kuncup .
docker run -p 3000:3000 screener-ma-kuncup
```

## 📊 Features

### Python Backend
- Powerful screener logic using pandas and numpy
- Yahoo Finance API integration
- Indonesian stock exchange (BEI) tick size rules
- Streamlit UI with real-time results
- CLI interface for automation

### Next.js Frontend
- ✨ Modern React 18 + TypeScript
- 📊 TradingView Lightweight Charts for candlesticks
- 📱 Responsive design with Tailwind CSS
- 🚀 Serverless API routes on Vercel
- ⚡ Edge function support
- 📈 Real-time stock data from Yahoo Finance
- 🔍 Advanced filtering and parameter controls

## 🛠 Technology Stack

| Aspect | Python | Next.js |
|--------|--------|---------|
| **Framework** | Streamlit | Next.js 14 |
| **Language** | Python 3 | TypeScript |
| **Data** | yfinance, pandas | axios, fetch API |
| **Charts** | Plotly | TradingView Lightweight Charts |
| **Styling** | Streamlit CSS | Tailwind CSS |
| **Deployment** | Heroku/Self-hosted | Vercel |

## 📚 Documentation

### Python Application
- [main.py](main.py) - CLI interface documentation
- [screener/](screener/) - Core logic modules

### Next.js Application
- [vercel-screener-ma/README.md](vercel-screener-ma/README.md) - Full documentation
- [vercel-screener-ma/DEPLOYMENT.md](vercel-screener-ma/DEPLOYMENT.md) - Deployment guides
- [vercel-screener-ma/CONTRIBUTING.md](vercel-screener-ma/CONTRIBUTING.md) - Contributing guidelines

## 🎯 Screener Logic

**MA Kuncup Conditions:**
1. Range between MAs < 6 ticks (BEI tick size)
2. Volatility < 3.8% (rolling 10-day)
3. Volume > 1,000,000
4. Close price ≥ MA100

**Uses Moving Averages:** MA3, MA5, MA10, MA20, MA50, MA100

**BEI Tick Size Rules:**
- Price < 200: tick = 1
- Price < 500: tick = 2
- Price < 2000: tick = 5
- Price < 5000: tick = 10
- Price ≥ 5000: tick = 25

## 📊 Example Results

```
Ticker    Close   Range Ticks   Vol %   Volume    MA Tight   Signal
BBCA      8,850   4.2           2.1     5.2M      ✓          ✓
BBRI      4,620   5.8           3.1     8.1M      ✓          ✓
BMRI      8,100   6.5           3.9     2.4M      ✗          ✗
...
```

## 🤝 Contributing

Contributions are welcome! See:
- [vercel-screener-ma/CONTRIBUTING.md](vercel-screener-ma/CONTRIBUTING.md) for Next.js app
- Open issues and PRs on GitHub

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

**Screener Methodology:**
- **Pak T** ([@TradingDiary2](https://x.com/TradingDiary2)) - Original technique
- **Ikhwanuddin** ([@ikhwanuddin](https://x.com/ikhwanuddin)) - Summary and optimization

**Technologies:**
- [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts)
- [Next.js](https://nextjs.org/)
- [Vercel](https://vercel.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Streamlit](https://streamlit.io/)

## 📞 Support

- **Documentation**: Read README files in each directory
- **Deployment Help**: See [DEPLOYMENT.md](vercel-screener-ma/DEPLOYMENT.md)
- **Issues**: Open GitHub issues for bugs and features
- **Discussions**: Start a discussion for questions

## 🗺️ Roadmap

- [ ] WebSocket real-time updates
- [ ] Database for persistent history
- [ ] Advanced technical indicators
- [ ] Backtesting engine
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Email/SMS alerts
- [ ] Portfolio tracking
