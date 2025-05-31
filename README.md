# 🧠 Mem01 AI Applications - OpenAI + Mem0 + Qdrant

A collection of advanced AI applications demonstrating **persistent memory capabilities** using **OpenAI GPT models**, **Mem0** memory framework, and **Qdrant** vector database. These applications showcase how to build intelligent, memory-powered AI systems that remember user interactions across sessions.

[![Youtube Tutorial Demo](https://img.youtube.com/vi/ElnD4vOUQ8E/0.jpg)](https://www.youtube.com/watch?v=ElnD4vOUQ8E&t=177s)

## 🚀 Featured Applications

### 🧬 Health Coach AI - Peptide Therapy Assistant
**Location**: `gradio-peptides-app/`

A specialized AI health coach focused on peptide therapy education and guidance, featuring:
- **Memory-Powered Conversations**: Remembers health profiles and chat history using Mem0 + Qdrant
- **Optional Health Profiles**: Start chatting immediately or complete profile for personalized advice
- **Persistent Storage**: Health data saved across sessions - no need to refill forms
- **3 Demo Users**: John (beginner), Jane (experienced), Jarvis (gut health focus)
- **Safety-First**: Emphasizes medical supervision and evidence-based information

**Tech Stack**: Gradio + OpenAI GPT-4o-mini + Mem0 + Qdrant + Pydantic V2

[📖 View Full Documentation](gradio-peptides-app/README.md)

### 🏥 AI Prompt Engineering Tutor for Healthcare  
**Location**: `gradio-ai-tutor/`

An educational AI tutor that teaches healthcare professionals effective prompt engineering for medical AI applications:
- **Progressive Learning**: Builds on previous conversations and learning progress
- **Healthcare Domain Focus**: Specialized in health AI prompt engineering best practices
- **User Isolation**: Complete separation of learning sessions between users
- **Simple Interface**: Clean, reliable Gradio UI for easy learning

**Tech Stack**: Gradio + OpenAI GPT-4o-mini + Mem0 + Qdrant + Pydantic

[📖 View Full Documentation](gradio-ai-tutor/README.md)

## 🛠️ Core Technologies

### 🧠 Memory Architecture
- **Mem0**: Advanced memory management framework for AI applications
- **Qdrant**: High-performance vector database for semantic search and memory storage
- **OpenAI GPT-4o-mini**: Fast, intelligent language model for conversations
- **Persistent Memory**: User interactions and profiles saved across sessions

### 🔧 Development Stack
- **Frontend**: Gradio for rapid web UI development
- **Data Validation**: Pydantic V2 for robust data modeling
- **Package Management**: UV for fast Python dependency management
- **Testing**: Pytest with Allure reporting

## 📦 Quick Start

### Prerequisites
- Python 3.8+ 
- OpenAI API key
- Qdrant vector database (local or cloud)

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd mem01-ai-tutor

# Create virtual environment
uv venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate     # On Windows

# Install dependencies  
uv pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults provided)
QDRANT_URL=http://localhost:6333
QDRANT_USE_HTTPS=false
```

### 3. Database Setup
**Option A: Local Qdrant (Development)**
```bash
# Using Docker (recommended)
docker run -p 6333:6333 qdrant/qdrant

# Using pip
pip install qdrant-client
```

**Option B: Qdrant Cloud (Production)**
1. Sign up for [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a cluster and get your URL
3. Update `.env` with your cloud URL and set `QDRANT_USE_HTTPS=true`

### 4. Launch Applications

**Health Coach AI (Peptide Therapy)**:
```bash
cd gradio-peptides-app
./run.sh
# Access: http://localhost:7861
```

**AI Prompt Engineering Tutor**:
```bash  
cd gradio-ai-tutor
./run.sh
# Access: http://localhost:7860
```

## 🏗️ Project Structure

```
mem01-ai-tutor/
├── 📁 gradio-peptides-app/          # Health Coach AI for peptide therapy
│   ├── app.py                       # Main Gradio application (31KB)
│   ├── README.md                    # Detailed documentation
│   ├── run.sh                       # Launch script
│   └── test_gradio_peptides.py      # Application tests
├── 📁 gradio-ai-tutor/              # AI Prompt Engineering Tutor
│   ├── app.py                       # Main Gradio application (15KB)
│   ├── README.md                    # Detailed documentation
│   └── run.sh                       # Launch script
├── 📁 tests/                        # Comprehensive test suite
├── 📁 docs/                         # Project documentation
├── 📁 scripts/                      # Utility scripts
├── 🔧 requirements.txt              # Python dependencies
├── 🔧 requirements.in               # Dependency definitions
├── 🔧 .env.example                  # Environment template
└── 📚 README.md                     # This file
```

## 🎯 Key Features Demonstrated

### Memory Management
- **Persistent Conversations**: Chat history saved across sessions
- **User Isolation**: Complete data separation between users
- **Context-Aware Responses**: AI remembers previous interactions
- **Profile Storage**: User data persisted in vector database

### Advanced AI Capabilities
- **Domain Specialization**: Applications focused on specific use cases
- **Safety-First Design**: Responsible AI with appropriate disclaimers
- **Adaptive Responses**: Different advice based on user profiles/progress
- **Evidence-Based**: Grounded in factual information

### Production-Ready Architecture
- **Scalable Database**: Qdrant vector storage for large-scale deployment
- **Modern UI**: Gradio for rapid, responsive web interfaces
- **Robust Validation**: Pydantic models for data integrity
- **Comprehensive Testing**: Full test coverage with detailed reporting

## 🧪 Testing & Development

### Running Tests
```bash
# Run all tests with Allure reporting
pytest --alluredir=allure-results -v

# Generate and serve test report
allure serve allure-results
```

### Application-Specific Tests
```bash
# Test Health Coach AI
pytest gradio-peptides-app/test_gradio_peptides.py -v

# Test AI Tutor (manual)
python gradio-ai-tutor/app.py
```

### Memory Isolation Testing
Each application includes comprehensive tests to verify:
- User data separation
- Memory persistence across sessions
- Proper conversation history management
- Profile storage and retrieval

## 🚀 Deployment Options

### Local Development
Both applications include run scripts for immediate local deployment:
```bash
./run.sh  # In each application directory
```

### Cloud Deployment
The repository includes configurations for:
- **Railway**: `railway.json`, `Dockerfile.railway`
- **Render**: `render.yaml`, deployment scripts
- **Docker**: Multi-stage Dockerfiles for production

## 🔍 Use Cases & Applications

### Healthcare AI Development
- **Prompt Engineering Training**: Learn effective healthcare AI prompting
- **Patient Education**: Specialized health coaching applications
- **Medical AI Safety**: Best practices for responsible health AI

### Memory-Powered AI Systems
- **Persistent Conversations**: Building AI that remembers users
- **Profile Management**: Storing and retrieving user preferences
- **Context-Aware Responses**: Intelligent, personalized interactions

### Gradio Application Development
- **Rapid Prototyping**: Fast UI development for AI applications
- **User Authentication**: Simple user identification systems
- **Data Validation**: Robust input handling with Pydantic

## ⚠️ Important Notes

### Medical Disclaimer
The Health Coach AI application is **for educational purposes only**. Peptides like BPC-157 are not FDA-approved for human use. Always consult qualified healthcare professionals before starting any therapy.

### API Usage
These applications use OpenAI's API which incurs costs. Monitor your usage and set appropriate limits.

### Data Privacy
- User conversations are stored in your Qdrant database
- No data is shared between users
- Consider data retention policies for production use

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- Additional AI application examples
- Enhanced memory management patterns
- New deployment configurations
- Improved testing coverage
- Documentation improvements

### Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📚 Additional Resources

### Documentation
- [Health Coach AI Documentation](gradio-peptides-app/README.md)
- [AI Tutor Documentation](gradio-ai-tutor/README.md)
- [Qdrant API Reference](README_QDRANT_API.md)
- [Railway Deployment Guide](README_RAILWAY_DEPLOYMENT.md)

### Related Projects
- [Mem0 Framework](https://github.com/mem0ai/mem0)
- [Qdrant Vector Database](https://github.com/qdrant/qdrant)
- [Gradio ML Interfaces](https://github.com/gradio-app/gradio)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🚀 Ready to build memory-powered AI applications?** Start with either the Health Coach AI or AI Tutor, and explore how Mem0 + Qdrant create intelligent, persistent AI experiences! 
