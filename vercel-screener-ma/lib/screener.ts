// Core screener logic

import { fetchStockData } from './data';
import { calculateAllIndicators, getLatestIndicators, StockDataWithIndicators } from './indicators';

export interface ScreenerResult {
  ticker: string;
  close: number;
  MA3: number;
  MA5: number;
  MA10: number;
  MA20: number;
  MA50: number;
  MA100: number;
  Range_Ticks: number;
  Vol_Pct: number;
  Volume: number;
  MA_Tight: boolean;
  Signal: boolean;
  error?: string;
}

/**
 * Screen a single stock
 * @param ticker - Stock ticker symbol
 * @param rangeTicks - Range ticks threshold
 * @param volPct - Volatility percentage threshold
 * @param minVolume - Minimum volume threshold
 * @returns Screener result or null
 */
export async function screenSingleStock(
  ticker: string,
  rangeTicks: number = 6,
  volPct: number = 3.8,
  minVolume: number = 1_000_000
): Promise<ScreenerResult | null> {
  try {
    const data = await fetchStockData(ticker);
    
    if (data.length < 100) {
      return {
        ticker,
        close: 0,
        MA3: 0,
        MA5: 0,
        MA10: 0,
        MA20: 0,
        MA50: 0,
        MA100: 0,
        Range_Ticks: 0,
        Vol_Pct: 0,
        Volume: 0,
        MA_Tight: false,
        Signal: false,
        error: 'Insufficient data',
      };
    }

    const dataWithIndicators = calculateAllIndicators(data, rangeTicks, volPct, minVolume);
    const latest = getLatestIndicators(dataWithIndicators);

    if (!latest) return null;

    return {
      ticker,
      close: latest.close,
      MA3: latest.MA3 || 0,
      MA5: latest.MA5 || 0,
      MA10: latest.MA10 || 0,
      MA20: latest.MA20 || 0,
      MA50: latest.MA50 || 0,
      MA100: latest.MA100 || 0,
      Range_Ticks: latest.Range_Ticks || 0,
      Vol_Pct: latest.Vol_Pct || 0,
      Volume: latest.volume,
      MA_Tight: latest.MA_Tight || false,
      Signal: latest.Signal || false,
    };
  } catch (error) {
    console.error(`Error screening ${ticker}:`, error);
    return null;
  }
}

/**
 * Run screener on multiple stocks
 * @param tickers - Array of ticker symbols
 * @param rangeTicks - Range ticks threshold
 * @param volPct - Volatility percentage threshold
 * @param minVolume - Minimum volume threshold
 * @param maxConcurrent - Maximum concurrent requests
 * @returns Array of screener results
 */
export async function runScreener(
  tickers: string[],
  rangeTicks: number = 6,
  volPct: number = 3.8,
  minVolume: number = 1_000_000,
  maxConcurrent: number = 10
): Promise<ScreenerResult[]> {
  const results: ScreenerResult[] = [];
  
  // Process in batches to avoid overwhelming the API
  for (let i = 0; i < tickers.length; i += maxConcurrent) {
    const batch = tickers.slice(i, i + maxConcurrent);
    const batchResults = await Promise.all(
      batch.map(ticker => screenSingleStock(ticker, rangeTicks, volPct, minVolume))
    );
    
    results.push(...batchResults.filter((r): r is ScreenerResult => r !== null));
  }

  return results;
}
