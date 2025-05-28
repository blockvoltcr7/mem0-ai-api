# AI Agent Mem0 API Documentation

## Overview

The AI Agent Mem0 API provides conversational AI capabilities with persistent memory using Mem0 and Qdrant vector database. This API enables AI agents to maintain context across conversations and provide personalized responses based on user history.

## Features

- **Persistent Memory**: Conversations are stored and retrieved using Mem0 + Qdrant
- **User-based Context**: Each user has their own memory space
- **Session Grouping**: Optional session IDs for organizing conversations
- **Metadata Support**: Rich metadata for memory filtering and context
- **Health Monitoring**: Comprehensive health checks for all system components
- **Error Handling**: Detailed error responses with suggestions

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required for this MVP API.

## Endpoints

### Chat Endpoint

#### POST `/chat`

Send a message to the AI agent and receive a contextual response.

**Request Body:**
```json
{
  "user_id": "string",
  "message": "string",
  "session_id": "string (optional)",
  "metadata": {
    "key": "value"
  }
}
```

**Response:**
```json
{
  "response": "string",
  "memories_found": 0,
  "memories_created": 1,
  "user_id": "string",
  "response_time_ms": 1250
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "I am interested in learning about BPC-157 peptide for healing.",
    "metadata": {
      "domain": "peptide_coaching",
      "location": "SF",
      "urgency": "normal"
    }
  }'
```

**Example Response:**
```json
{
  "response": "BPC-157 is a peptide that has shown promising results for healing and tissue repair. However, it's important to note that it's not FDA-approved for human use and should only be considered under medical supervision. What specific aspect of BPC-157 are you most interested in learning about?",
  "memories_found": 0,
  "memories_created": 1,
  "user_id": "user123",
  "response_time_ms": 1250
}
```

### Health Endpoints

#### GET `/health`

Basic health check for simple monitoring.

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Agent API is running successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### GET `/health/detailed`

Detailed health check with component status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "mem0": {"status": "initialized"},
    "qdrant": {"status": "connected", "collection": "peptide_health_coaching_memories"},
    "openai": {"status": "available"}
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Request/Response Models

### ChatRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user_id | string | Yes | Unique user identifier (1-100 chars) |
| message | string | Yes | User's message (1-5000 chars) |
| session_id | string | No | Optional session identifier |
| metadata | object | No | Optional metadata for memory context |

### ChatResponse

| Field | Type | Description |
|-------|------|-------------|
| response | string | AI assistant's response |
| memories_found | integer | Number of relevant memories retrieved |
| memories_created | integer | Number of new memories created |
| user_id | string | User identifier |
| response_time_ms | integer | Response time in milliseconds |

## Error Handling

The API returns structured error responses with helpful information:

```json
{
  "detail": {
    "error_code": "invalid_user_id",
    "message": "user_id is required and cannot be empty",
    "suggestions": ["Provide a valid user_id in the request"]
  }
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| invalid_user_id | 400 | User ID is missing or empty |
| invalid_message | 400 | Message is missing or empty |
| internal_error | 500 | Unexpected server error |

## Memory System

### User Identification

- Each user is identified by a unique `user_id`
- Users are automatically created when they first interact with the API
- No explicit user registration is required

### Memory Storage

- Conversations are automatically stored in the Qdrant collection
- Memories include both user messages and AI responses
- Metadata is stored alongside memories for enhanced context

### Memory Retrieval

- Relevant memories are retrieved based on semantic similarity
- Search is limited to the specified user's memories
- Number of retrieved memories is configurable (default: 5)

### Session Grouping

- Optional `session_id` can be used to group related conversations
- Sessions help organize memories by context (e.g., consultation sessions)
- Session metadata is automatically included in memory storage

## Configuration

The API is configured via environment variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url

# Optional
QDRANT_PORT=6333
QDRANT_USE_HTTPS=true
MEM0_COLLECTION_NAME=peptide_health_coaching_memories
AI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000
MEMORY_SEARCH_LIMIT=5
```

## Running the API

1. **Install Dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

3. **Start the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite with Allure reporting:

```bash
# Run tests
pytest tests/test_ai_agent_api.py --alluredir=allure-results

# Generate report
allure serve allure-results
```

## Performance Considerations

- **Response Time**: Typical responses are under 2 seconds
- **Memory Limit**: Search is limited to 5 most relevant memories by default
- **Concurrent Users**: API supports multiple concurrent users
- **Rate Limiting**: No rate limiting implemented in MVP

## Limitations

- No authentication/authorization
- No rate limiting
- Single collection for all users
- No conversation history endpoint
- No memory deletion capabilities

## Future Enhancements

- User authentication and authorization
- Rate limiting and usage quotas
- Multiple collections for different domains
- Conversation history retrieval
- Memory management (edit/delete)
- Real-time streaming responses
- Analytics and usage metrics 