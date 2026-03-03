'use client';

import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import { StockDataWithIndicators } from '@/lib/indicators';

interface ChartData {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

interface CandlestickChartProps {
  data: StockDataWithIndicators[];
  title?: string;
  height?: number;
}

export function CandlestickChart({ data, title = 'Price Chart', height = 400 }: CandlestickChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<any>(null);

  useEffect(() => {
    if (!containerRef.current || data.length === 0) return;

    // Create chart
    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#ffffff' },
        textColor: '#000000',
      },
      width: containerRef.current.clientWidth,
      height: height,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    chartRef.current = chart;

    // Prepare candlestick data with validation
    const candleData: ChartData[] = data
      .filter(d => d.open && d.high && d.low && d.close)
      .map(d => ({
        time: new Date(d.date).toISOString().split('T')[0],
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }));

    // Add candlestick series
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderUpColor: '#26a69a',
      borderDownColor: '#ef5350',
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    candlestickSeries.setData(candleData);

    // Add moving averages with strict validation
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
    const periods = [3, 5, 10, 20, 50];

    periods.forEach((period, idx) => {
      const maSeries = chart.addLineSeries({
        color: colors[idx],
        lineWidth: 1,
        title: `MA${period}`,
      });

      const maKey = `MA${period}` as keyof StockDataWithIndicators;
      const maData = data
        .map(d => {
          const value = d[maKey];
          return {
            time: new Date(d.date).toISOString().split('T')[0],
            value: typeof value === 'number' && !isNaN(value) && isFinite(value) ? value : null,
          };
        })
        .filter(item => item.value !== null) as Array<{ time: string; value: number }>;

      if (maData.length > 0) {
        maSeries.setData(maData);
      }
    });

    chart.timeScale().fitContent();

    // Handle resize
    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({
          width: containerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height]);

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <div ref={containerRef} className="w-full" />
    </div>
  );
}
