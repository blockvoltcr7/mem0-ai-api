# AI Agent Mem0 API with Qdrant Vector Database

## Overview

This API provides a sophisticated conversational AI system with **persistent memory** capabilities, powered by **Mem0**, **Qdrant vector database**, and **OpenAI**. The system enables context-aware conversations that remember user interactions across sessions, making it ideal for coaching, consultation, and educational applications.

## 🚀 Key Features

### 🧠 Persistent Memory System
- **Cross-session memory**: Conversations persist across API calls and sessions
- **User isolation**: Each user maintains their own private memory space
- **Context-aware responses**: AI leverages conversation history for relevant answers
- **Memory statistics**: Track memory creation and retrieval metrics

### 🔍 Vector-Powered Search
- **Qdrant integration**: High-performance vector database for semantic search
- **OpenAI embeddings**: 1536-dimensional vectors for precise memory matching
- **Similarity search**: Retrieve relevant memories based on semantic similarity
- **Scalable storage**: Production-ready vector storage with Railway deployment

### 📊 Production-Ready Monitoring
- **Health endpoints**: Comprehensive system status monitoring
- **Performance metrics**: Response times and memory retrieval statistics
- **Error handling**: Structured error responses with actionable suggestions
- **Logging**: Detailed application logs for debugging and monitoring

### 📖 Interactive Documentation
- **Swagger UI**: Full interactive API documentation at `/docs`
- **ReDoc**: Alternative documentation view at `/redoc`
- **OpenAPI schema**: Machine-readable API specification at `/openapi.json`

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Mem0 System   │    │ Qdrant Vector   │
│                 │◄──►│                 │◄──►│   Database      │
│ • REST Endpoints│    │ • Memory Mgmt   │    │ • Vector Store  │
│ • Swagger UI    │    │ • Context Aware │    │ • Similarity    │
│ • Health Checks │    │ • User Isolation│    │ • Collections   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OpenAI API    │    │  User Sessions  │    │  Railway Cloud  │
│                 │    │                 │    │                 │
│ • GPT-4 Model   │    │ • Session IDs   │    │ • Hosted Qdrant │
│ • Embeddings    │    │ • Metadata      │    │ • SSL/TLS       │
│ • Completions   │    │ • Context Tags  │    │ • Auto-scaling  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **User Request**: Client sends message with `user_id` and optional metadata
2. **Memory Retrieval**: System searches Qdrant for relevant user memories
3. **Context Building**: Retrieved memories provide context for AI response
4. **AI Generation**: OpenAI generates response using conversation context
5. **Memory Storage**: New conversation stored as vector embeddings in Qdrant
6. **Response**: Structured response with AI answer and memory statistics

## 📚 API Documentation

### Swagger UI (`/docs`)

**Access**: http://localhost:8000/docs

The Swagger UI provides a comprehensive, interactive interface for testing and exploring the API:

#### Features:
- **Try it out**: Execute API calls directly from the browser
- **Request/Response examples**: Multiple realistic scenarios for each endpoint
- **Parameter validation**: Real-time validation with helpful error messages
- **Schema exploration**: Detailed model definitions and field descriptions
- **Authentication testing**: Built-in support for API key testing (when enabled)

#### Organized Sections:
- **🧠 Chat Endpoints**: Main conversational AI functionality
- **📊 Health Endpoints**: System monitoring and status checks
- **👋 Hello Endpoints**: Basic API information and root endpoints

#### Interactive Testing:
```json
// Example chat request in Swagger UI
{
  "user_id": "user123",
  "message": "Tell me about BPC-157 peptide benefits",
  "session_id": "consultation_2024",
  "metadata": {
    "domain": "peptide_coaching",
    "context": "health_consultation"
  }
}
```

### ReDoc (`/redoc`)

**Access**: http://localhost:8000/redoc

ReDoc provides an alternative, clean documentation view:

#### Features:
- **Clean layout**: Focused on readability and navigation
- **Detailed descriptions**: Rich markdown formatting with examples
- **Code samples**: Multiple programming language examples
- **Downloadable**: Export documentation for offline use
- **Search functionality**: Quick navigation through endpoints

#### Benefits:
- **Developer-friendly**: Ideal for integration planning
- **Comprehensive**: Complete API reference with all details
- **Professional**: Suitable for sharing with stakeholders
- **Mobile-responsive**: Accessible on all devices

### OpenAPI Schema (`/openapi.json`)

**Access**: http://localhost:8000/openapi.json

Machine-readable API specification for:
- **Code generation**: Auto-generate client libraries
- **Testing tools**: Import into Postman, Insomnia, etc.
- **Documentation**: Generate custom documentation
- **Validation**: Ensure API compliance

## 🔧 How It Works

### Memory Persistence Mechanism

#### 1. User Identification
```python
# Each user gets isolated memory space
user_id = "user123"  # Consistent across sessions
session_id = "consultation_2024"  # Optional grouping
```

