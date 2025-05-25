#!/bin/bash

echo "🧠 Starting Sina - The Disciplined Mentor"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
    echo "💡 Tip: Create one with 'python3 -m venv venv'"
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing/checking dependencies..."
    pip install -r requirements.txt
fi

# Make the startup script executable
chmod +x start_sina.py

# Start the application
echo "🚀 Starting Sina application..."
python3 start_sina.py 