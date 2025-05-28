# Health Coach AI: Streamlit Application with Mem0 Integration

## Overview
Create a Streamlit-based health coaching application that demonstrates the power of Mem0 for maintaining conversational context and user history. The application will focus on peptide therapy coaching, specifically around BPC-157 usage, while emphasizing medical supervision and safety.

## Core Features

### 1. User Authentication
- Implement secure user authentication using `streamlit-authenticator`
- Store user credentials in a YAML configuration file
- Support user sessions with cookie-based authentication
- Implement logout functionality

### 2. Health Profile Onboarding
Create an onboarding flow that collects essential health information:
- Peptide usage status
- BPC-157 specific information:
  - Current usage
  - Dosage
  - Duration of use
- Health goals (multi-select)
- Medical conditions
- Current medications
- Store completion status and timestamp

### 3. Memory-Powered Chat Interface
Implement a chat interface that:
- Uses Mem0 for conversation memory
- Stores chat history per user
- Retrieves relevant context from previous conversations
- Maintains user-specific health profile context

## Technical Requirements

### Environment Setup
- Required environment variables:
  - `OPENAI_API_KEY`
  - `QDRANT_URL`
  - `QDRANT_USE_HTTPS`

### Dependencies
Core dependencies:
```
streamlit
openai
mem0
qdrant-client
python-dotenv
streamlit-authenticator
pydantic>=2.0.0
```

### Data Models
- UserHealth (Pydantic model):
  - peptide_usage: Optional[bool]
  - bpc157_usage: Optional[bool]
  - bpc157_dosage: Optional[str]
  - bpc157_duration: Optional[str]
  - health_goals: List[str]
  - medical_conditions: List[str]
  - current_medications: List[str]
  - onboarding_completed: bool
  - onboarding_date: Optional[datetime]

## User Journey

1. **Authentication**
   - User arrives at the application
   - Logs in with username/password
   - Session is maintained across visits

2. **First-Time Experience**
   - New users directed to onboarding flow
   - Complete health profile questionnaire
   - Profile information stored for future context

3. **Chat Interface**
   - Access to AI health coach
   - Context-aware responses based on:
     - Health profile
     - Previous conversations
     - Current query

4. **Session Persistence**
   - Conversations stored in Qdrant via Mem0
   - User can return later and continue conversations
   - AI maintains context of previous discussions

## Implementation Guidelines

### Memory System
- Initialize Mem0 with Qdrant backend
- Use username as unique identifier
- Store both chat history and health profile
- Implement efficient memory search and retrieval

### Chat System
- Use OpenAI's GPT-4o-mini model
- Include health profile in system context
- Retrieve relevant memories for each query
- Store new conversations after each interaction

### Security Considerations
- Secure storage of credentials
- Protection of health information
- Safe handling of API keys
- Session management best practices

## Testing Requirements

1. **Authentication Tests**
   - Login functionality
   - Session management
   - Logout process

2. **Onboarding Tests**
   - Form validation
   - Data storage
   - Profile updates

3. **Memory Tests**
   - Context retrieval
   - User isolation
   - Conversation persistence

4. **Chat Tests**
   - Response generation
   - Context integration
   - Memory utilization

## Future Enhancements
- Support for additional peptides
- Integration with health tracking devices
- Export of conversation history
- Customizable AI coaching styles
- Progress tracking and reporting
