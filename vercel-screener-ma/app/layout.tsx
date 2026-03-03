import type { Metadata } from 'next';
import './globals.css';
import { Navigation } from '@/components/Navigation';

export const metadata: Metadata = {
  title: 'Screener MA Kuncup',
  description: 'Deteksi pola MA Kuncup (MA Ketat) di Bursa Efek Indonesia',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="bg-gray-50">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 py-8">
          {children}
        </main>
        <footer className="bg-gray-100 border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <p className="text-xs text-gray-600 text-center">
              Based on techniques by Pak T (@TradingDiary2) and summarized by @ikhwanuddin
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
