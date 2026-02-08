#!/bin/bash

# AI Cost Observatory - Quick Start Script

set -e

echo "🔭 AI Cost Observatory - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install SDK
echo "📥 Installing SDK..."
cd sdk
pip install -e . > /dev/null 2>&1
cd ..

# Install server dependencies
echo "📥 Installing server dependencies..."
cd server
pip install -r requirements.txt > /dev/null 2>&1
cd ..

# Install UI dependencies
echo "📥 Installing UI dependencies..."
cd ui
pip install -r requirements.txt > /dev/null 2>&1
cd ..

# Initialize database
echo "🗄️  Initializing database..."
cd server
python -c "from database import init_db; init_db()" > /dev/null 2>&1
cd ..

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the system:"
echo ""
echo "1. Start the API server (in terminal 1):"
echo "   cd server && python -m api.main"
echo ""
echo "2. Start the dashboard (in terminal 2):"
echo "   cd ui && streamlit run dashboard.py"
echo ""
echo "3. Run an example (in terminal 3):"
echo "   export OPENAI_API_KEY=your-key"
echo "   python examples/basic_openai.py"
echo ""
echo "4. View dashboard at: http://localhost:8501"
echo ""
echo "📚 For more info, see README.md"
