# Qdrant Integration Tests - Testing Guide

## Overview

This guide provides comprehensive information for running and maintaining the **streamlined Qdrant integration test suite**. The test suite contains **4 essential tests** that validate core functionality of the AI Agent Mem0 API with Qdrant vector database integration.

## Quick Start

### Prerequisites
1. **API Server**: Running on `http://localhost:8000`
2. **Environment Variables**: `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_COLLECTION_NAME`
3. **Dependencies**: `pytest`, `pytest-asyncio`, `allure-pytest`, `httpx`

### Basic Execution
```bash
# Quick connectivity test
python quick_test.py

# Run all core tests
python -m pytest test_core_integration.py -v

# Generate Allure report
python -m pytest test_core_integration.py --alluredir=allure-results
allure serve allure-results
```

## Test Suite Structure

### Core Integration Tests (`test_core_integration.py`)

The test suite contains **4 essential tests** organized in a single class:

```python
class TestCoreIntegration:
    async def test_health_check()        # API health verification
    async def test_basic_chat()          # Chat functionality
    async def test_memory_persistence()  # Memory storage/retrieval
    async def test_user_isolation()      # User privacy
```

## Individual Test Details

### 1. Health Check Test

**Purpose**: Verify API is running and responding correctly

**Test Flow**:
1. Send `GET /health` request
2. Verify status code 200
3. Validate response structure
4. Check health status is "healthy"

**Expected Response**:
```json
{
    "status": "healthy",
    "message": "API is running successfully"
}
```

**Execution**:
```bash
python -m pytest test_core_integration.py::TestCoreIntegration::test_health_check -v
```

**Duration**: ~100ms

### 2. Basic Chat Test

**Purpose**: Test core chat functionality and response format

**Test Flow**:
1. Create unique user ID
2. Send chat request about peptides
3. Verify response structure
4. Validate memory creation
5. Check response content

**Expected Behavior**:
- Status code: 200
- Response contains: `response`, `memories_found`, `memories_created`, `user_id`
- First conversation: `memories_found = 0`, `memories_created >= 1`
- Response is non-empty string

**Execution**:
```bash
python -m pytest test_core_integration.py::TestCoreIntegration::test_basic_chat -v
```

**Duration**: ~3-5 seconds

### 3. Memory Persistence Test

**Purpose**: Verify memory storage and retrieval across conversations

**Test Flow**:
1. **First Conversation**: Ask about BPC-157 for recovery
   - Verify memory creation
   - No previous memories found
2. **Wait**: 2 seconds for memory storage
3. **Second Conversation**: Ask about dosage for "what we discussed"
   - Verify memory retrieval
   - Check context awareness in response

**Expected Behavior**:
- First conversation creates memory
- Second conversation finds previous memory
- Response references previous context (BPC-157, recovery, dosage)

**Execution**:
```bash
python -m pytest test_core_integration.py::TestCoreIntegration::test_memory_persistence -v
```

**Duration**: ~8-10 seconds

### 4. User Isolation Test

**Purpose**: Ensure users cannot access each other's memories

**Test Flow**:
1. **User 1**: Conversation about TB-500 for healing
2. **User 2**: Conversation about Ipamorelin for growth hormone
3. **Wait**: 2 seconds for memory storage
4. **User 1 Follow-up**: Ask about "the healing peptide we discussed"
5. **Verify Isolation**: User 1 only accesses their own memories

**Expected Behavior**:
- Each user creates their own memories
- User 1 follow-up finds their own memories
- User 1 response references TB-500, not Ipamorelin
- No cross-user memory access

**Execution**:
```bash
python -m pytest test_core_integration.py::TestCoreIntegration::test_user_isolation -v
```

**Duration**: ~12-15 seconds

## Test Execution Options

### By Test Category
```bash
# Health tests only
python -m pytest -m health -v

# Chat functionality tests
python -m pytest -m chat -v

# Memory-related tests
python -m pytest -m memory -v

# All integration tests
python -m pytest -m integration -v
```

### With Different Output Formats
```bash
# Verbose output
python -m pytest test_core_integration.py -v

# Short output
python -m pytest test_core_integration.py -q

# Show local variables on failure
python -m pytest test_core_integration.py -l

# Stop on first failure
python -m pytest test_core_integration.py -x
```

### With Allure Reporting
```bash
# Generate results
python -m pytest test_core_integration.py --alluredir=allure-results

# Serve interactive report
allure serve allure-results

# Generate static report
allure generate allure-results -o allure-report --clean
```

## Quick Connectivity Test

### Purpose
The `quick_test.py` provides fast validation that the API is accessible before running the full test suite.

### Features
- Basic health check
- Detailed health check
- Simple chat request
- Connection error handling
- Timeout detection

### Execution
```bash
# Standalone execution
python quick_test.py

# With pytest
python -m pytest quick_test.py -v
```