#### 2. Memory Storage
- **Conversation vectorization**: Messages converted to 1536-dim embeddings
- **Metadata enrichment**: Domain, context, and user preferences stored
- **Qdrant storage**: Vectors stored with metadata for efficient retrieval

#### 3. Memory Retrieval
- **Semantic search**: Find relevant memories using vector similarity
- **Context filtering**: Use metadata to narrow search scope
- **Relevance ranking**: Return most relevant memories first

#### 4. Context-Aware Response
- **Memory integration**: Retrieved memories provide conversation context
- **AI generation**: OpenAI uses context to generate relevant responses
- **Continuous learning**: New interactions stored for future reference

### Example Conversation Flow

#### First Interaction:
```json
POST /api/v1/chat
{
  "user_id": "athlete_001",
  "message": "I'm interested in peptides for recovery",
  "metadata": {"domain": "sports_medicine"}
}

Response:
{
  "response": "Peptides can be excellent for recovery...",
  "memories_found": 0,     // No previous memories
  "memories_created": 1,   // New memory created
  "user_id": "athlete_001"
}
```

#### Follow-up Interaction:
```json
POST /api/v1/chat
{
  "user_id": "athlete_001",
  "message": "What about BPC-157 specifically?",
  "metadata": {"domain": "sports_medicine"}
}

Response:
{
  "response": "Based on your interest in recovery peptides, BPC-157...",
  "memories_found": 1,     // Previous conversation found
  "memories_created": 1,   // New memory created
  "user_id": "athlete_001"
}
```

## 🎯 Benefits

### For Developers

#### 1. **Rapid Development**
- **Pre-built infrastructure**: Complete AI system ready to use
- **Interactive testing**: Swagger UI eliminates need for external tools
- **Comprehensive documentation**: Self-documenting API with examples
- **Error handling**: Structured error responses with actionable guidance

#### 2. **Production Ready**
- **Scalable architecture**: Qdrant handles millions of vectors
- **Health monitoring**: Built-in endpoints for system status
- **Performance metrics**: Response time and memory statistics
- **Cloud deployment**: Railway integration for easy scaling

#### 3. **Flexible Integration**
- **RESTful API**: Standard HTTP interface for any programming language
- **OpenAPI compliance**: Generate client libraries automatically
- **Metadata support**: Customize behavior with domain-specific context
- **Session management**: Organize conversations by topic or time

### For Applications

#### 1. **Enhanced User Experience**
- **Contextual conversations**: AI remembers previous interactions
- **Personalized responses**: Tailored to user's history and preferences
- **Consistent experience**: Memory persists across sessions and devices
- **Progressive learning**: System improves with each interaction

#### 2. **Domain Specialization**
- **Coaching applications**: Remember client goals and progress
- **Educational platforms**: Track learning progress and preferences
- **Customer support**: Maintain conversation history and context
- **Healthcare**: Remember patient information and consultation history

#### 3. **Business Intelligence**
- **Conversation analytics**: Track user engagement and topics
- **Memory statistics**: Understand system usage patterns
- **Performance monitoring**: Optimize response times and accuracy
- **User insights**: Analyze conversation patterns and preferences

### For Operations

#### 1. **Monitoring & Observability**
- **Health endpoints**: `/health` for basic checks, `/health/detailed` for comprehensive status
- **Performance metrics**: Response times, memory retrieval speed, system load
- **Error tracking**: Structured error responses with diagnostic information
- **Logging**: Comprehensive application logs for debugging

#### 2. **Scalability**
- **Vector database**: Qdrant handles large-scale vector operations
- **Cloud deployment**: Railway provides auto-scaling infrastructure
- **Memory optimization**: Efficient storage and retrieval of conversation data
- **Load balancing**: Multiple instances supported with shared vector store

#### 3. **Reliability**
- **Error resilience**: Graceful handling of service failures
- **Data persistence**: Conversations stored reliably in Qdrant
- **Backup & recovery**: Vector data can be backed up and restored
- **Monitoring**: Real-time health checks and alerting

## 🚀 Quick Start

### 1. Start the API Server
```bash
# Activate virtual environment
source .venv/bin/activate

# Start server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access Documentation
```bash
# Open Swagger UI automatically
python scripts/open_swagger_ui.py

# Or visit manually
open http://localhost:8000/docs
```

### 3. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Detailed system status
curl http://localhost:8000/api/v1/health/detailed

# Chat test
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "Hello! Tell me about peptides.",
    "metadata": {"domain": "health_coaching"}
  }'
```

## 📊 API Endpoints

### Chat Endpoints

#### `POST /api/v1/chat`
**Purpose**: Main conversational AI endpoint with persistent memory

**Request**:
```json
{
  "user_id": "string",           // Required: Unique user identifier
  "message": "string",           // Required: User's message
  "session_id": "string",        // Optional: Session grouping
  "metadata": {                  // Optional: Context metadata
    "domain": "string",
    "context": "string",
    "preferences": {}
  }
}
```

