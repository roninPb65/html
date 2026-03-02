#!/bin/bash

echo "🚀 Starting Universal Data Analyzer..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Create directories
mkdir -p uploads outputs

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting Flask server..."
echo "   Backend: http://localhost:5000"
echo ""
echo "📖 To use the app:"
echo "   1. Open index.html in your browser"
echo "   2. Or visit: http://localhost:8000 (if using Python HTTP server)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask server
python app.py
