'use client';

import React, { useState, useEffect } from 'react';
import { ScreenerControls, ScreenerControlsParams } from '@/components/ScreenerControls';
import { ScreenerTable } from '@/components/ScreenerTable';
import { CandlestickChart } from '@/components/CandlestickChart';
import { VolumeChart } from '@/components/VolumeChart';
import { ScreenerResult } from '@/lib/screener';
import { StockDataWithIndicators } from '@/lib/indicators';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'detail' | 'history'>('dashboard');
  const [results, setResults] = useState<ScreenerResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [stocks, setStocks] = useState<string[]>([]);
  const [lastRun, setLastRun] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Stock detail state
  const [selectedTicker, setSelectedTicker] = useState<string>('BBCA');
  const [stockData, setStockData] = useState<StockDataWithIndicators[]>([]);
  const [stockLoading, setStockLoading] = useState(false);
  const [rangeTicks, setRangeTicks] = useState(6);
  const [volPct, setVolPct] = useState(3.8);
  
  // History state
  const [history, setHistory] = useState<any[]>([]);

  // Load available stocks on mount
  useEffect(() => {
    const loadStocks = async () => {
      try {
        const response = await fetch('/api/stocks');
        const data = await response.json();
        setStocks(data.stocks || []);
      } catch (err) {
        console.error('Failed to load stocks:', err);
      }
    };
    loadStocks();
    
    // Load history from localStorage
    const stored = localStorage.getItem('screener_history');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setHistory(parsed.slice(-100));
      } catch {
        // Ignore parse errors
      }
    }
  }, []);

  // Load stock data when ticker changes
  useEffect(() => {
    if (activeTab === 'detail' && selectedTicker) {
      loadStockData();
    }
  }, [selectedTicker, rangeTicks, volPct, activeTab]);

  const loadStockData = async () => {
    setStockLoading(true);
    try {
      const response = await fetch(
        `/api/stock/${selectedTicker}?rangeTicks=${rangeTicks}&volPct=${volPct}`
      );
      if (response.ok) {
        const result = await response.json();
        setStockData(result.data || []);
      }
    } catch (err) {
      console.error('Failed to load stock data:', err);
    } finally {
      setStockLoading(false);
    }
  };

  const handleRun = async (params: ScreenerControlsParams) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/screener', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tickers: params.tickers,
          rangeTicks: params.rangeTicks,
          volPct: params.volPct,
          minVolume: params.minVolume,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to run screener');
      }

      const data = await response.json();
      setResults(data.results || []);
      setLastRun(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectStock = (ticker: string) => {
    setSelectedTicker(ticker);
    setActiveTab('detail');
  };

  const latest = stockData.length > 0 ? stockData[stockData.length - 1] : null;

  return (
    <div className="space-y-6">
      {/* Info Card */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>MA Kuncup (Tight MA)</strong> adalah pola yang menunjukkan saat-saat di mana harga dan berbagai moving averages (MA) berkumpul dalam rentang yang sangat sempit, dengan volatilitas rendah. Kondisi ini sering dianggap sebagai fase konsolidasi sebelum breakout.
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'dashboard'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🏠 Dashboard
          </button>
          <button
            onClick={() => setActiveTab('detail')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'detail'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📈 Detail Saham
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'history'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📅 Riwayat
          </button>
        </nav>
      </div>

      {/* Tab Content: Dashboard */}
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1">
              <ScreenerControls
                onRun={handleRun}
                loading={loading}
                stocks={stocks}
              />
            </div>

            <div className="lg:col-span-3">
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <p className="text-red-900 text-sm">{error}</p>
                </div>
              )}

              {lastRun && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <p className="text-green-900 text-sm">
                    Last run: {lastRun.toLocaleString('id-ID')}
                  </p>
                </div>
              )}

              <div className="bg-white rounded-lg shadow-md p-6">
                <ScreenerTable
                  results={results}
                  loading={loading}
                  onSelectStock={handleSelectStock}
                />
              </div>
            </div>
          </div>

          {results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg shadow-md p-4">
                <div className="text-3xl font-bold text-blue-600">{results.length}</div>
                <div className="text-sm text-gray-600">Total Stocks Screened</div>
              </div>
              <div className="bg-white rounded-lg shadow-md p-4">
                <div className="text-3xl font-bold text-green-600">
                  {results.filter(r => r.MA_Tight).length}
                </div>
                <div className="text-sm text-gray-600">MA Tight Conditions</div>
              </div>
              <div className="bg-white rounded-lg shadow-md p-4">
                <div className="text-3xl font-bold text-emerald-600">
                  {results.filter(r => r.Signal).length}
                </div>
                <div className="text-sm text-gray-600">Trading Signals</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: Detail Saham */}
      {activeTab === 'detail' && (
        <div className="space-y-6">
          {/* Ticker Input */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Pilih Saham</h3>
            <div className="flex items-center gap-4">
              <select
                value={selectedTicker}
                onChange={(e) => setSelectedTicker(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {stocks.map(stock => (
                  <option key={stock} value={stock}>{stock}</option>
                ))}
              </select>
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

          {stockLoading ? (
            <div className="text-center py-8">
              <p className="text-gray-600">Loading {selectedTicker} data...</p>
            </div>
          ) : stockData.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-600">No data available for {selectedTicker}</p>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="flex items-baseline justify-between">
                <h1 className="text-4xl font-bold text-gray-800">{selectedTicker}</h1>
                {latest && (
                  <div className="text-3xl font-bold text-blue-600">
                    IDR {latest.close.toFixed(0)}
                  </div>
                )}
              </div>

              {/* Indicators Summary */}
              {latest && (
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
              )}

              {/* Moving Averages Table */}
              {latest && (
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
              )}

              {/* Charts */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <CandlestickChart data={stockData} title="Price & Moving Averages" height={500} />
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <VolumeChart data={stockData} title="Trading Volume" height={300} />
              </div>
            </>
          )}
        </div>
      )}

      {/* Tab Content: History */}
      {activeTab === 'history' && (
        <div className="space-y-6">
          {history.length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <p className="text-gray-600">
                Belum ada riwayat. Jalankan screener untuk mulai melacak hasil.
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-gray-300 bg-gray-50">
                    <th className="text-left p-4 font-semibold">Tanggal</th>
                    <th className="text-left p-4 font-semibold">Ticker</th>
                    <th className="text-right p-4 font-semibold">Harga Close</th>
                    <th className="text-center p-4 font-semibold">Signal</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((entry, idx) => (
                    <tr
                      key={idx}
                      className={`border-b border-gray-200 hover:bg-gray-50 cursor-pointer ${
                        entry.signal ? 'bg-green-50' : ''
                      }`}
                      onClick={() => {
                        setSelectedTicker(entry.ticker);
                        setActiveTab('detail');
                      }}
                    >
                      <td className="p-4 text-sm text-gray-600">
                        {new Date(entry.date).toLocaleString('id-ID')}
                      </td>
                      <td className="p-4 font-semibold text-blue-600">
                        {entry.ticker}
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
              Riwayat disimpan secara lokal di browser Anda dan akan dihapus saat Anda membersihkan cache.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
