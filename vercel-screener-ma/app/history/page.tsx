'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface HistoryEntry {
  date: string;
  ticker: string;
  close: number;
  signal: boolean;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real application, you'd fetch historical data from localStorage or a database
    const stored = localStorage.getItem('screener_history');
    if (stored) {
      try {
        const parsed = JSON.parse(stored) as HistoryEntry[];
        setHistory(parsed.slice(-100)); // Last 100 entries
      } catch {
        // Ignore parse errors
      }
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="text-4xl mb-4">📅</div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <Link href="/" className="text-blue-600 hover:underline text-sm mb-4 inline-block">
          ← Back to Dashboard
        </Link>
        <h1 className="text-4xl font-bold text-gray-800">Screening History</h1>
      </div>

      {history.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-gray-600">No history available yet. Run the screener to start tracking results.</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b-2 border-gray-300 bg-gray-50">
                <th className="text-left p-4 font-semibold">Date</th>
                <th className="text-left p-4 font-semibold">Ticker</th>
                <th className="text-right p-4 font-semibold">Close Price</th>
                <th className="text-center p-4 font-semibold">Signal</th>
              </tr>
            </thead>
            <tbody>
              {history.map((entry, idx) => (
                <tr
                  key={idx}
                  className={`border-b border-gray-200 hover:bg-gray-50 ${
                    entry.signal ? 'bg-green-50' : ''
                  }`}
                >
                  <td className="p-4 text-sm text-gray-600">
                    {new Date(entry.date).toLocaleString('id-ID')}
                  </td>
                  <td className="p-4 font-semibold text-blue-600">
                    <Link href={`/detail/${entry.ticker}`} className="hover:underline">
                      {entry.ticker}
                    </Link>
                  </td>
                  <td className="p-4 text-right text-gray-800">
                    IDR {entry.close.toFixed(0)}
                  </td>
                  <td className="p-4 text-center">
                    <span className={entry.signal ? 'text-green-600 font-bold' : 'text-gray-400'}>
                      {entry.signal ? '✓' : '✗'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          History is stored locally in your browser and cleared when you clear your cache.
          For persistent history, run screeners from this application and results will be saved automatically.
        </p>
      </div>
    </div>
  );
}
