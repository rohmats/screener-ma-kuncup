'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2 hover:opacity-80">
            <span className="text-2xl">📊</span>
            <div>
              <h1 className="text-xl font-bold text-gray-800">Screener MA Kuncup</h1>
              <p className="text-xs text-gray-600">Deteksi pola MA Kuncup di BEI</p>
            </div>
          </Link>

          <div className="flex items-center space-x-6">
            <Link
              href="/"
              className={`text-sm font-medium transition ${
                isActive('/') ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              🏠 Home
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
