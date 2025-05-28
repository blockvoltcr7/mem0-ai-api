# 🧬 Health Coach AI - Peptide Therapy Assistant (Gradio)

A specialized AI health coach application focused on peptide therapy education and guidance, converted from Streamlit to Gradio with enhanced user experience and the same powerful functionality.

## ⚠️ Important Medical Disclaimer

**This application is for educational purposes only.** Peptides like BPC-157 are not FDA-approved for human use and should only be used under proper medical supervision. Always consult with qualified healthcare professionals before starting any peptide therapy.

## 🚀 Features

### 🎯 Core Functionality
- **AI Health Coach**: Specialized in peptide therapy with evidence-based responses
- **Memory-Powered Conversations**: Remembers health profiles and conversation history using Mem0 + Qdrant
- **Persistent Storage**: Health profiles saved across sessions - no need to refill
- **Optional Profiles**: Start chatting immediately or complete profile for personalized advice
- **User Isolation**: Complete separation of user data and conversation memories
- **Health Profile Management**: Comprehensive onboarding and profile tracking

### 👥 Demo Users
The application includes 3 pre-configured demo users:

| User | Profile | Specialty Focus |
|------|---------|----------------|
| **John Smith** | New to peptide therapy | Basic education and learning |
| **Jane Doe** | Experienced with BPC-157 | Athletic performance optimization |
| **Jarvis Wilson** | Health enthusiast | Gut health improvement |

### 📋 Health Profile System
- **Optional Setup**: Skip profile to chat immediately or complete for personalized advice
- **Persistent Storage**: Profiles saved in Qdrant database across sessions
- **Peptide Usage Tracking**: Current peptide usage status
- **BPC-157 Details**: Specific dosage and duration tracking
- **Health Goals**: Customizable health and wellness objectives
- **Medical History**: Conditions and current medications tracking
- **Profile Management**: Edit, reset, skip, and view profile summary

### 💬 Intelligent Chat System
- **Immediate Access**: Start chatting without completing profile
- **Adaptive Responses**: General advice or personalized recommendations based on profile
- **Context-aware responses** based on health profile and conversation history
- **Memory of previous conversations** across sessions
- **Safety-first recommendations** with medical supervision emphasis
- **Educational Content**: Evidence-based peptide therapy information

## 🛠️ Technology Stack

- **Frontend**: Gradio (Web UI Framework)
- **AI Model**: OpenAI GPT-4o-mini
- **Memory System**: Mem0 (Memory management)
- **Vector Database**: Qdrant (Conversation storage)
- **Data Validation**: Pydantic V2
- **Environment**: Python 3.8+

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Qdrant vector database (local or cloud)

### 1. Environment Setup
```bash
# Clone or navigate to the project directory
cd gradio-peptides-app

# Create virtual environment (recommended)
uv venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate     # On Windows

# Install dependencies
uv pip install -r ../requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the project root:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults provided)
QDRANT_URL=http://localhost:6333
QDRANT_USE_HTTPS=false
```

### 3. Database Setup
**Option A: Local Qdrant (Recommended for development)**
```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant

# Using pip
pip install qdrant-client
# Then use the in-memory mode (automatic)
```

**Option B: Qdrant Cloud**
1. Sign up for Qdrant Cloud
2. Create a cluster
3. Update `QDRANT_URL` and `QDRANT_USE_HTTPS=true` in your `.env`

## 🚀 Running the Application

### Quick Start
```bash
# Make run script executable (first time only)
chmod +x run.sh

# Launch the application
./run.sh
```

### Manual Launch
```bash
python app.py
```

### Access the Application
- **Local**: http://localhost:7861
- **Network**: http://0.0.0.0:7861 (accessible from other devices on your network)

## 📖 Usage Guide

### Getting Started
1. **Select a Demo User**: Choose from John, Jane, or Jarvis
2. **Login**: Click the login button to authenticate
3. **Choose Your Path**:
   - **Start Chatting Immediately**: Ask questions for general peptide therapy advice
   - **Complete Health Profile**: Fill out the questionnaire for personalized recommendations
   - **Skip Profile**: Use the skip button to chat with general advice

### Flexible Profile Management
The application offers three approaches to health profiling:

#### Option 1: Immediate Chat (No Profile Required)
- Start asking questions right away
- Receive general, evidence-based advice
- Complete profile later for personalized recommendations

#### Option 2: Complete Health Profile First
- Fill out the comprehensive health questionnaire
- Get personalized advice based on your specific situation
- Profile is saved permanently across sessions

