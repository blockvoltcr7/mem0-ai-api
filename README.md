# FastAPI Allure Pytest Template

This repository provides a quick start template for building APIs with FastAPI, testing with Pytest, and generating beautiful test reports using Allure. The goal is to enable developers to quickly create and deploy APIs to platforms like Render or Railway.

## 🧠 AI Agent Mem0 API

This template now includes a complete **AI Agent API with persistent memory** using **Mem0** and **Qdrant** vector database. The API provides conversational AI capabilities with memory that persists across sessions.

### Key Features
- 🧠 **Persistent Memory**: Conversations stored and retrieved across sessions
- 👤 **User Isolation**: Each user has their own memory space  
- 🔍 **Context-Aware**: AI responses based on conversation history
- 📊 **Health Monitoring**: Comprehensive system health checks
- 🚀 **High Performance**: Optimized for production use
- 📖 **Interactive Documentation**: Full Swagger UI for testing

### Quick Start
```bash
# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open Swagger UI for testing
python scripts/open_swagger_ui.py
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Example Usage
```bash
# Test the chat endpoint
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Tell me about BPC-157 peptide",
    "metadata": {"domain": "peptide_coaching"}
  }'
```

For detailed testing instructions, see [`docs/swagger-ui-guide.md`](docs/swagger-ui-guide.md).

## Table of Contents

- [AI Agent Mem0 API](#-ai-agent-mem0-api)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Testing with Swagger UI](#api-testing-with-swagger-ui)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
  - [Render](#render)
  - [Railway](#railway)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

The project is organized as follows:

```
.
├── app/                  # Main application code (FastAPI)
│   ├── api/             # API endpoints and routers
│   ├── core/            # Core configuration and managers
│   ├── db/              # Database clients and connections
│   ├── models/          # Pydantic models
│   └── services/        # Business logic services
├── tests/                # Pytest tests with Allure reporting
├── scripts/              # Utility scripts for testing and deployment
├── docs/                 # Project documentation including API guides
├── .github/              # GitHub Actions workflows (if any)
├── .venv/                # Virtual environment
├── allure-results/       # Allure test results
├── output/               # General output directory
├── .dockerignore         # Specifies intentionally untracked files that Docker should ignore
├── .gitignore            # Specifies intentionally untracked files that Git should ignore
├── cloudbuild.yaml       # Google Cloud Build configuration
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for building the application image
├── Dockerfile.railway    # Dockerfile specific to Railway deployment
├── Dockerfile.original   # Original Dockerfile (backup or alternative)
├── deploy-railway.sh     # Script for deploying to Railway
├── deploy.sh             # General deployment script
├── get-pip.py            # Script to install pip
├── pytest.ini            # Pytest configuration
├── railway-simple.json   # Simplified Railway configuration
├── railway.json          # Railway configuration
├── README_RAILWAY_DEPLOYMENT.md # Detailed Railway deployment instructions
├── README_RAILWAY_DEPLOYMENT_DETAILS.md # Additional Railway deployment details
├── RAILWAY_CLI_COMMANDS.md # Railway CLI commands
├── README_RENDER_DEPLOYMENT.md # Detailed Render deployment instructions
├── render.yaml           # Render configuration
├── requirements.in       # Main dependencies file for uv
├── requirements.lock     # Lock file for dependencies
├── requirements.txt      # Pinned dependencies generated from requirements.in
```

## Getting Started

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Python package installer and virtual environment manager)
- Docker (optional, for containerized development and deployment)
- **For AI Agent API**: OpenAI API key and Qdrant vector database access

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pytest-fast-api-template.git
    cd pytest-fast-api-template
    ```

2.  **Create and activate a virtual environment using uv:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Unix/macOS
    # .venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies using uv:**
    ```bash
    uv pip install -r requirements.txt
    ```
    *Note: `requirements.txt` is generated from `requirements.in`. If you add new dependencies, add them to `requirements.in` and then run `uv pip compile requirements.in` to update `requirements.txt`.*