### Expected Output
```
🚀 Quick Test for Qdrant Integration API
==================================================
🔍 Testing API connectivity...
  ➤ Testing basic health check...
  ✅ Basic health check: PASSED
     Status: healthy
  ➤ Testing detailed health check...
  ✅ Detailed health check: PASSED
     mem0: ✅ initialized
     qdrant: ✅ connected
     openai: ✅ available
  ➤ Testing simple chat request...
  ✅ Chat request: PASSED
     Response length: 150 characters
     Memories created: 1
==================================================
✅ Quick test PASSED - API is ready for testing
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Connection Errors
```
httpx.ConnectError: All connection attempts failed
```

**Cause**: API server not running or not accessible

**Solutions**:
- Start the API server: `uvicorn app.main:app --reload`
- Check if server is running on `http://localhost:8000`
- Verify no firewall blocking the connection
- Check if port 8000 is available

#### 2. Memory Tests Failing
```
AssertionError: Expected at least 1 memory found, got 0
```

**Cause**: Qdrant database connection issues

**Solutions**:
- Verify `QDRANT_URL` environment variable
- Check Qdrant server is running and accessible
- Verify `QDRANT_COLLECTION_NAME` is correct
- Check Qdrant logs for connection errors

#### 3. Chat Tests Failing
```
AssertionError: Response missing required field: 'response'
```

**Cause**: OpenAI API issues

**Solutions**:
- Verify `OPENAI_API_KEY` environment variable is set
- Check OpenAI API key is valid and has credits
- Verify internet connection for OpenAI API access
- Check API rate limits

#### 4. Async Warnings
```
PytestDeprecationWarning: asyncio_default_fixture_loop_scope is unset
```

**Cause**: pytest-asyncio configuration warning

**Solution**: This is a warning only, tests still work correctly. Can be ignored.

#### 5. Import Errors
```
ModuleNotFoundError: No module named 'app.core.config'
```

**Cause**: Python path not set correctly

**Solutions**:
- Run tests from the correct directory
- Verify project structure is correct
- Check `conftest.py` has proper path setup

## Performance Expectations

### Expected Test Times
| Test | Expected Duration | Acceptable Range |
|------|------------------|------------------|
| Health Check | ~100ms | < 500ms |
| Basic Chat | ~3-5s | < 8s |
| Memory Persistence | ~8-10s | < 15s |
| User Isolation | ~12-15s | < 20s |
| **Total Suite** | **~25s** | **< 45s** |

### Performance Monitoring
The tests include performance tracking and will fail if response times exceed acceptable thresholds:

- Health checks: Must respond within 500ms
- Chat requests: Must respond within 8-15 seconds depending on complexity
- Memory operations: Must complete within expected timeframes

## Environment Configuration

### Required Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration  
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=mem0_collection

# Optional Configuration
ENVIRONMENT=test
LOG_LEVEL=INFO
```

### Test Configuration
The tests use these default settings:
- **Base URL**: `http://localhost:8000`
- **Timeout**: 30 seconds
- **Async Mode**: Auto
- **Fixture Scope**: Function (for isolation)

## Allure Reporting Features

### Report Contents
- **Test Steps**: Detailed step-by-step execution
- **Attachments**: Request/response data, performance metrics
- **Categories**: Organized by epic/feature/story
- **Severity Levels**: All tests marked as CRITICAL
- **Environment Info**: API URL, test environment
- **Performance Data**: Response times and metrics

### Report Navigation
- **Overview**: Test execution summary
- **Categories**: Tests organized by functionality
- **Suites**: Test file organization
- **Graphs**: Performance and trend analysis
- **Timeline**: Execution timeline view

### Generating Reports
```bash
# Generate and serve immediately
python -m pytest test_core_integration.py --alluredir=allure-results
allure serve allure-results

# Generate static report for sharing
allure generate allure-results -o allure-report --clean
```

## Best Practices

### Running Tests
1. **Always run quick test first** to verify connectivity
2. **Use verbose mode** (`-v`) for detailed output
3. **Generate Allure reports** for comprehensive analysis
4. **Run tests in isolation** to avoid interference

### Debugging Failures
1. **Check logs** in the API server console
2. **Use Allure attachments** to see request/response data
3. **Run individual tests** to isolate issues
4. **Verify environment variables** are set correctly

### Maintenance
1. **Update performance thresholds** as system improves
2. **Review test data** for relevance and accuracy
3. **Monitor test execution times** for performance regression
4. **Keep documentation updated** with any changes

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          uv pip install pytest pytest-asyncio allure-pytest httpx
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          QDRANT_URL: ${{ secrets.QDRANT_URL }}
        run: |
          python -m pytest test_core_integration.py --alluredir=allure-results
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: allure-results
          path: allure-results
```

## Conclusion

This streamlined test suite provides essential validation of the AI Agent Mem0 API with Qdrant integration while maintaining:

- ✅ **Fast execution** (~25 seconds total)
- ✅ **Essential coverage** (4 critical tests)
- ✅ **High reliability** (no flaky tests)
- ✅ **Clear diagnostics** (detailed error messages)
- ✅ **Comprehensive reporting** (Allure integration)

The focus on **quality over quantity** ensures that the most important functionality is thoroughly tested while maintaining efficiency and maintainability. 