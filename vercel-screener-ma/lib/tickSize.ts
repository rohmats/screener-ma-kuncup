// BEI tick size rules for Indonesian stocks

/**
 * Calculate tick size based on BEI (Indonesia Stock Exchange) rules
 * @param price - Stock price
 * @returns Tick size in IDR
 */
export function tickSize(price: number): number {
  if (price < 200) return 1;
  if (price < 500) return 2;
  if (price < 2000) return 5;
  if (price < 5000) return 10;
  return 25;
}

/**
 * Calculate tick size for an array of prices
 * @param prices - Array of stock prices
 * @returns Array of tick sizes
 */
export function tickSizeArray(prices: number[]): number[] {
  return prices.map(tickSize);
}
