# AI Agent Mem0 API Implementation

**Task Type:** Epic  
**Priority:** High  
**Story Points:** 13  
**Sprint:** Current Sprint  
**Assignee:** Development Team  
**Reporter:** Product Owner  

## **Summary**
Implement a FastAPI-based AI agent API that integrates Mem0 with Qdrant vector store for persistent memory management in peptide health coaching conversations.

## **Description**

### **Background**
We have successfully implemented Mem0 + Qdrant integration in CLI format (`scripts/interactive_mem0_qdrant_cli.py`) and comprehensive test coverage (`tests/integration_mem0/`). Now we need to expose this functionality as a production-ready REST API for external AI agents and applications.

### **Business Value**
- Enable external applications to leverage our AI agent with persistent memory
- Provide scalable API for peptide health coaching conversations
- Create foundation for future AI agent integrations
- Demonstrate production-ready Mem0 + Qdrant implementation

### **Technical Context**
- Existing FastAPI app structure in `/app` directory
- Proven Mem0 + Qdrant integration patterns from CLI and tests
- Single collection approach: `peptide_health_coaching_memories`
- OpenAI GPT-4o-mini for AI responses

## **Requirements**

### **Functional Requirements**
1. **Single Chat Endpoint**: Implement `/api/v1/chat` endpoint that mirrors CLI functionality
2. **User Management**: Auto-create users if they don't exist in the collection
3. **Memory Integration**: Search and store memories using Mem0 + Qdrant
4. **Context-Aware Responses**: Generate AI responses using retrieved memory context
5. **Collection Management**: Ensure collection exists on startup
6. **Health Monitoring**: Enhanced health endpoint with Mem0/Qdrant status

### **Non-Functional Requirements**
1. **Performance**: Sub-2 second response times for chat endpoint
2. **Scalability**: Handle multiple concurrent users
3. **Reliability**: Graceful error handling and recovery
4. **Maintainability**: Follow existing app structure and patterns
5. **Security**: Basic API key authentication
6. **Observability**: Comprehensive logging and monitoring

## **Technical Specifications**

### **API Endpoints**

#### **Chat Endpoint**
```http
POST /api/v1/chat
Content-Type: application/json
Authorization: Bearer {api_key}

{
    "user_id": "string",           # Required - unique user identifier
    "message": "string",           # Required - user's message
    "session_id": "string",        # Optional - for session-based memory
    "metadata": {                  # Optional - structured data for filtering
        "domain": "peptide_coaching",
        "location": "SF",
        "timestamp": "2024-01-15",
        "urgency": "normal"
    }
}
```

**Response:**
```json
{
    "response": "AI assistant's response",
    "memories_found": 3,
    "memories_created": 1,
    "user_id": "user123",
    "response_time_ms": 1250
}
```

#### **Enhanced Health Endpoint**
```http
GET /api/v1/health/detailed
```

**Response:**
```json
{
    "status": "healthy",
    "services": {
        "qdrant": {"status": "connected", "collection": "peptide_health_coaching_memories"},
        "mem0": {"status": "initialized"},
        "openai": {"status": "available"}
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### **File Structure Implementation**

```
app/
├── main.py                           # Add startup event for Mem0 initialization
├── core/
│   ├── config.py                     # Extend with Mem0/Qdrant settings
│   └── mem0_manager.py               # NEW: Mem0 + Qdrant initialization
├── services/
│   ├── ai_agent_service.py           # NEW: Core AI agent logic (from CLI)
│   ├── memory_service.py             # NEW: Memory operations wrapper
│   └── chat_service.py               # NEW: Chat orchestration service
├── models/
│   └── chat_models.py                # NEW: Pydantic models for chat API
├── api/v1/
│   ├── endpoints/
│   │   ├── chat.py                   # NEW: Main chat endpoint
│   │   └── health.py                 # NEW: Enhanced health checks
│   └── schemas/
│       └── chat_schemas.py           # NEW: Request/Response schemas
└── db/
    └── qdrant_client.py              # NEW: Qdrant client initialization
```

### **Configuration Extensions**

Add to `app/core/config.py`:
```python
# Mem0 & Qdrant settings
qdrant_url: str = ""
qdrant_port: Optional[int] = None
qdrant_use_https: bool = True
mem0_collection_name: str = "peptide_health_coaching_memories"

