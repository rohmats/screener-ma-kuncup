// API Route: Run screener on multiple stocks
// POST /api/screener

import { NextRequest, NextResponse } from 'next/server';
import { runScreener } from '@/lib/screener';

export const runtime = 'edge';
export const maxDuration = 60;

interface ScreenerRequest {
  tickers: string[];
  rangeTicks?: number;
  volPct?: number;
  minVolume?: number;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json() as ScreenerRequest;
    const { tickers, rangeTicks = 6, volPct = 3.8, minVolume = 1_000_000 } = body;

    if (!tickers || !Array.isArray(tickers) || tickers.length === 0) {
      return NextResponse.json(
        { error: 'Invalid or empty tickers array' },
        { status: 400 }
      );
    }

    // Limit to 100 stocks per request to avoid timeouts
    const limitedTickers = tickers.slice(0, 100);

    const results = await runScreener(limitedTickers, rangeTicks, volPct, minVolume);

    return NextResponse.json({
      results,
      total: results.length,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Screener API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
