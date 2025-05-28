# Qdrant Integration Tests

Essential integration tests for the AI Agent Mem0 API with Qdrant vector database integration.

## Overview

This test suite contains **4 core integration tests** that verify the essential functionality of the AI Agent Mem0 API with Qdrant vector database. The tests are designed to be fast, reliable, and focused on critical business logic.

## Test Structure

### Core Tests (`test_core_integration.py`)

1. **Health Check** - Verifies API is running and responding correctly
2. **Basic Chat** - Tests chat endpoint functionality and response format
3. **Memory Persistence** - Validates memory storage and retrieval across conversations
4. **User Isolation** - Ensures users cannot access each other's memories

### Quick Test (`quick_test.py`)

A standalone connectivity test that can be run independently to verify the API is accessible before running the full test suite.

## Prerequisites

1. **API Server Running**: The API must be running on `http://localhost:8000`
2. **Environment Variables**:
   - `OPENAI_API_KEY` - OpenAI API key for chat functionality
   - `QDRANT_URL` - Qdrant database URL
   - `QDRANT_COLLECTION_NAME` - Collection name for memory storage

3. **Dependencies**:
   ```bash
   uv pip install pytest pytest-asyncio allure-pytest httpx
   ```

## Running Tests

### Quick Connectivity Test
```bash
# Test API connectivity
python quick_test.py

# Or with pytest
python -m pytest quick_test.py -v
```

### Core Integration Tests
```bash
# Run all core tests
python -m pytest test_core_integration.py -v

# Run specific test
python -m pytest test_core_integration.py::TestCoreIntegration::test_health_check -v

# Run with Allure reporting
python -m pytest test_core_integration.py --alluredir=allure-results
allure serve allure-results
```

### Test Categories
```bash
# Run by category
python -m pytest -m health -v          # Health check tests
python -m pytest -m chat -v            # Chat functionality tests  
python -m pytest -m memory -v          # Memory persistence tests
python -m pytest -m integration -v     # All integration tests
```

## Test Details

### 1. Health Check Test
- **Purpose**: Verify API is running and healthy
- **Endpoint**: `GET /health`
- **Validates**: Status code 200, response structure, health status
- **Duration**: ~100ms

### 2. Basic Chat Test
- **Purpose**: Test core chat functionality
- **Endpoint**: `POST /api/v1/chat`
- **Validates**: Response format, memory creation, user ID handling
- **Duration**: ~3-5 seconds

### 3. Memory Persistence Test
- **Purpose**: Verify memory storage and retrieval
- **Flow**: First conversation → Wait → Second conversation
- **Validates**: Memory creation, memory retrieval, context awareness
- **Duration**: ~8-10 seconds

### 4. User Isolation Test
- **Purpose**: Ensure user memory privacy
- **Flow**: User1 conversation → User2 conversation → User1 follow-up
- **Validates**: Memory isolation, no cross-user access
- **Duration**: ~12-15 seconds

## Expected Results

When the API is running correctly, all tests should **PASS**:

```
test_core_integration.py::TestCoreIntegration::test_health_check PASSED
test_core_integration.py::TestCoreIntegration::test_basic_chat PASSED  
test_core_integration.py::TestCoreIntegration::test_memory_persistence PASSED
test_core_integration.py::TestCoreIntegration::test_user_isolation PASSED

4 passed in ~25 seconds
```

## Troubleshooting

### Connection Errors
```
httpx.ConnectError: All connection attempts failed
```
**Solution**: Ensure the API server is running on `http://localhost:8000`

### Memory Tests Failing
```
AssertionError: Expected at least 1 memory found, got 0
```
**Solution**: Check Qdrant connection and ensure `QDRANT_URL` is correct

### Chat Tests Failing
```
AssertionError: Response missing required field: 'response'
```
**Solution**: Verify `OPENAI_API_KEY` is set and valid

## Configuration

The tests use these configuration files:

- `conftest.py` - Pytest fixtures and configuration
- `pytest.ini` - Pytest settings and markers
- Test timeout: 30 seconds
- Base URL: `http://localhost:8000`

## Allure Reporting

The tests include comprehensive Allure reporting with:
- Test steps and descriptions
- Request/response attachments
- Performance metrics
- Context analysis
- Error details

Generate reports with:
```bash
python -m pytest --alluredir=allure-results
allure serve allure-results
```

## Architecture

```
tests/qdrant_integration_tests/
├── conftest.py                 # Pytest fixtures
├── test_core_integration.py    # 4 core tests
├── quick_test.py              # Connectivity test
├── pytest.ini                # Pytest configuration
└── README.md                  # This file
```

## Maintenance

This streamlined test suite focuses on:
- ✅ **Essential functionality only**
- ✅ **Fast execution** (~25 seconds total)
- ✅ **High reliability**
- ✅ **Clear failure messages**
- ✅ **Comprehensive reporting**

For additional testing scenarios, consider adding them to the core test file rather than creating new test files to maintain simplicity. 