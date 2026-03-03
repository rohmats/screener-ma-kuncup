// API Route: Get stock data with indicators
// GET /api/stock/[ticker]

import { NextRequest, NextResponse } from 'next/server';
import { fetchStockData } from '@/lib/data';
import { calculateAllIndicators } from '@/lib/indicators';

export const runtime = 'edge';

interface RouteParams {
  params: {
    ticker: string;
  };
}

export async function GET(
  request: NextRequest,
  { params }: RouteParams
) {
  try {
    const { ticker } = params;
    const { searchParams } = new URL(request.url);
    
    const rangeTicks = parseFloat(searchParams.get('rangeTicks') || '6');
    const volPct = parseFloat(searchParams.get('volPct') || '3.8');
    const minVolume = parseInt(searchParams.get('minVolume') || '1000000');

    if (!ticker) {
      return NextResponse.json(
        { error: 'Ticker is required' },
        { status: 400 }
      );
    }

    const data = await fetchStockData(ticker);

    if (data.length === 0) {
      return NextResponse.json(
        { error: 'No data found for ticker' },
        { status: 404 }
      );
    }

    const dataWithIndicators = calculateAllIndicators(data, rangeTicks, volPct, minVolume);

    return NextResponse.json({
      ticker,
      data: dataWithIndicators,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Stock API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