4.  **Configure environment variables:**
    ```bash
    # Copy the example environment file
    cp env.example .env
    
    # Edit .env with your configuration
    # - OPENAI_API_KEY: Your OpenAI API key
    # - QDRANT_URL: Your Qdrant database URL
    # - Other configuration as needed
    ```

## Running the Application

To run the FastAPI application locally:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://127.0.0.1:8000`.

### Health Check
```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system status
curl http://localhost:8000/api/v1/health/detailed
```

## API Testing with Swagger UI

The API includes comprehensive Swagger UI documentation for interactive testing:

### Access Swagger UI
```bash
# Automatic launcher (recommended)
python scripts/open_swagger_ui.py

# Or visit manually
open http://localhost:8000/docs
```

### Testing Workflow
1. **Health Check**: Start with `/health` endpoints to verify system status
2. **Chat Testing**: Use `/api/v1/chat` with different user scenarios
3. **Memory Verification**: Test memory persistence across conversations

### Example Test Cases
```json
// New user conversation
{
  "user_id": "test_user_001",
  "message": "I'm interested in BPC-157 peptide",
  "metadata": {"domain": "peptide_coaching"}
}

// Follow-up conversation (same user_id)
{
  "user_id": "test_user_001", 
  "message": "What are the side effects?",
  "metadata": {"domain": "peptide_coaching"}
}
```

For comprehensive testing instructions, see [`docs/swagger-ui-guide.md`](docs/swagger-ui-guide.md).

## Running Tests

This project uses Pytest for testing and Allure for reporting.

You can run tests directly with pytest, or use the provided shell scripts for more control over test execution and environment selection.

### AI Agent API Tests
```bash
# Run AI Agent specific tests
pytest tests/test_ai_agent_api.py --alluredir=allure-results -v

# Run manual test script
python scripts/test_ai_agent_api.py
```

### Using Test Runner Scripts

Shell scripts are available in `tests/utils/test_runners/` to help you:
- Run all tests
- Run tests by group/feature
- Run tests by file
- Specify the environment to test against (dev, uat, prod)

**Examples:**

Run all tests in the default (dev) environment:
```bash
./tests/utils/test_runners/run_all_tests.sh
```

Run all tests in a specific environment:
```bash
./tests/utils/test_runners/run_all_tests.sh -e dev
```

Run tests by group:
```bash
./tests/utils/test_runners/run_by_group.sh -g "API Tests"
```

Run a specific test file:
```bash
./tests/utils/test_runners/run_by_file.sh -f tests/api/v1/test_hello.py
```

You can also pass additional pytest options to these scripts as needed.

For more details on test organization, environment configuration, and advanced usage, see [`tests/README.md`](tests/README.md).

1.  **Run Pytest tests and generate Allure results (direct):**
    ```bash
    pytest --alluredir=allure-results -v -s
    ```

2.  **Serve the Allure report:**
    ```bash
    allure serve allure-results
    ```
    This will open the report in your web browser.

## Deployment

This template is designed for easy deployment to cloud platforms.

### Render

Refer to the `README_RENDER_DEPLOYMENT.md` file and `render.yaml` for detailed instructions on deploying to Render.

Key files:
- `render.yaml`
- `README_RENDER_DEPLOYMENT.md`
- `Dockerfile` (or rely on Render's native Python support)

### Railway

Refer to the `README_RAILWAY_DEPLOYMENT.md`, `README_RAILWAY_DEPLOYMENT_DETAILS.md`, and `RAILWAY_CLI_COMMANDS.md` files for comprehensive guidance on deploying to Railway.

Key files:
- `railway.json` / `railway-simple.json`
- `Dockerfile.railway`
- `deploy-railway.sh`
- `README_RAILWAY_DEPLOYMENT.md`
- `README_RAILWAY_DEPLOYMENT_DETAILS.md`
- `RAILWAY_CLI_COMMANDS.md`

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to the project's coding standards and that all tests pass.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if one exists, otherwise specify your chosen license). 