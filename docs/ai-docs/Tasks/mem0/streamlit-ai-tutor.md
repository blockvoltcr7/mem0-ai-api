# AI Prompt Engineering Tutor: Streamlit Application with Mem0 Memory Testing

## Overview
Create a Streamlit-based AI prompt engineering tutor application specifically designed for the health domain. The application will demonstrate Mem0's ability to maintain separate conversational contexts for multiple users, using phone number and username as unique identifiers. The focus is on teaching healthcare professionals how to craft effective prompts for AI health coaching applications.

## Core Features

### 1. User Identification (No Authentication)
- Simple user input form collecting:
  - Username (text input)
  - Phone number (text input with validation)
- No password or authentication required
- Combine username + phone number as unique user identifier
- Store user info in session state for navigation

### 2. Memory Isolation Testing
- Use combined identifier (username_phonenumber) for Mem0 user isolation
- Test that conversations remain separate between different users
- Verify that AI remembers previous conversations for returning users
- Demonstrate context persistence across sessions

### 3. AI Prompt Engineering Chat Interface
- Specialized AI tutor focused on health domain prompt engineering
- Teaches best practices for:
  - Health coaching prompts
  - Medical AI safety considerations
  - Prompt structure and optimization
  - Domain-specific prompt techniques
- Uses conversation history to build on previous learning

## Technical Requirements

### Environment Setup
Required environment variables:
```
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_USE_HTTPS=true_or_false
```

### Dependencies
Core dependencies for requirements.in:
```
streamlit
openai
mem0ai
qdrant-client
python-dotenv
pydantic>=2.0.0
phonenumbers
```

### Data Models
```python
from pydantic import BaseModel, Field
from typing import Optional
import phonenumbers

class UserIdentification(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    phone_number: str = Field(min_length=10)
    user_id: str = Field(default="")
    
    def model_post_init(self, __context):
        # Create unique identifier
        self.user_id = f"{self.username}_{self.phone_number.replace('+', '').replace('-', '').replace(' ', '')}"
```

## System Prompt Design

The AI tutor should use this system prompt:

```
You are an expert AI Prompt Engineering Tutor specializing in the healthcare domain. Your mission is to teach healthcare professionals, AI developers, and health coaches how to craft high-quality, effective prompts for AI health coaching applications.

Your expertise covers:
- Best practices for health-focused AI prompting
- Safety considerations in medical AI applications
- Prompt structure optimization for health coaching
- Domain-specific techniques for healthcare AI
- Ethical considerations in health AI interactions
- Regulatory compliance awareness in health AI

Your teaching approach:
- Provide practical, actionable advice
- Use real-world healthcare examples
- Emphasize safety and ethical considerations
- Build on previous conversations and learning progress
- Adapt explanations to the user's experience level
- Encourage hands-on practice with prompt crafting

Remember: You're helping create better AI health coaches through improved prompt engineering. Always prioritize patient safety and ethical AI practices in your guidance.
```

## User Journey

### 1. User Identification Flow
```
Landing Page → User Input Form → Validation → Chat Interface
```

**User Input Page:**
- Clean, simple form with two fields
- Phone number validation using phonenumbers library
- Username validation (alphanumeric, 2-50 characters)
- Submit button navigates to chat interface

### 2. Chat Interface Flow
```
Chat Page → Memory Retrieval → AI Response → Memory Storage → Continue Chat
```

**Chat Experience:**
- Welcome message acknowledging returning/new user
- Context-aware responses based on conversation history
- Focus on prompt engineering education
- Persistent memory across sessions

## Implementation Structure

### File Organization
```
streamlit_ai_tutor/
├── app.py                 # Main Streamlit application
├── models/
│   └── user_models.py     # Pydantic models
├── services/
│   ├── memory_service.py  # Mem0 integration
│   └── ai_service.py      # OpenAI integration
├── pages/
│   ├── user_input.py      # User identification page
│   └── chat.py            # Chat interface page
├── utils/
│   └── validation.py      # Input validation utilities
├── config/
│   └── settings.py        # Configuration management
└── requirements.in        # Dependencies
```

### Key Components

#### 1. Memory Service
```python
class MemoryService:
    def __init__(self):
        self.client = MemoryClient()
    
    def get_user_context(self, user_id: str) -> str:
        """Retrieve conversation history for user"""
        
    def store_conversation(self, user_id: str, message: str, response: str):
        """Store new conversation turn"""
        
    def get_user_summary(self, user_id: str) -> str:
        """Get learning progress summary"""
```

#### 2. AI Service
```python
class AITutorService:
    def __init__(self):
        self.client = OpenAI()
        self.system_prompt = HEALTH_PROMPT_TUTOR_PROMPT
    
    def generate_response(self, user_message: str, context: str) -> str:
        """Generate tutor response with context"""
```

## Testing Strategy

### 1. Memory Isolation Tests
- Create multiple test users with different identifiers
- Verify conversations remain separate
- Test context retrieval accuracy
- Validate user identification logic

### 2. User Experience Tests
- Form validation testing
- Navigation flow testing
- Session persistence testing
- Phone number format handling

### 3. AI Tutor Quality Tests
- Prompt engineering advice quality
- Health domain specificity
- Context utilization effectiveness
- Learning progression tracking

## Success Metrics

### Memory System Validation
- [ ] Users can return and continue previous conversations
- [ ] No cross-contamination between user memories
- [ ] Context retrieval improves response relevance
- [ ] Memory storage persists across application restarts

### Educational Effectiveness
- [ ] AI provides relevant prompt engineering advice
- [ ] Responses build on previous learning
- [ ] Health domain focus maintained
- [ ] Safety considerations emphasized

## Development Phases

### Phase 1: Core Infrastructure
1. Set up Streamlit application structure
2. Implement user identification system
3. Integrate Mem0 with Qdrant backend
4. Create basic chat interface

### Phase 2: AI Tutor Implementation
1. Implement system prompt and AI service
2. Add context retrieval and storage
3. Test memory isolation with multiple users
4. Refine prompt engineering focus

### Phase 3: Testing and Optimization
1. Comprehensive testing with multiple users
2. Memory performance optimization
3. UI/UX improvements
4. Documentation and deployment preparation

## Future Enhancements
- Analytics dashboard for learning progress
- Prompt template library
- Interactive prompt building tools
- Integration with health AI frameworks
- Advanced memory search capabilities
- Export conversation summaries