# AI Agent settings
ai_model: str = "gpt-4o-mini"
ai_temperature: float = 0.7
ai_max_tokens: int = 1000
memory_search_limit: int = 5
```

### **Dependencies**

Add to `requirements.in`:
```
mem0ai
qdrant-client
```

## **Implementation Plan**

### **Phase 1: Core Infrastructure (3 points)**
- [ ] Extend `app/core/config.py` with Mem0/Qdrant settings
- [ ] Create `app/core/mem0_manager.py` (based on test fixtures)
- [ ] Create `app/db/qdrant_client.py` for client initialization
- [ ] Add startup event to `app/main.py` for collection initialization
- [ ] Update dependencies in `requirements.in`

### **Phase 2: Services Layer (5 points)**
- [ ] Create `app/services/ai_agent_service.py` (port CLI logic)
- [ ] Create `app/services/memory_service.py` (Mem0 operations wrapper)
- [ ] Create `app/services/chat_service.py` (orchestration layer)
- [ ] Implement user auto-creation logic
- [ ] Add comprehensive error handling

### **Phase 3: API Layer (3 points)**
- [ ] Create `app/models/chat_models.py` (Pydantic models)
- [ ] Create `app/api/v1/schemas/chat_schemas.py` (request/response schemas)
- [ ] Create `app/api/v1/endpoints/chat.py` (main chat endpoint)
- [ ] Create `app/api/v1/endpoints/health.py` (enhanced health checks)
- [ ] Update API router to include new endpoints

### **Phase 4: Testing & Documentation (2 points)**
- [ ] Create integration tests based on existing test patterns
- [ ] Add API endpoint tests to `tests/test_fastapi_endpoints.py`
- [ ] Update API documentation
- [ ] Performance testing and optimization

## **Acceptance Criteria**

### **Core Functionality**
- [ ] Chat endpoint successfully processes user messages
- [ ] AI responses include context from retrieved memories
- [ ] New conversations are stored as memories in Qdrant
- [ ] Users are auto-created if they don't exist
- [ ] Collection is automatically created on startup if missing

### **Performance**
- [ ] Chat endpoint responds within 2 seconds for typical requests
- [ ] Memory search completes within 500ms
- [ ] API handles 10 concurrent users without degradation

### **Error Handling**
- [ ] Graceful handling of Qdrant connection failures
- [ ] Proper error responses for invalid requests
- [ ] Fallback behavior when Mem0 is unavailable
- [ ] Comprehensive logging for debugging

### **Integration**
- [ ] Follows existing FastAPI app structure
- [ ] Maintains consistency with current code patterns
- [ ] Integrates with existing configuration system
- [ ] Compatible with current testing framework

### **Testing**
- [ ] All new endpoints have corresponding tests
- [ ] Integration tests cover Mem0 + Qdrant functionality
- [ ] Tests follow existing Allure reporting patterns
- [ ] Minimum 80% code coverage for new components

## **Technical Risks & Mitigations**

### **Risk 1: Qdrant Connection Issues**
- **Mitigation**: Implement connection retry logic and health checks
- **Fallback**: Graceful degradation with error responses

### **Risk 2: Memory Search Performance**
- **Mitigation**: Implement caching and optimize search parameters
- **Monitoring**: Add performance metrics and alerting

### **Risk 3: OpenAI API Rate Limits**
- **Mitigation**: Implement exponential backoff and request queuing
- **Monitoring**: Track API usage and implement alerts

## **Definition of Done**

- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Integration tests passing
- [ ] API documentation updated
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Deployed to staging environment
- [ ] Product owner acceptance

## **Dependencies**

### **Blocked By**
- Environment variables configured for Qdrant and OpenAI
- Qdrant instance available and accessible

### **Blocks**
- External AI agent integrations
- Production deployment of AI coaching features

## **Related Tasks**

- **Reference Implementation**: `scripts/interactive_mem0_qdrant_cli.py`
- **Test Patterns**: `tests/integration_mem0/test_peptide_coaching_scenario.py`
- **Existing API Structure**: `app/api/v1/endpoints/hello_world_v1.py`

## **Notes**

### **Implementation Guidelines**
1. **Reuse Existing Patterns**: Leverage successful CLI implementation
2. **Follow Current Structure**: Maintain consistency with existing FastAPI organization
3. **Configuration-Driven**: All settings should be configurable via environment variables
4. **Error Handling**: Implement semantic error responses for AI-friendly debugging
5. **Logging**: Add comprehensive logging for monitoring and debugging

### **Testing Strategy**
- Unit tests for each service component
- Integration tests for Mem0 + Qdrant functionality
- API endpoint tests with various scenarios
- Performance tests for response times
- Error scenario testing

### **Future Enhancements**
- Session management with run_id support
- Advanced metadata filtering
- Batch operations for multiple messages
- Real-time streaming responses
- Analytics and usage metrics
