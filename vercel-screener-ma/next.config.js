// next.config.js with Vercel optimizations

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  
  // Image optimization
  images: {
    unoptimized: true,
  },

  // Headers for security and CORS
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type' },
          { key: 'Cache-Control', value: 'public, max-age=3600' },
        ],
      },
    ]
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/stock/:ticker',
        destination: '/detail/:ticker',
        permanent: true,
      },
    ]
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_APP_NAME: 'Screener MA Kuncup',
    NEXT_PUBLIC_APP_VERSION: '1.0.0',
  },
}

module.exports = nextConfig
