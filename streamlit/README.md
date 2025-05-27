# Health Coach AI - Streamlit Application

A demonstration Streamlit application showcasing Mem0's memory capabilities for AI health coaching, specifically focused on peptide therapy guidance.

## Features

- 🧠 **Memory-Powered Conversations**: Uses Mem0 with Qdrant vector database for persistent conversation memory
- 🔒 **Simple Authentication**: User-specific sessions with plain text passwords (demo only)
- 📋 **Health Profile Management**: Comprehensive onboarding and profile tracking
- 🧬 **Peptide Therapy Focus**: Specialized knowledge with safety emphasis on BPC-157
- 💬 **Contextual Responses**: AI remembers user health profile and conversation history
- 🎨 **Modern UI/UX**: Beautiful interface with custom CSS styling

## Prerequisites

1. **Environment Variables**: Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_USE_HTTPS=true
   ```

2. **Dependencies**: All required packages are listed in `requirements.txt`

3. **Qdrant Vector Database**: Ensure you have a running Qdrant instance

## Installation

1. **Activate Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit App**:
   ```bash
   streamlit run streamlit/app.py
   ```

2. **Access the Application**:
   - Open your browser to `http://localhost:8501`
   - Use demo credentials:
     - Username: `demo_user`, Password: `demo123`
     - Username: `test_user`, Password: `test123`
     - Username: `admin_user`, Password: `admin123`

## User Journey

### 1. Authentication
- Users log in with username/password
- Session is maintained with secure cookies
- Demo accounts available for testing

### 2. Health Profile Onboarding
New users complete a comprehensive health profile including:
- Peptide usage status
- BPC-157 specific information (dosage, duration)
- Health goals (tissue repair, injury recovery, etc.)
- Medical conditions
- Current medications

### 3. AI Health Coach Chat
- Context-aware conversations using Mem0 memory
- Personalized responses based on health profile
- Safety-focused guidance with medical supervision emphasis
- Persistent conversation history

### 4. Profile Management
- View health profile summary
- Update profile information
- Session statistics and memory tracking

## Technical Architecture

### Memory System
- **Mem0**: Manages conversation memory and context
- **Qdrant**: Vector database for similarity search
- **OpenAI GPT-4o-mini**: Language model for responses
- **User Isolation**: Memories are isolated per user

### Data Models
- **UserHealth**: Pydantic model for health profile data
- **Session State**: Streamlit session management
- **Authentication**: Secure credential handling

### Security Features
- Plain text passwords (demo/development only)
- Session-based authentication
- Environment variable protection
- User data isolation

## Demo Scenario

The application demonstrates a peptide coaching scenario:

1. **Initial Greeting**: User starts conversation
2. **Information Sharing**: User shares BPC-157 usage details
3. **Memory Storage**: Information stored in Qdrant via Mem0
4. **Context Retrieval**: AI recalls user's peptide information
5. **Personalized Guidance**: Contextual responses with safety emphasis

## Safety and Compliance

- **Medical Disclaimer**: Prominent warnings about FDA approval status
- **Professional Supervision**: Emphasis on medical consultation
- **Educational Purpose**: Clear positioning as educational tool
- **Safety First**: Prioritizes user safety in all responses

## File Structure

```
streamlit/
├── app.py                 # Main Streamlit application
├── config.yaml           # Authentication configuration
├── generate_passwords.py  # Password hash generation utility
└── README.md             # This file
```

## Configuration

### Authentication
- Users defined in `config.yaml`
- Plain text passwords for demo purposes
- Simple session management

### Memory Configuration
- Collection name: `health_coach_memories`
- Embedding dimensions: 1536 (OpenAI default)
- Vector storage: Qdrant with HTTPS support

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   uv pip install streamlit mem0 qdrant-client
   ```

2. **Authentication Issues**: Verify config.yaml has correct user credentials

3. **Memory System Errors**: Check environment variables and Qdrant connection
   ```bash
   # Test Qdrant connection
   curl https://your-qdrant-url/collections
   ```

4. **OpenAI API Issues**: Verify API key is valid and has sufficient credits

### Environment Variables
Ensure these are set in your `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: Your Qdrant instance URL
- `QDRANT_USE_HTTPS`: Set to "true" for HTTPS connections

## Development

### Adding New Users
1. Update `config.yaml` with new user credentials:
   ```yaml
   credentials:
     usernames:
       new_user:
         email: new@example.com
         name: New User
         password: newpassword123
   ```
2. Restart the application

### Customizing Health Profile
Modify the `UserHealth` Pydantic model in `app.py` to add new fields or validation rules.

### Extending Memory System
The memory system can be extended to support additional context types or search strategies by modifying the `generate_ai_response` function.

## Testing

The application integrates with the existing test suite in `tests/integration_mem0/` for:
- Memory persistence testing
- User isolation verification
- Conversation context validation
- Authentication flow testing

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main project documentation
3. Examine the test files for usage examples
4. Check environment variable configuration 