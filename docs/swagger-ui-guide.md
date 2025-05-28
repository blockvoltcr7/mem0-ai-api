# Swagger UI Testing Guide

## Overview

The AI Agent Mem0 API includes a comprehensive Swagger UI interface for interactive API testing and documentation. This guide will help you effectively use the Swagger UI to test and explore the API endpoints.

## Accessing Swagger UI

### Quick Access
```bash
# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open Swagger UI automatically
python scripts/open_swagger_ui.py
```

### Manual Access
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Interface Overview

The Swagger UI is organized into three main sections:

### 1. **Chat Endpoints** 🧠
- `/api/v1/chat` - Main conversational AI endpoint with persistent memory

### 2. **Health Endpoints** 📊
- `/api/v1/health` - Basic health check for load balancers
- `/api/v1/health/detailed` - Comprehensive system status

### 3. **Hello Endpoints** 👋
- `/` - Root endpoint with API information
- `/health` - Simple health status

## Testing Workflow

### Step 1: Verify System Health
1. **Start with Basic Health Check**
   - Click on the `health` section
   - Try `/health` endpoint first
   - Should return `{"status": "healthy"}`

2. **Check Detailed Health Status**
   - Try `/api/v1/health/detailed` endpoint
   - Verify all services show as "connected" or "initialized"
   - Check Qdrant, Mem0, and OpenAI status

### Step 2: Test Chat Functionality

#### First Conversation
```json
{
  "user_id": "test_user_001",
  "message": "Hello! I'm interested in learning about BPC-157 peptide.",
  "session_id": "test_session_2024",
  "metadata": {
    "domain": "peptide_coaching",
    "context": "initial_consultation"
  }
}
```

#### Follow-up Conversation
```json
{
  "user_id": "test_user_001",
  "message": "What are the potential side effects?",
  "session_id": "test_session_2024",
  "metadata": {
    "domain": "peptide_coaching",
    "context": "safety_inquiry"
  }
}
```

### Step 3: Verify Memory Persistence
- Use the same `user_id` in multiple requests
- Check `memories_found` in responses (should increase)
- Verify AI responses reference previous conversations

## Example Test Scenarios

### Scenario 1: New User Onboarding
```json
{
  "user_id": "new_user_123",
  "message": "I'm new to peptides. Can you help me understand the basics?",
  "metadata": {
    "experience_level": "beginner",
    "goals": ["education", "safety"]
  }
}
```

### Scenario 2: Experienced User Consultation
```json
{
  "user_id": "experienced_user_456",
  "message": "I've been using TB-500 for 3 months. What should I consider for my next cycle?",
  "session_id": "cycle_planning_2024",
  "metadata": {
    "experience_level": "advanced",
    "current_protocol": "TB-500",
    "duration": "3_months"
  }
}
```

### Scenario 3: Multi-Session Tracking
```json
{
  "user_id": "client_789",
  "message": "Following up on our discussion about recovery protocols.",
  "session_id": "follow_up_consultation",
  "metadata": {
    "consultation_type": "follow_up",
    "previous_session": "initial_consultation"
  }
}
```

## Understanding Responses

### Response Structure
```json
{
  "response": "AI-generated response text",
  "memories_found": 2,        // Number of relevant memories retrieved
  "memories_created": 1,      // New memories created from this conversation
  "user_id": "test_user_001",
  "session_id": "test_session_2024",
  "metadata": {
    "model_used": "gpt-4",
    "response_time_ms": 1250,
    "memory_retrieval_time_ms": 45
  }
}
```

### Key Metrics to Monitor
- **memories_found**: Should increase as you have more conversations
- **memories_created**: Usually 1 per conversation
- **response_time_ms**: Typical range 1000-3000ms
- **memory_retrieval_time_ms**: Should be under 100ms

## Error Testing

### Test Invalid Requests
1. **Empty user_id**
   ```json
   {
     "user_id": "",
     "message": "Test message"
   }
   ```

2. **Empty message**
   ```json
   {
     "user_id": "test_user",
     "message": ""
   }
   ```

3. **Missing required fields**
   ```json
   {
     "message": "Test without user_id"
   }
   ```

### Expected Error Responses
```json
{
  "detail": {
    "error_code": "invalid_user_id",
    "message": "user_id is required and cannot be empty",
    "suggestions": ["Provide a valid user_id in the request"]
  }
}
```

## Advanced Features

### Using Metadata for Context
```json
{
  "metadata": {
    "domain": "peptide_coaching",
    "consultation_type": "initial",
    "medical_history": "previous_injuries",
    "goals": ["recovery", "performance"],
    "experience_level": "intermediate"
  }
}
```

### Session Management
- Use consistent `session_id` for related conversations
- Different sessions can have different contexts
- Sessions help organize memory retrieval

### Memory Filtering
- Metadata helps filter relevant memories
- Domain-specific context improves responses
- User preferences persist across sessions

## Troubleshooting

### Common Issues

1. **Server Not Running**
   ```bash
   # Start the server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Health Check Fails**
   - Check environment variables in `.env`
   - Verify Qdrant and OpenAI connections
   - Review server logs for errors

3. **Slow Responses**
   - Check `response_time_ms` in responses
   - Monitor `memory_retrieval_time_ms`
   - Verify network connectivity

4. **Memory Not Persisting**
   - Ensure consistent `user_id`
   - Check `memories_created` > 0
   - Verify Qdrant collection exists

### Debug Commands
```bash
# Check server status
curl http://localhost:8000/health

# Get detailed health info
curl http://localhost:8000/api/v1/health/detailed

# Test connection components
python debug_connection.py
```

## Best Practices

### For Testing
1. **Use descriptive user_ids**: `test_user_peptides_001`
2. **Include relevant metadata**: Domain, context, goals
3. **Test memory persistence**: Multiple conversations with same user
4. **Verify error handling**: Test invalid inputs
5. **Monitor performance**: Check response times

### For Development
1. **Document test scenarios**: Save successful test cases
2. **Use consistent data**: Standardize test user profiles
3. **Test edge cases**: Empty fields, long messages, special characters
4. **Validate responses**: Check all response fields
5. **Monitor logs**: Watch server output for errors

## Integration Testing

### Automated Testing
```bash
# Run the comprehensive test suite
python scripts/test_ai_agent_api.py

# Run pytest with Allure reporting
pytest tests/test_ai_agent_api.py --alluredir=allure-results
```

### Manual Testing Checklist
- [ ] Health endpoints respond correctly
- [ ] Chat endpoint accepts valid requests
- [ ] Memory persistence works across conversations
- [ ] Error handling for invalid inputs
- [ ] Response times are acceptable
- [ ] All required fields are present in responses
- [ ] Metadata is properly processed

## Support

For issues or questions:
1. Check the server logs for error details
2. Verify environment configuration
3. Test individual components with `debug_connection.py`
4. Review the API documentation in Swagger UI
5. Contact the development team for persistent issues 