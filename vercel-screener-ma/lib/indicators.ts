// Technical indicators for the MA Kuncup screener

import { tickSizeArray } from './tickSize';
import { MA_PERIODS, VOL_ROLLING_PERIOD, MA_TREND_PERIOD } from './config';
import { OHLCVData } from './data';

export interface StockDataWithIndicators extends OHLCVData {
  MA3?: number;
  MA5?: number;
  MA10?: number;
  MA20?: number;
  MA50?: number;
  MA100?: number;
  MA_max?: number;
  MA_min?: number;
  Range_Ticks?: number;
  Vol_Pct?: number;
  MA_Tight?: boolean;
  Signal?: boolean;
}

/**
 * Calculate Simple Moving Average
 * @param values - Array of values
 * @param period - Moving average period
 * @returns Array of SMA values (NaN for insufficient data)
 */
function sma(values: number[], period: number): number[] {
  const result: number[] = [];
  
  for (let i = 0; i < values.length; i++) {
    if (i < period - 1) {
      result.push(NaN);
    } else {
      let sum = 0;
      for (let j = 0; j < period; j++) {
        sum += values[i - j];
      }
      result.push(sum / period);
    }
  }
  
  return result;
}

/**
 * Calculate standard deviation
 * @param values - Array of values
 * @returns Standard deviation
 */
function stdDev(values: number[]): number {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
  return Math.sqrt(variance);
}

/**
 * Calculate rolling standard deviation
 * @param values - Array of values
 * @param period - Rolling period
 * @returns Array of rolling std dev values
 */
function rollingStdDev(values: number[], period: number): number[] {
  const result: number[] = [];
  
  for (let i = 0; i < values.length; i++) {
    if (i < period) {
      result.push(NaN);
    } else {
      const slice = values.slice(i - period + 1, i + 1);
      result.push(stdDev(slice));
    }
  }
  
  return result;
}

/**
 * Calculate all technical indicators
 * @param data - Array of OHLCV data
 * @param rangeTicks - Range ticks threshold
 * @param volPct - Volatility percentage threshold
 * @param minVolume - Minimum volume threshold
 * @returns Array of data with indicators
 */
export function calculateAllIndicators(
  data: OHLCVData[],
  rangeTicks: number = 6,
  volPct: number = 3.8,
  minVolume: number = 1_000_000
): StockDataWithIndicators[] {
  if (data.length < 100) return data as StockDataWithIndicators[];

  const closes = data.map(d => d.close);
  
  // Calculate all moving averages
  const allPeriods = [...MA_PERIODS, MA_TREND_PERIOD];
  const maValues: { [key: string]: number[] } = {};
  
  for (const period of allPeriods) {
    maValues[`MA${period}`] = sma(closes, period);
  }

  // Calculate daily returns
  const returns: number[] = [NaN];
  for (let i = 1; i < closes.length; i++) {
    returns.push((closes[i] - closes[i - 1]) / closes[i - 1]);
  }

  // Calculate rolling volatility (in percentage)
  const volatility = rollingStdDev(returns, VOL_ROLLING_PERIOD).map(v => v * 100);

  // Calculate tick sizes
  const tickSizes = tickSizeArray(closes);

  // Build result with all indicators
  const result: StockDataWithIndicators[] = data.map((row, i) => {
    const maColumns = MA_PERIODS.map(p => maValues[`MA${p}`][i]);
    const priceAndMAs = [closes[i], ...maColumns];
    
    const validValues = priceAndMAs.filter(v => !isNaN(v));
    const MA_max = validValues.length > 0 ? Math.max(...validValues) : NaN;
    const MA_min = validValues.length > 0 ? Math.min(...validValues) : NaN;
    
    const Range_Ticks = !isNaN(MA_max) && !isNaN(MA_min) 
      ? (MA_max - MA_min) / tickSizes[i]
      : NaN;

    const MA_Tight = !isNaN(Range_Ticks) && !isNaN(volatility[i])
      ? Range_Ticks < rangeTicks && volatility[i] < volPct
      : false;

    const MA100 = maValues[`MA${MA_TREND_PERIOD}`][i];
    const Signal = MA_Tight && 
      row.volume > minVolume && 
      !isNaN(MA100) && 
      MA100 <= closes[i];

    return {
      ...row,
      MA3: maValues['MA3'][i],
      MA5: maValues['MA5'][i],
      MA10: maValues['MA10'][i],
      MA20: maValues['MA20'][i],
      MA50: maValues['MA50'][i],
      MA100: MA100,
      MA_max,
      MA_min,
      Range_Ticks,
      Vol_Pct: volatility[i],
      MA_Tight,
      Signal,
    };
  });

  return result;
}

/**
 * Get the latest row from data with indicators
 * @param data - Array of data with indicators
 * @returns Latest row or null
 */
export function getLatestIndicators(
  data: StockDataWithIndicators[]
): StockDataWithIndicators | null {
  if (data.length === 0) return null;
  return data[data.length - 1];
}
