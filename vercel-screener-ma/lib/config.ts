// Configuration constants for the MA Kuncup screener

export const RANGE_TICKS_THRESHOLD = 6;
export const VOL_PCT_THRESHOLD = 3.8;
export const MIN_VOLUME = 1_000_000;
export const MA_PERIODS = [3, 5, 10, 20, 50];
export const MA_TREND_PERIOD = 100;
export const VOL_ROLLING_PERIOD = 10;
export const DATA_PERIOD = '1y';

// Yahoo Finance API configuration
export const YAHOO_FINANCE_BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart';
