#!/bin/bash

# Setup script for development environment

echo "🚀 Setting up Screener MA Kuncup..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create environment file
if [ ! -f .env.local ]; then
  echo "📝 Creating .env.local from .env.example..."
  cp .env.example .env.local
  echo "✅ Created .env.local (you can customize it if needed)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  npm run dev"
echo ""
echo "Open http://localhost:3000 in your browser"
