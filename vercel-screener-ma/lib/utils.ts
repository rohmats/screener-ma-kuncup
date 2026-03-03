import React from 'react';

/**
 * Utils for the UI components
 */

export function formatNumber(value: number, decimals: number = 2): string {
  return value.toFixed(decimals);
}

export function formatVolume(volume: number): string {
  if (volume >= 1_000_000) {
    return (volume / 1_000_000).toFixed(1) + 'M';
  }
  if (volume >= 1_000) {
    return (volume / 1_000).toFixed(1) + 'K';
  }
  return volume.toString();
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function getSignalColor(signal: boolean): string {
  return signal ? 'text-green-600' : 'text-gray-400';
}

export function getTightColor(tight: boolean): string {
  return tight ? 'text-green-600' : 'text-gray-400';
}
