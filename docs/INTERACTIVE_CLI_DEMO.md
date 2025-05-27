# Interactive Mem0 + Qdrant CLI Demo

This document provides instructions for using the interactive CLI demo script to showcase Mem0's memory capabilities with Qdrant vector database.

## 🎯 Purpose

The interactive CLI allows you to manually test and demonstrate:
- **Persistent Memory**: Conversations stored in Qdrant database
- **User Isolation**: Different users have separate memory spaces
- **Contextual AI**: AI responses use conversation history
- **Memory Search**: Find specific information from past conversations
- **Real-time Statistics**: Monitor memory usage and performance

## 🚀 Quick Start

### Prerequisites

1. **Environment Setup**: Ensure your `.env` file contains:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=qdrant-production-3e2f.up.railway.app
   QDRANT_USE_HTTPS=true
   ```

2. **Dependencies**: All required packages should be installed in your virtual environment.

### Running the Demo

```bash
# Activate virtual environment
source .venv/bin/activate

# Test that components work (optional)
python scripts/test_cli_functionality.py

# Start the interactive CLI
python scripts/interactive_mem0_qdrant_cli.py

# Or start with a specific user ID
python scripts/interactive_mem0_qdrant_cli.py "demo_user_john"
```

## 🎪 Demo Scenarios

### Scenario 1: Basic Memory Demonstration

1. **Start the CLI**:
   ```bash
   python scripts/interactive_mem0_qdrant_cli.py
   ```

2. **Initial Conversation**:
   ```
   💬 You: Hi, I'm John and I work as a software engineer at TechCorp
   🤖 AI: Hello John! Nice to meet you. It's great to know you're a software engineer at TechCorp...
   ```

3. **Test Memory Recall**:
   ```
   💬 You: What's my name and where do I work?
   🤖 AI: Your name is John and you work as a software engineer at TechCorp...
   ```

4. **Check Statistics**:
   ```
   💬 You: /stats
   📊 Session Statistics
     Total memories: 2
     Conversations: 2
     Current user: demo_user_a1b2c3d4
     Session duration: 1.2 minutes
   ```

### Scenario 2: Peptide Coaching Demo

1. **Run Automated Demo**:
   ```
   💬 You: /demo
   ```
   
   This runs through the complete BPC-157 peptide coaching scenario automatically.

2. **Manual Peptide Demo**:
   ```
   💬 You: Hi, I'm interested in peptide therapy
   🤖 AI: Hello! I'd be happy to help with information about peptide therapy...
   
   💬 You: I'm using BPC-157 for tissue repair at 250mcg daily
   🤖 AI: I understand you're using BPC-157 for tissue repair. Please remember that BPC-157 is not FDA-approved...
   
   💬 You: What peptide am I using?
   🤖 AI: Based on our conversation, you mentioned you're using BPC-157 for tissue repair at 250mcg daily...
   ```

### Scenario 3: User Isolation Demo

1. **Start with User A**:
   ```
   💬 You: I'm Alice and I love Python programming
   🤖 AI: Hello Alice! It's wonderful to meet a Python enthusiast...
   ```

2. **Switch to User B**:
   ```
   💬 You: /user bob_demo
   ✅ Switched from user 'demo_user_a1b2c3d4' to 'bob_demo'
   
   💬 You: What's my name?
   🤖 AI: I don't have any information about your name from our previous conversations...
   ```

3. **Switch Back to User A**:
   ```
   💬 You: /user demo_user_a1b2c3d4
   ✅ Switched from user 'bob_demo' to 'demo_user_a1b2c3d4'
   
   💬 You: What's my name?
   🤖 AI: Your name is Alice, and you mentioned you love Python programming...
   ```

### Scenario 4: Memory Search Demo

1. **Add Various Information**:
   ```
   💬 You: I work on machine learning projects
   💬 You: My favorite framework is TensorFlow
   💬 You: I'm learning about vector databases
   ```

2. **Search Memories**:
   ```
   💬 You: /search machine learning
   🔍 Found 1 memories for 'machine learning'
     1. User mentioned working on machine learning projects
   
   💬 You: /search TensorFlow
   🔍 Found 1 memories for 'TensorFlow'
     1. User's favorite framework is TensorFlow
   ```

3. **View All Memories**:
   ```
   💬 You: /memories
   📚 All Memories for User: demo_user_a1b2c3d4
     1. User mentioned working on machine learning projects
     2. User's favorite framework is TensorFlow
     3. User is learning about vector databases
   ```

## 🎛️ Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all available commands | `/help` |
| `/stats` | Display session statistics | `/stats` |
| `/search <query>` | Search memories for specific content | `/search Python` |
| `/user <user_id>` | Switch to different user | `/user alice_demo` |
| `/newuser` | Generate new random user ID | `/newuser` |
| `/memories` | Show all memories for current user | `/memories` |
| `/demo` | Run automated peptide coaching demo | `/demo` |
| `exit` or `quit` | End the session | `exit` |

## 🎨 Features for Demo

### Visual Feedback
- **Colored Output**: Different colors for different types of information
- **Real-time Status**: Shows memory search, AI generation, and storage progress
- **Statistics**: Live session and memory statistics

### Memory Capabilities
- **Persistent Storage**: All conversations stored in Qdrant
- **User Isolation**: Each user has separate memory space
- **Contextual Responses**: AI uses conversation history
- **Semantic Search**: Find relevant memories using natural language

### Performance Monitoring
- **Response Times**: Track memory search, AI generation, and storage times
- **Memory Count**: See how many memories are stored
- **Session Duration**: Monitor how long the demo has been running

## 🐛 Troubleshooting

### Common Issues

1. **Environment Variables Missing**:
   ```
   ❌ OPENAI_API_KEY not found in environment variables
   ```
   **Solution**: Check your `.env` file and ensure all required variables are set.

2. **Qdrant Connection Issues**:
   ```
   ❌ Failed to connect to Qdrant: Connection timeout
   ```
   **Solution**: Verify `QDRANT_URL` is correct and the service is running.

3. **Architecture Compatibility**:
   If you see pydantic_core architecture errors, the core functionality still works as demonstrated by the test suite.

### Testing Components

Before the demo, run the component test:
```bash
python scripts/test_cli_functionality.py
```

This verifies all components are working correctly.

## 📊 Demo Tips

### For Team Presentations

1. **Start Simple**: Begin with basic conversation to show memory works
2. **Show Persistence**: Demonstrate that information is remembered across questions
3. **User Isolation**: Switch users to show memory separation
4. **Search Capabilities**: Use `/search` to find specific information
5. **Statistics**: Use `/stats` to show technical metrics
6. **Automated Demo**: Use `/demo` for consistent peptide coaching scenario

### Key Points to Highlight

- **Persistent Memory**: Unlike ChatGPT, this remembers across sessions
- **User Isolation**: Each user has private memory space
- **Semantic Search**: Can find relevant information using natural language
- **Real-time Performance**: See actual response times and memory operations
- **Scalable Storage**: Uses Qdrant vector database for production-ready storage

## 🔧 Technical Details

### Architecture
- **Frontend**: Interactive CLI with colored output
- **Memory**: Mem0 library for memory management
- **Vector Store**: Qdrant for persistent storage
- **LLM**: OpenAI GPT-4o-mini for responses
- **Embeddings**: OpenAI text-embedding-ada-002

### Configuration
- **Collection**: `mem0_interactive_demo`
- **Embedding Dimensions**: 1536
- **Memory Limit**: 5 relevant memories per query
- **Response Limit**: 1000 tokens max

This CLI provides a comprehensive way to demonstrate Mem0's capabilities in a real-world scenario with persistent storage and user isolation. 