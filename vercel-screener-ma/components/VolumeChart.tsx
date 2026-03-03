'use client';

import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import { StockDataWithIndicators } from '@/lib/indicators';

interface VolumeChartProps {
  data: StockDataWithIndicators[];
  title?: string;
  height?: number;
}

export function VolumeChart({ data, title = 'Volume', height = 200 }: VolumeChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<any>(null);

  useEffect(() => {
    if (!containerRef.current || data.length === 0) return;

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

    const volumeSeries = chart.addHistogramSeries({
      color: '#1E90FF',
    });

    const volumeData = data
      .filter(d => d.volume && typeof d.volume === 'number' && d.volume > 0)
      .map(d => ({
        time: new Date(d.date).toISOString().split('T')[0],
        value: d.volume,
        color: d.close >= d.open ? '#26a69a' : '#ef5350',
      }));

    if (volumeData.length > 0) {
      volumeSeries.setData(volumeData);
    }
    chart.timeScale().fitContent();

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
