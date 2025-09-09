# Canvas API Grader - Project Brief

## Overview
A Python-based automated grading system that integrates with Canvas LMS to provide AI-powered feedback on student discussion posts. The system uses external grader processes running in isolated UV virtual environments to ensure clean, reproducible grading.

## Core Requirements

### Primary Goals
1. **UV Environment Isolation**: Execute external Python graders in separate UV virtual environments to avoid dependency conflicts
2. **Canvas API Integration**: Seamlessly interface with Canvas discussions and assignments via REST API
3. **Automated Grading**: Process student submissions and provide structured feedback with grades
4. **Privacy-Focused**: Post private comments to students rather than public discussion replies
5. **Production Ready**: Robust error handling, logging, and dry-run capabilities

### Key Features
- **UV Wrapper System**: Shell script wrapper (`uv_grader_wrapper.sh`) that isolates grader execution
- **Canvas SpeedGrader Integration**: Direct integration with Canvas assignment grading system
- **JSON Communication**: Structured input/output via JSON for grader communication
- **Single Student Testing**: `--only-student` parameter for safe testing and iteration
- **Comprehensive Logging**: Detailed logging for troubleshooting and audit trails
- **Dry Run Mode**: Default safe mode that shows what would happen without posting grades

### Technical Architecture
- **Python 3.12** with **UV** package management for modern, fast dependency resolution
- **Direct Canvas API calls** using `requests` library (no heavy Canvas SDK dependencies)
- **Shell wrapper** for environment isolation and signal handling
- **JSON-based grader interface** for clean separation of concerns

## Success Criteria
1. Graders can run in isolated UV environments without dependency conflicts
2. Canvas API integration works reliably for both discussions and assignments  
3. System handles errors gracefully and provides clear feedback
4. Safe testing mode allows iteration without affecting live grades
5. Production deployment is straightforward with minimal external dependencies

## Project Scope
**In Scope:**
- UV environment wrapper system
- Canvas API discussion and assignment integration  
- JSON grader communication protocol
- Error handling and logging infrastructure
- Git repository setup with proper exclusions

**Out of Scope:**
- Canvas SDK dependencies (using direct API calls instead)
- Complex UI interfaces (command-line focused)
- Multi-institutional Canvas support (single instance focused)
- Real-time grading triggers (batch processing focused)
