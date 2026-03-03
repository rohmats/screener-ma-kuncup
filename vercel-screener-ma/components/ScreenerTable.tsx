'use client';

import React from 'react';
import { ScreenerResult } from '@/lib/screener';

interface ScreenerTableProps {
  results: ScreenerResult[];
  loading?: boolean;
  onSelectStock?: (ticker: string) => void;
}

export function ScreenerTable({ results, loading = false, onSelectStock }: ScreenerTableProps) {
  if (loading) {
    return (
      <div className="overflow-x-auto">
        <div className="text-center py-8">Loading results...</div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="overflow-x-auto">
        <div className="text-center py-8 text-gray-500">No results found</div>
      </div>
    );
  }

  const signalResults = results.filter(r => r.Signal);

  return (
    <div className="overflow-x-auto">
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          Found {signalResults.length} signal(s) out of {results.length} stocks
        </p>
      </div>

      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="border-b-2 border-gray-300">
            <th className="text-left p-2 font-semibold">Ticker</th>
            <th className="text-right p-2 font-semibold">Close</th>
            <th className="text-right p-2 font-semibold">MA3</th>
            <th className="text-right p-2 font-semibold">MA5</th>
            <th className="text-right p-2 font-semibold">MA10</th>
            <th className="text-right p-2 font-semibold">MA20</th>
            <th className="text-right p-2 font-semibold">MA50</th>
            <th className="text-right p-2 font-semibold">MA100</th>
            <th className="text-right p-2 font-semibold">Range Ticks</th>
            <th className="text-right p-2 font-semibold">Vol %</th>
            <th className="text-right p-2 font-semibold">Volume</th>
            <th className="text-center p-2 font-semibold">MA Tight</th>
            <th className="text-center p-2 font-semibold">Signal</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, idx) => (
            <tr
              key={idx}
              className={`border-b border-gray-200 hover:bg-gray-50 cursor-pointer ${
                result.Signal ? 'bg-green-50' : ''
              }`}
              onClick={() => onSelectStock?.(result.ticker)}
            >
              <td className="p-2 font-semibold text-blue-600">{result.ticker}</td>
              <td className="text-right p-2">{result.close.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA3.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA5.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA10.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA20.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA50.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{result.MA100.toFixed(2)}</td>
              <td className="text-right p-2">{result.Range_Ticks.toFixed(2)}</td>
              <td className="text-right p-2">{result.Vol_Pct.toFixed(2)}</td>
              <td className="text-right p-2 text-xs">{(result.Volume / 1_000_000).toFixed(1)}M</td>
              <td className="text-center p-2">
                <span className={result.MA_Tight ? 'text-green-600 font-semibold' : 'text-gray-400'}>
                  {result.MA_Tight ? '✓' : '✗'}
                </span>
              </td>
              <td className="text-center p-2">
                <span className={result.Signal ? 'text-green-600 font-bold text-lg' : 'text-gray-400'}>
                  {result.Signal ? '✓' : '✗'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
