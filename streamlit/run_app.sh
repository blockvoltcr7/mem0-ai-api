#!/bin/bash

# Health Coach AI - Streamlit Application Launcher
# This script activates the virtual environment and runs the Streamlit app

echo "🧬 Health Coach AI - Starting Application..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   uv pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
fi

if [ -z "$QDRANT_URL" ]; then
    echo "⚠️  Warning: QDRANT_URL not set"
fi

# Run the application
echo "🚀 Starting Streamlit application..."
echo "📱 Open your browser to: http://localhost:8501"
echo "🔐 Demo credentials: username=demo_user, password=demo123"
echo ""

streamlit run app.py 