#### Option 3: Skip Profile Setup
- Click "Skip Profile & Start Chatting" 
- Chat immediately with general advice
- Complete profile anytime later

### Health Profile Setup
When you choose to complete your health profile, the application guides you through:

#### Basic Information
- **Peptide Usage**: Whether you currently use any peptides
- **BPC-157 Specific**: Usage, dosage, and duration details

#### Health Details
- **Goals**: Select from tissue repair, injury recovery, gut health, etc.
- **Medical Conditions**: Track relevant health conditions
- **Medications**: List current medications and supplements

### Persistent Data
- **Automatic Saving**: Health profiles are automatically saved to Qdrant database
- **Cross-Session Memory**: Your profile and conversation history persist between sessions
- **No Re-entry Required**: Once saved, your profile loads automatically on future logins

### Chat Features
- **Personalized Responses**: AI considers your health profile when available
- **General Advice**: Quality information even without completed profile
- **Memory Retention**: Remembers previous conversations across sessions
- **Safety Focus**: Emphasizes medical supervision and safety regardless of profile status
- **Educational Content**: Evidence-based peptide therapy information

## 🔧 Configuration

### Memory Settings
The application uses Mem0 for intelligent memory management:
- **Collection Name**: `health_coach_memories`
- **Embedding Model**: 1536 dimensions
- **LLM Model**: GPT-4o-mini
- **Memory Limit**: 5 relevant memories per query

### User Isolation
Each demo user has completely isolated:
- Health profiles
- Conversation memories
- Chat histories
- Personal recommendations

## 🧪 Testing & Development

### Manual Testing
1. Select each demo user and complete different health profiles
2. Test various conversation scenarios
3. Verify memory persistence across sessions
4. Check profile management features

### Conversation Testing
Try these example conversations:
- "What is BPC-157 and how does it work?"
- "I'm new to peptides, where should I start?"
- "What are the potential side effects I should watch for?"
- "Can you help me understand proper dosing?"

## 🔒 Privacy & Security

- **Data Isolation**: Each user's data is completely separate
- **Local Storage**: Health profiles stored in application memory
- **Memory Management**: Conversations stored in Qdrant with user-specific isolation
- **No Authentication**: Demo mode only - no real user credentials stored

## 🐛 Troubleshooting

### Common Issues

**Service Initialization Error**
```
⚠️ Service Initialization Error: Please check your environment variables
```
- Verify `OPENAI_API_KEY` is set correctly
- Check Qdrant connection (`QDRANT_URL`)
- Ensure all dependencies are installed

**Memory Service Issues**
- Restart Qdrant service
- Check Qdrant logs for connection errors
- Verify network connectivity to Qdrant URL

**Profile Not Saving**
- Complete all required fields in health profile
- Check for validation errors in profile status
- Try resetting and re-completing the profile

### Debug Mode
Enable detailed logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deployment

### Local Network Deployment
The application is configured to run on `0.0.0.0:7861`, making it accessible to other devices on your local network.

### Production Considerations
For production deployment:
1. Use environment variables for all configuration
2. Set up proper authentication system
3. Use production-grade Qdrant deployment
4. Implement proper error handling and logging
5. Add rate limiting and usage monitoring

## 🔄 Migration from Streamlit

This application maintains feature parity with the original Streamlit version:

### Preserved Features
- ✅ Complete health profile onboarding
- ✅ Memory-powered chat system
- ✅ User isolation and data management
- ✅ BPC-157 specific tracking
- ✅ Medical safety emphasis

### Gradio Enhancements
- 🔄 Improved user interface and experience
- 📱 Better mobile responsiveness
- ⚡ Faster page loads and interactions
- 🎨 Modern, clean design
- 🔧 Enhanced error handling

## 📚 References & Resources

### Peptide Therapy Education
- Research papers on BPC-157 mechanisms
- Safety guidelines for peptide use
- Healthcare professional consultation importance

### Technical Documentation
- [Gradio Documentation](https://gradio.app/docs/)
- [Mem0 Documentation](https://mem0.ai/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI API Reference](https://platform.openai.com/docs)

## 🤝 Contributing

This application is part of a larger AI tutoring system. For modifications:
1. Follow existing code patterns
2. Maintain user isolation principles
3. Preserve medical safety messaging
4. Test with all demo users
5. Update documentation accordingly

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with relevant medical device regulations and AI ethics guidelines when deploying in production environments.

---

**💡 Remember**: This is an educational tool. Always consult healthcare professionals for medical advice and before starting any peptide therapy regimen. 