**Response**:
```json
{
  "response": "string",          // AI-generated response
  "memories_found": 0,           // Number of relevant memories retrieved
  "memories_created": 1,         // Number of new memories created
  "user_id": "string",           // User identifier
  "session_id": "string",        // Session identifier (if provided)
  "metadata": {                  // Processing metadata
    "model_used": "gpt-4",
    "response_time_ms": 1250,
    "memory_retrieval_time_ms": 45
  }
}
```

### Health Endpoints

#### `GET /api/v1/health/detailed`
**Purpose**: Comprehensive system health check

**Response**:
```json
{
  "status": "healthy",           // Overall status: healthy/degraded/unhealthy
  "services": {
    "mem0": {
      "status": "initialized",
      "collection_name": "mem0_production",
      "memory_count": 1247
    },
    "qdrant": {
      "status": "connected",
      "collections": 11,
      "url": "https://qdrant-production.railway.app"
    },
    "openai": {
      "status": "available",
      "models": 75,
      "default_model": "gpt-4"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### `GET /api/v1/health`
**Purpose**: Basic health check for load balancers

**Response**:
```json
{
  "status": "healthy",
  "message": "AI Agent API is running successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Basic Endpoints

#### `GET /`
**Purpose**: API information and documentation links

**Response**:
```json
{
  "message": "AI Agent Mem0 API",
  "version": "1.0.0",
  "environment": "production",
  "status": "running",
  "docs_url": "/docs",
  "redoc_url": "/redoc",
  "openapi_url": "/openapi.json"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_instance_url

# Optional
QDRANT_COLLECTION_NAME=mem0_production
ENVIRONMENT=production
LOG_LEVEL=INFO
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
```

### Qdrant Configuration
- **Collection**: Automatically created if not exists
- **Vector size**: 1536 dimensions (OpenAI embeddings)
- **Distance metric**: Cosine similarity
- **Storage**: Persistent storage with Railway deployment

## 📈 Performance Metrics

### Typical Response Times
- **Health check**: 50-100ms
- **Memory retrieval**: 30-80ms
- **AI generation**: 1000-3000ms
- **Total chat response**: 1200-3500ms

### Memory Statistics
- **Storage efficiency**: ~1KB per conversation memory
- **Retrieval accuracy**: 85-95% relevance for semantic search
- **Scalability**: Supports millions of memories per user
- **Concurrent users**: Limited by OpenAI API rate limits

## 🛠️ Development Tools

### Testing Scripts
```bash
# Comprehensive API testing
python scripts/test_ai_agent_api.py

# Connection debugging
python debug_connection.py

# Swagger UI launcher
python scripts/open_swagger_ui.py
```

### Automated Testing
```bash
# Run pytest with Allure reporting
pytest tests/test_ai_agent_api.py --alluredir=allure-results -v

# Generate test report
allure serve allure-results
```

## 📋 Use Cases

### 1. Health & Wellness Coaching
- **Peptide coaching**: Remember client protocols and progress
- **Nutrition guidance**: Track dietary preferences and restrictions
- **Fitness planning**: Maintain workout history and goals

### 2. Educational Platforms
- **Personalized tutoring**: Adapt to student's learning style and progress
- **Course assistance**: Remember completed modules and current topics
- **Q&A systems**: Provide context-aware answers based on course material

### 3. Customer Support
- **Technical support**: Remember previous issues and solutions
- **Account management**: Maintain customer interaction history
- **Product recommendations**: Suggest based on previous inquiries

### 4. Professional Services
- **Legal consultation**: Track case details and client communications
- **Financial advisory**: Remember investment preferences and risk tolerance
- **Medical consultation**: Maintain patient history and treatment plans

## 🔒 Security Considerations

### Data Privacy
- **User isolation**: Each user's memories are completely isolated
- **Metadata filtering**: Control access to memories based on context
- **No data sharing**: Memories are never shared between users

### API Security
- **Input validation**: All requests validated against Pydantic schemas
- **Error handling**: No sensitive information exposed in error messages
- **Rate limiting**: Can be implemented at the reverse proxy level

### Infrastructure Security
- **HTTPS**: All communications encrypted in transit
- **Railway deployment**: Managed infrastructure with security updates
- **Environment variables**: Sensitive configuration stored securely

## 📞 Support & Documentation

### Documentation Resources
- **Swagger UI**: http://localhost:8000/docs (Interactive testing)
- **ReDoc**: http://localhost:8000/redoc (Comprehensive reference)
- **Testing Guide**: [`docs/swagger-ui-guide.md`](docs/swagger-ui-guide.md)
- **Implementation Summary**: [`docs/swagger-ui-summary.md`](docs/swagger-ui-summary.md)

### Troubleshooting
1. **Check health endpoints** for system status
2. **Review server logs** for error details
3. **Test connections** with `debug_connection.py`
4. **Verify environment variables** in `.env` file

### Getting Help
- Review the comprehensive testing guide for common scenarios
- Check the Swagger UI for interactive API exploration
- Use the health endpoints to diagnose system issues
- Examine server logs for detailed error information

---

**Built with**: FastAPI, Mem0, Qdrant, OpenAI, Railway  
**Version**: 1.0.0  
**License**: MIT 