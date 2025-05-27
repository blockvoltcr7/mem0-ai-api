# End-to-End Tests for Mem0

This directory contains end-to-end tests that validate the complete Mem0 conversation flow and memory functionality.

## Test Files

### `test_mem0_conversation_flow.py`

This comprehensive e2e test replicates the manual CLI test flow from `tests/integration_mem0/test_mem0_cli.py` to verify that Mem0 memory functionality works correctly in an automated testing environment.

#### Test Coverage

The test suite includes the following test scenarios:

1. **Initial Conversation Without Memory** (`test_initial_conversation`)
   - Tests the first conversation with no existing memory context
   - Verifies response generation and timing metrics
   - Confirms no memories are found for initial conversation

2. **Memory Context Retrieval** (`test_memory_context_question`)
   - Tests asking about previous conversation
   - Verifies the system handles memory context questions appropriately

3. **User Preference Storage** (`test_store_user_preferences`)
   - Tests storing user food preferences in memory
   - Replicates the manual test: "i like all kinds of cheese except cow milk cheese, i only like sheep or goat cheese"
   - Verifies the AI acknowledges and responds appropriately to preferences

4. **Memory Retrieval and Context Usage** (`test_retrieve_user_preferences`)
   - Tests retrieving stored user preferences from memory
   - Replicates the manual test: "what are my food preferences?"
   - Verifies the AI can recall and use stored preferences in responses

5. **Memory Search Functionality** (`test_memory_search`)
   - Tests direct memory search with various queries
   - Validates search results structure and content

6. **Session Statistics** (`test_session_statistics`)
   - Tests session statistics functionality
   - Verifies conversation counting and timing metrics

7. **Multi-User Memory Isolation** (`test_user_memory_isolation`)
   - Tests that memories are properly isolated between different users
   - Stores different preferences for different users
   - Verifies each user gets their own context

8. **Error Handling and Recovery** (`test_error_handling`)
   - Tests system behavior with edge cases (empty messages, long messages, emojis)
   - Verifies graceful error handling

#### Manual Test Flow Replication

The automated test replicates this exact manual CLI test flow:

```
💬 You: hi
🤖 AI: Hello! How can I assist you today?

💬 You: what did i just say?
🤖 AI: I'm not able to hear or recall past conversations...

💬 You: i like all kinds of cheese except cow milk cheese, i only like sheep or goat cheese
🤖 AI: That's great! Sheep and goat cheeses offer a wide variety of flavors...

💬 You: what are my food preferences?
🤖 AI: You like all kinds of cheese except cow milk cheese; you prefer sheep or goat cheese instead.
```

#### Key Features

- **In-Memory Storage**: Uses in-memory vector storage for simplicity (no external database required)
- **Comprehensive Logging**: Includes detailed Allure reporting with attachments
- **Performance Metrics**: Tracks timing for memory search, response generation, and storage
- **Error Handling**: Tests edge cases and error scenarios
- **User Isolation**: Verifies memory isolation between different users

#### Running the Tests

```bash
# Run the e2e test with Allure reporting
cd tests/e2e
pytest test_mem0_conversation_flow.py -v --alluredir=../../allure-results

# Generate and view the Allure report
cd ../../
allure serve allure-results
```

#### Test Configuration

The test uses the following configuration:
- **Model**: `gpt-4o-mini` (same as manual test)
- **Storage**: In-memory vector storage
- **Temperature**: 0.7 (balanced creativity vs consistency)
- **Max Tokens**: 1000 (reasonable response length)

#### Allure Reporting

The test includes comprehensive Allure reporting with:
- **Epic**: End-to-End Testing
- **Feature**: Mem0 Conversation Flow
- **Stories**: Individual test scenarios
- **Attachments**: Conversation logs, performance metrics, memory details
- **Severity Levels**: Critical, Normal, Minor based on test importance

#### Dependencies

- `pytest`: Test framework
- `allure-pytest`: Allure reporting integration
- `mem0`: Memory management library
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

#### Environment Requirements

- `OPENAI_API_KEY`: Required environment variable for OpenAI API access
- Python 3.8+ with required dependencies installed

This automated test ensures that the Mem0 memory functionality works consistently and can be validated as part of a CI/CD pipeline, providing the same verification as the manual CLI test but in a repeatable, automated format. 