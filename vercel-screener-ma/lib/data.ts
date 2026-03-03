// Data fetching utilities

import { YAHOO_FINANCE_BASE_URL, DATA_PERIOD } from './config';

export interface OHLCVData {
  date: Date;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

/**
 * Fetch stock data from Yahoo Finance
 * @param ticker - Stock ticker symbol
 * @param period - Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
 * @returns Array of OHLCV data
 */
export async function fetchStockData(
  ticker: string,
  period: string = DATA_PERIOD
): Promise<OHLCVData[]> {
  // Clean ticker
  const cleanTicker = ticker.trim().toUpperCase().replace(/[^A-Z0-9.]/g, '');
  if (!cleanTicker) return [];

  // Add .JK suffix for Indonesian stocks if not present
  const symbol = cleanTicker.endsWith('.JK') ? cleanTicker : `${cleanTicker}.JK`;

  try {
    const response = await fetch(
      `${YAHOO_FINANCE_BASE_URL}/${symbol}?range=${period}&interval=1d`,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0',
        },
      }
    );

    if (!response.ok) {
      console.error(`Failed to fetch ${symbol}: ${response.status}`);
      return [];
    }

    const data = await response.json();
    const result = data?.chart?.result?.[0];
    
    if (!result) return [];

    const timestamps = result.timestamp || [];
    const quote = result.indicators?.quote?.[0] || {};
    const adjclose = result.indicators?.adjclose?.[0]?.adjclose || quote.close;

    const ohlcvData: OHLCVData[] = [];

    for (let i = 0; i < timestamps.length; i++) {
      const close = adjclose[i] ?? quote.close[i];
      
      if (
        close != null &&
        quote.open[i] != null &&
        quote.high[i] != null &&
        quote.low[i] != null &&
        quote.volume[i] != null
      ) {
        ohlcvData.push({
          date: new Date(timestamps[i] * 1000),
          open: quote.open[i],
          high: quote.high[i],
          low: quote.low[i],
          close: close,
          volume: quote.volume[i],
        });
      }
    }

    return ohlcvData;
  } catch (error) {
    console.error(`Error fetching ${symbol}:`, error);
    return [];
  }
}

/**
 * Load stock list from a text/CSV string
 * @param content - CSV content with 'ticker' column
 * @returns Array of ticker symbols
 */
export function parseStockList(content: string): string[] {
  const lines = content.split('\n');
  const tickers: string[] = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line) {
      const ticker = line.split(',')[0].trim();
      if (ticker) {
        tickers.push(ticker);
      }
    }
  }

  return Array.from(new Set(tickers)); // Remove duplicates
}
