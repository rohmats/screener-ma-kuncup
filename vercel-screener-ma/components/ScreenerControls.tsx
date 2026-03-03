'use client';

import React, { useState, useEffect } from 'react';
import { ScreenerResult } from '@/lib/screener';

interface ScreenerControlsProps {
  onRun: (params: ScreenerControlsParams) => void;
  loading?: boolean;
  stocks?: string[];
}

export interface ScreenerControlsParams {
  tickers: string[];
  rangeTicks: number;
  volPct: number;
  minVolume: number;
}

export function ScreenerControls({ onRun, loading = false, stocks = [] }: ScreenerControlsProps) {
  const [rangeTicks, setRangeTicks] = useState(6);
  const [volPct, setVolPct] = useState(3.8);
  const [minVolume, setMinVolume] = useState(1_000_000);
  const [selectedStocks, setSelectedStocks] = useState<string[]>([]);
  const [useAllStocks, setUseAllStocks] = useState(true);

  const handleRun = () => {
    const tickers = useAllStocks ? stocks : selectedStocks;
    if (tickers.length === 0) {
      alert('Please select stocks or enable "Use All Stocks"');
      return;
    }
    onRun({ tickers, rangeTicks, volPct, minVolume });
  };

  const toggleStock = (ticker: string) => {
    setSelectedStocks(prev =>
      prev.includes(ticker) ? prev.filter(t => t !== ticker) : [...prev, ticker]
    );
  };

  const toggleAll = () => {
    if (selectedStocks.length === stocks.length) {
      setSelectedStocks([]);
    } else {
      setSelectedStocks([...stocks]);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Range Ticks Threshold</label>
          <input
            type="range"
            min="1"
            max="20"
            step="1"
            value={rangeTicks}
            onChange={e => setRangeTicks(Number(e.target.value))}
            className="w-full"
            disabled={loading}
          />
          <div className="text-sm text-gray-600">Current: {rangeTicks}</div>
        </div>

        <div>
          <label className="block text-sm font-semibold mb-2">Volatility Threshold (%)</label>
          <input
            type="range"
            min="0.5"
            max="10"
            step="0.1"
            value={volPct}
            onChange={e => setVolPct(Number(e.target.value))}
            className="w-full"
            disabled={loading}
          />
          <div className="text-sm text-gray-600">Current: {volPct.toFixed(1)}%</div>
        </div>

        <div>
          <label className="block text-sm font-semibold mb-2">Minimum Volume</label>
          <input
            type="number"
            value={minVolume}
            onChange={e => setMinVolume(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded"
            disabled={loading}
          />
          <div className="text-sm text-gray-600">
            Current: {(minVolume / 1_000_000).toFixed(1)}M
          </div>
        </div>

        <div className="space-y-2">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={useAllStocks}
              onChange={e => setUseAllStocks(e.target.checked)}
              disabled={loading}
              className="mr-2"
            />
            <span className="text-sm font-semibold">Use All Stocks</span>
          </label>
          {!useAllStocks && stocks.length > 0 && (
            <div className="border border-gray-300 rounded p-3 max-h-40 overflow-y-auto">
              <button
                onClick={toggleAll}
                className="text-xs text-blue-600 mb-2 font-semibold"
              >
                {selectedStocks.length === stocks.length ? 'Deselect All' : 'Select All'}
              </button>
              <div className="grid grid-cols-4 gap-2">
                {stocks.map(stock => (
                  <label key={stock} className="flex items-center text-xs cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedStocks.includes(stock)}
                      onChange={() => toggleStock(stock)}
                      disabled={loading}
                      className="mr-1"
                    />
                    {stock}
                  </label>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <button
        onClick={handleRun}
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded transition"
      >
        {loading ? 'Running...' : 'Run Screener'}
      </button>
    </div>
  );
}
