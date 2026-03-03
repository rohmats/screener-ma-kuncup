# Screener MA Kuncup - Vercel Edition

A modern Next.js application for detecting "MA Kuncup" (tight moving average) patterns in Indonesian stocks (BEI). Built with React, TypeScript, and TradingView Lightweight Charts.

## 📋 Features

- 📊 **Real-time Stock Screening** - Scan up to 100 stocks simultaneously
- 📈 **Interactive Charts** - TradingView Lightweight Charts with candlesticks, moving averages, and volume
- 🔍 **Detailed Analysis** - View technical indicators for individual stocks
- 📅 **History Tracking** - Track screening results over time
- ⚡ **Serverless** - Deployed on Vercel with automatic scaling
- 🚀 **Fast** - Optimized performance with Next.js

## 🎯 What is MA Kuncup?

MA Kuncup (Tight Moving Average) is a trading pattern where:
- Price and multiple moving averages converge within a narrow range
- Trading volume decreases (low volatility)
- This consolidation often precedes significant breakouts

**Screening Criteria:**
- Range between MAs < 6 ticks (based on BEI tick size)
- Rolling volatility (10-day) < 3.8%
- Volume > 1,000,000
- Price ≥ MA100 (100-day moving average)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/screener-ma-kuncup.git
   cd screener-ma-kuncup/vercel-screener-ma
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install pnpm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Environment Setup

Create a `.env.local` file (optional, all values have defaults):
```bash
cp .env.example .env.local
```

## 📦 Building for Production

```bash
npm run build
npm start
```

## 🌐 Deploy to Vercel

### Option 1: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/screener-ma-kuncup&project-name=screener-ma-kuncup)

### Option 2: Manual Deployment

1. **Sign up for Vercel** at [vercel.com](https://vercel.com)

2. **Create new project**
   ```bash
   npm install -g vercel
   vercel
   ```

3. **Follow the prompts** to connect your Git repository

4. **Vercel will auto-deploy** on every push to main branch

### Environment Variables (Vercel)

In Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add any custom variables from `.env.example`
3. Click "Save"

## 📖 Using the Application

### Dashboard

1. **Set Parameters** (left sidebar):
   - Range Ticks Threshold (1-20)
   - Volatility Threshold (0.5-10%)
   - Minimum Volume

2. **Run Screener**:
   - Click "Run Screener" button
   - Results display in the table
   - Green rows = Trading Signal detected

3. **View Details**:
   - Click on any stock ticker
   - View candlestick chart with moving averages
   - See detailed indicators
   - Adjust parameters in real-time

### Stock Detail Page

- **Interactive Chart** with price and all moving averages
- **Volume Chart** showing trading volume
- **Indicator Summary** cards
- **Parameter Controls** to adjust analysis
- **Moving Average Values** table

### History Page

- Track past screening results
- Navigate to stocks you've analyzed
- Local browser storage (cleared on cache clear)

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Next.js 14, TypeScript |
| **Charts** | [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) |
| **Styling** | Tailwind CSS |
| **Data** | Yahoo Finance API |
| **Deployment** | Vercel Edge Functions |

## 📚 Project Structure

```
vercel-screener-ma/
├── app/
│   ├── api/               # API routes
│   │   ├── screener/      # POST /api/screener
│   │   ├── stock/         # GET /api/stock/[ticker]
│   │   └── stocks/        # GET /api/stocks
│   ├── detail/            # Stock detail page
│   ├── history/           # Screening history
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── CandlestickChart.tsx
│   ├── VolumeChart.tsx
│   ├── ScreenerTable.tsx
│   ├── ScreenerControls.tsx
│   └── Navigation.tsx
├── lib/                   # Utility libraries
│   ├── config.ts          # Configuration
│   ├── data.ts            # Data fetching
│   ├── indicators.ts      # Technical indicators
│   ├── screener.ts        # Screener logic
│   ├── tickSize.ts        # BEI tick size rules
│   └── utils.ts           # Helper functions
└── public/                # Static assets
```

## 🔧 API Routes

### POST /api/screener
Run screener on multiple stocks.

**Request:**
```json
{
  "tickers": ["BBCA", "BBRI", "BMRI"],
  "rangeTicks": 6,
  "volPct": 3.8,
  "minVolume": 1000000
}
```

**Response:**
```json
{
  "results": [...],
  "total": 3,
  "timestamp": "2026-03-03T12:00:00Z"
}
```

### GET /api/stock/[ticker]
Get stock data with technical indicators.

**Parameters:**
- `ticker`: Stock symbol (e.g., BBCA)
- `rangeTicks`: Range ticks threshold (default: 6)
- `volPct`: Volatility threshold (default: 3.8)
- `minVolume`: Minimum volume (default: 1000000)

### GET /api/stocks
Get list of available BEI stocks.

## 📊 Indicators Calculated

- **Simple Moving Averages**: MA3, MA5, MA10, MA20, MA50, MA100
- **Range Ticks**: Difference between max and min price/MA in tick units
- **Volatility**: Rolling 10-day standard deviation (%)
- **MA Tight**: Boolean flag (Range_Ticks < threshold AND Vol_Pct < threshold)
- **Signal**: Boolean flag (MA_Tight AND Volume > MIN_VOLUME AND Price >= MA100)

## 🐛 Troubleshooting

### No data returned
- Ensure ticker is valid BEI stock (e.g., BBCA.JK)
- Check internet connection
- Verify Yahoo Finance API is accessible

### Charts not loading
- Check browser console for errors
- Ensure JavaScript is enabled
- Clear browser cache

### Slow performance
- Reduce number of stocks in screener
- Use shorter timeframes if available
- Check internet bandwidth

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Credits

- **Screener Logic**: Based on Pak T's techniques ([@TradingDiary2](https://x.com/TradingDiary2))
- **Summary & Optimization**: [@ikhwanuddin](https://x.com/ikhwanuddin)
- **Charts**: [TradingView](https://github.com/tradingview/lightweight-charts)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📧 Support

- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation above

## 🗺️ Roadmap

- [ ] Add more technical indicators
- [ ] Implement backtesting
- [ ] Add alerts/notifications
- [ ] Database for persistent history
- [ ] Mobile app
- [ ] Multi-language support

