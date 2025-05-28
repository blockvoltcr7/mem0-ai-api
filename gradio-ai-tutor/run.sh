#!/bin/bash

# AI Prompt Engineering Tutor - Gradio Application Runner
# Simple and reliable healthcare prompt engineering education tool

echo "🏥 Starting AI Prompt Engineering Tutor (Gradio)"
echo "================================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating your virtual environment first"
    echo ""
fi

# Check for required environment variables
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    echo "   Please set your OpenAI API key in your .env file"
    exit 1
fi

if [[ -z "$QDRANT_URL" ]]; then
    echo "⚠️  Warning: QDRANT_URL not set, using default: http://localhost:6333"
    export QDRANT_URL="http://localhost:6333"
fi

echo "✅ Environment variables configured"
echo "🚀 Launching Gradio application..."
echo ""
echo "📱 The app will be available at: http://localhost:7860"
echo "🔗 Network access: http://0.0.0.0:7860"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the Gradio application
python app.py 