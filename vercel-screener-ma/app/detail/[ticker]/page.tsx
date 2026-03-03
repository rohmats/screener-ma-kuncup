'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { CandlestickChart } from '@/components/CandlestickChart';
import { VolumeChart } from '@/components/VolumeChart';
import { StockDataWithIndicators } from '@/lib/indicators';

interface StockDetailPageProps {
  params: {
    ticker: string;
  };
}

export default function StockDetailPage({ params }: StockDetailPageProps) {
  const { ticker } = params;
  const [data, setData] = useState<StockDataWithIndicators[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [rangeTicks, setRangeTicks] = useState(6);
  const [volPct, setVolPct] = useState(3.8);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `/api/stock/${ticker}?rangeTicks=${rangeTicks}&volPct=${volPct}`
        );
        if (!response.ok) {
          throw new Error('Failed to load stock data');
        }
        const result = await response.json();
        setData(result.data || []);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [ticker, rangeTicks, volPct]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="text-4xl mb-4">📈</div>
          <p className="text-gray-600">Loading {ticker} data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Link href="/" className="text-blue-600 hover:underline">
          ← Back to Dashboard
        </Link>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-900">{error}</p>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="space-y-4">
        <Link href="/" className="text-blue-600 hover:underline">
          ← Back to Dashboard
        </Link>
        <div className="text-center py-8">
          <p className="text-gray-600">No data available for {ticker}</p>
        </div>
      </div>
    );
  }

  const latest = data[data.length - 1];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Link href="/" className="text-blue-600 hover:underline text-sm mb-4 inline-block">
          ← Back to Dashboard
        </Link>
        <div className="flex items-baseline justify-between">
          <h1 className="text-4xl font-bold text-gray-800">{ticker}</h1>
          <div className="text-3xl font-bold text-blue-600">
            IDR {latest.close.toFixed(0)}
          </div>
        </div>
      </div>

      {/* Parameters */}
      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <h3 className="text-lg font-semibold">Parameters</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold mb-2">
              Range Ticks Threshold: {rangeTicks}
            </label>
            <input
              type="range"
              min="1"
              max="20"
              step="1"
              value={rangeTicks}
              onChange={e => setRangeTicks(Number(e.target.value))}
              className="w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold mb-2">
              Volatility Threshold (%): {volPct.toFixed(1)}
            </label>
            <input
              type="range"
              min="0.5"
              max="10"
              step="0.1"
              value={volPct}
              onChange={e => setVolPct(Number(e.target.value))}
              className="w-full"
            />
          </div>
        </div>
      </div>

      {/* Indicators Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-gray-800">
            {latest.MA_Tight ? '✓' : '✗'}
          </div>
          <div className="text-sm text-gray-600">MA Tight</div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-gray-800">
            {latest.Range_Ticks?.toFixed(2) || '-'}
          </div>
          <div className="text-sm text-gray-600">Range Ticks</div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-gray-800">
            {latest.Vol_Pct?.toFixed(2) || '-'}%
          </div>
          <div className="text-sm text-gray-600">Volatility</div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-gray-800">
            {latest.Signal ? '✓' : '✗'}
          </div>
          <div className="text-sm text-gray-600">Trading Signal</div>
        </div>
      </div>

      {/* Moving Averages Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Moving Averages</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[3, 5, 10, 20, 50, 100].map(period => (
            <div key={period} className="border border-gray-200 rounded p-3">
              <div className="text-xs text-gray-600">MA{period}</div>
              <div className="text-lg font-semibold">
                {latest[`MA${period}` as keyof StockDataWithIndicators]
                  ? (latest[`MA${period}` as keyof StockDataWithIndicators] as number).toFixed(2)
                  : '-'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Charts */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <CandlestickChart data={data} title="Price & Moving Averages" height={500} />
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <VolumeChart data={data} title="Trading Volume" height={300} />
      </div>
    </div>
  );
}
