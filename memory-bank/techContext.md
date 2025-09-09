# Canvas API Grader - Technical Context

## Technologies Used

### Core Runtime
- **Python 3.12**: Latest stable Python with modern features and performance improvements
- **UV Package Manager**: Fast, modern Python package manager for dependency resolution and virtual environment management
- **Bash Shell Scripting**: UV wrapper system for environment isolation and process management

### Primary Dependencies
- **requests>=2.25.1**: HTTP library for Canvas API communication
  - Chosen over Canvas SDK to minimize dependencies and maintain control
  - Reliable, well-established library with excellent error handling
  - Direct REST API calls provide transparency and debugging capability

### Development Setup

#### UV Environment Configuration
```toml
# pyproject.toml
[project]
name = "canvas-api-grader"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = ["requests>=2.25.1"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
exclude = ["canvas_env/", "memory-bank/", ".clinerules/", "*.json", "*.log", "test_*.py"]
```

#### Environment Management
- **Primary Environment**: `.venv` managed by UV
- **Legacy Support**: `canvas_env/` directory for backward compatibility (gitignored)
- **Isolation Strategy**: `unset VIRTUAL_ENV` in wrapper to prevent conflicts

### Technical Constraints

#### Python Version Requirements
- **Minimum**: Python 3.12 for modern syntax and performance
- **UV Compatibility**: Latest UV version for optimal dependency resolution
- **Cross-Platform**: macOS and Linux support (Windows compatibility via WSL)

#### Canvas API Limitations
- **Rate Limits**: Sequential processing to avoid API throttling
- **Authentication**: Personal access tokens only (no OAuth implementation)
- **API Version**: Canvas REST API v1 (stable, widely supported)

#### System Resource Constraints
- **Memory**: Minimal memory footprint with streaming JSON processing
- **Network**: Robust error handling for intermittent connectivity
- **Storage**: Temporary files cleaned up automatically

## Tool Usage Patterns

### UV Workflow
```bash
# Initial setup
uv sync                                    # Install dependencies
uv run python canvas_speedgrader.py      # Execute with isolated environment

# Development workflow  
uv add requests                           # Add new dependencies
uv run python -m pytest                  # Run tests in isolated environment
uv build                                 # Build distribution packages
```

### Canvas API Integration
```python
# Direct REST API pattern
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(f"{canvas_url}/api/v1/courses/{course_id}/discussion_topics/{discussion_id}")

# Error handling pattern
try:
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Canvas API error: {e}")
    raise
```

### UV Wrapper Integration
```bash
# Environment isolation pattern
export PROJECT_PATH="/path/to/grader/project"
export GRADER_SCRIPT="grader.py"
./uv_grader_wrapper.sh < submission.json > results.json
```

## Development Practices

### Code Organization
- **Single Responsibility**: Each module has clear, focused purpose
- **Dependency Injection**: Canvas API configuration injected at runtime
- **Error Boundaries**: Comprehensive exception handling at module boundaries
- **Logging Strategy**: Structured logging with configurable levels

### Testing Approach
- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: Canvas API testing with dry-run mode
- **Manual Testing**: `--only-student` flag for safe live testing
- **Error Testing**: Comprehensive error condition coverage

### Performance Considerations
- **API Efficiency**: Batch requests where possible, respect rate limits
- **Memory Management**: Stream processing for large student lists
- **Timeout Management**: Reasonable timeouts prevent hanging operations
- **Resource Cleanup**: Explicit cleanup of temporary files and processes

## Deployment Architecture

### Local Development
```
canvas_api/
├── .venv/                 # UV virtual environment
├── pyproject.toml         # Project configuration
├── uv.lock               # Locked dependencies
├── canvas_speedgrader.py # Main application
├── uv_grader_wrapper.sh  # Environment wrapper
└── canvas_config.json    # API credentials (gitignored)
```

### Production Deployment
- **Containerization**: Docker support via pyproject.toml configuration
- **Credential Management**: Environment variables or secure config files
- **Monitoring**: Structured logging for external log aggregation
- **Scaling**: Horizontal scaling via multiple instances (stateless design)

### Security Considerations
- **Credential Storage**: Canvas API tokens in separate, gitignored files
- **Environment Isolation**: UV environments prevent dependency conflicts and potential security issues
- **Input Validation**: Strict validation of all Canvas IDs and parameters
- **Network Security**: HTTPS-only Canvas API communication
- **Process Isolation**: External graders run in isolated UV environments

## Integration Points

### Canvas LMS Integration
- **Discussion API**: Retrieve discussion topics and student entries
- **Users API**: Match student submissions to Canvas user records
- **Assignments API**: Post grades and submission comments
- **Authentication**: Personal access token authentication

### External Grader Integration
- **Communication**: JSON stdin/stdout protocol
- **Isolation**: UV virtual environments prevent conflicts
- **Timeout**: 30-second execution timeout prevents hangs
- **Error Handling**: Graceful degradation for grader failures

### File System Integration
- **Configuration**: JSON configuration files for Canvas credentials
- **Logging**: Rotating log files with configurable retention
- **Output**: JSON results files for audit and debugging
- **Temporary Files**: Automatic cleanup of processing artifacts
