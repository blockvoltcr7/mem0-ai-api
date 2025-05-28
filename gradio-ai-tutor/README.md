# 🏥 AI Prompt Engineering Tutor for Healthcare (Gradio)

A simple and reliable AI tutoring application built with Gradio that teaches healthcare professionals how to craft effective prompts for AI health coaching applications. Features memory-powered conversations using Mem0 and Qdrant for personalized learning experiences.

## ✨ Features

- 🧠 **Memory-Powered Conversations**: Uses Mem0 with Qdrant vector database to remember user interactions
- 🏥 **Healthcare Domain Focus**: Specialized knowledge in health AI prompt engineering
- 🔒 **User Isolation**: Each user's conversations are kept separate and private
- 📚 **Progressive Learning**: Builds on previous conversations and learning progress
- 🎯 **Simple Interface**: Clean Gradio UI that's easy to use and reliable
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Qdrant vector database (local or cloud)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd gradio-ai-tutor
   ```

2. **Install dependencies:**
   ```bash
   # From the parent directory
   uv pip sync ../requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file in the parent directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" >> ../.env
   echo "QDRANT_URL=http://localhost:6333" >> ../.env
   echo "QDRANT_USE_HTTPS=false" >> ../.env
   ```

4. **Run the application:**
   ```bash
   ./run.sh
   ```

   Or directly with Python:
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Local: http://localhost:7860
   - Network: http://0.0.0.0:7860

## 🎯 How to Use

### 1. User Identification
- Enter your **username** (2-50 characters)
- Enter your **phone number** (10+ digits, any format)
- Click **"🔑 Start Session"**

### 2. Learning Conversation
- Ask questions about prompt engineering for healthcare AI
- The AI tutor remembers your previous conversations
- Get personalized responses based on your learning progress

### 3. Features
- **📤 Send**: Submit your message to the AI tutor
- **🗑️ Clear Chat**: Clear current chat history (memory is preserved)
- **📚 Learning Summary**: View your learning progress and statistics

## 💡 Example Questions

Get started with these sample questions:

- "What are the key principles of prompt engineering for healthcare AI?"
- "How do I ensure safety when creating prompts for medical AI applications?"
- "Can you show me examples of effective health coaching prompts?"
- "What are the ethical considerations in healthcare AI prompting?"
- "How do I structure prompts for different healthcare scenarios?"

## 🔧 Technical Architecture

### Core Components

- **Frontend**: Gradio web interface
- **AI Model**: OpenAI GPT-4o-mini
- **Memory System**: Mem0 for conversation memory
- **Vector Database**: Qdrant for semantic search
- **Validation**: Pydantic for data validation

### Memory System

The application uses Mem0 to:
- Store conversation history per user
- Retrieve relevant context for responses
- Maintain learning progress across sessions
- Isolate user data for privacy

### User Identification

Users are identified by combining:
- Username + Phone number → Unique user ID
- Format: `username_cleanphonenumber`
- Example: `john_1234567890`

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ |
| `QDRANT_URL` | Qdrant database URL | `http://localhost:6333` | ❌ |
| `QDRANT_USE_HTTPS` | Use HTTPS for Qdrant | `false` | ❌ |

### Mem0 Configuration

```python
mem0_config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.1,
            "max_tokens": 1000
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "ai_tutor_memories",
            "client": qdrant_client,
            "embedding_model_dims": 1536,
            "on_disk": False
        }
    }
}
```

## 🧪 Testing Memory Isolation

To test that user memories are properly isolated:

1. **Create User A:**
   - Username: `alice`, Phone: `1234567890`
   - Have a conversation about prompt safety

2. **Create User B:**
   - Username: `bob`, Phone: `0987654321`
   - Have a conversation about prompt structure

3. **Return to User A:**
   - Same credentials should recall previous safety conversation
   - Should not know about Bob's structure conversation

## 🔍 Troubleshooting

### Common Issues

1. **Service Initialization Error**
   - Check OPENAI_API_KEY is set correctly
   - Verify Qdrant is running and accessible
   - Check network connectivity

2. **Memory Not Working**
   - Ensure Qdrant database is running
   - Check QDRANT_URL configuration
   - Verify user identification is consistent

3. **Phone Number Validation**
   - Use at least 10 digits
   - Any format accepted: +1234567890, (123) 456-7890, etc.
   - International numbers supported

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

- **Response Time**: ~2-3 seconds per message
- **Memory Retrieval**: ~500ms for context search
- **Concurrent Users**: Supports multiple simultaneous users
- **Memory Capacity**: Limited by Qdrant storage

## 🔒 Privacy & Security

- **User Isolation**: Each user's data is completely separate
- **No Authentication**: Simple username/phone identification
- **Local Storage**: All data stored in your Qdrant instance
- **No Data Sharing**: Conversations are not shared between users

## 🚧 Limitations

- No persistent user authentication
- Requires Qdrant database setup
- OpenAI API costs apply
- Memory limited to conversation history (no file uploads)

## 🤝 Contributing

This is a demonstration application. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with:
- OpenAI usage policies
- Healthcare data regulations (if applicable)
- Local privacy laws

## 🆘 Support

For issues or questions:
- Check the troubleshooting section above
- Review the logs for error messages
- Ensure all dependencies are properly installed
- Verify environment variables are set correctly

---

**⚠️ Important Medical Disclaimer**: This application is for educational purposes only. Always consult qualified healthcare professionals for medical advice. The AI responses should not be used as medical guidance. 