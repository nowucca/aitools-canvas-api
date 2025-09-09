# Canvas API Grader - System Patterns & Architecture

## System Architecture

### Core Components Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Canvas API     │    │  UV Wrapper     │
│ canvas_speed    │◄──►│  Integration    │◄──►│  Shell Script   │
│ grader.py       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Logging &     │    │  JSON Comm      │    │  External       │
│   Error         │    │  Protocol       │    │  Grader         │
│   Handling      │    │                 │    │  (Isolated)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Design Patterns

#### 1. **Command Pattern**
- CLI interface (`canvas_speedgrader.py`) encapsulates grading operations as executable commands
- Clear separation between command parsing and execution logic
- Supports dry-run mode as command modifier

#### 2. **Strategy Pattern**
- External grader scripts implement grading strategies
- UV wrapper enables strategy switching without system changes
- JSON communication provides consistent interface across strategies

#### 3. **Facade Pattern**
- Canvas API integration hides complexity of REST API calls
- Single interface for discussion, assignment, and user operations
- Simplifies error handling and retry logic

#### 4. **Template Method Pattern**
- `process_discussion()` method defines grading algorithm skeleton
- Subclasses (different grader types) implement specific steps
- Consistent logging and error handling across implementations

## Component Relationships

### Primary Data Flow
1. **CLI Input** → Parameter validation and Canvas API setup
2. **Canvas Fetch** → Retrieve students, discussions, and assignments
3. **Submission Processing** → Format data for external grader
4. **UV Execution** → Isolated grader execution via shell wrapper
5. **Result Integration** → Parse grader output and post to Canvas
6. **Logging & Cleanup** → Comprehensive audit trail and resource cleanup

### Critical Implementation Paths

#### Path 1: UV Environment Isolation
```bash
# uv_grader_wrapper.sh critical sequence:
unset VIRTUAL_ENV                    # Prevent environment conflicts
cd "$PROJECT_PATH"                   # Change to grader directory
uv run python "$GRADER_SCRIPT"      # Execute in isolated environment
```

**Key Decisions:**
- `unset VIRTUAL_ENV` prevents interference from existing virtual environments
- Foreground execution preserves stdin/stdout for JSON communication
- Signal handling ensures proper cleanup on interruption

#### Path 2: Canvas API Integration
```python
# canvas_speedgrader.py critical sequence:
discussion_data = canvas_api.get_discussion(discussion_id)
students = canvas_api.get_students(course_id) 
entries = canvas_api.get_discussion_entries(discussion_id)
# Process each submission
grading_result = call_grader(submission_data)
canvas_api.submit_grade(user_id, assignment_id, grade)
canvas_api.post_submission_comment(assignment_id, user_id, comment)
```

**Key Decisions:**
- Direct REST API calls instead of SDK dependencies
- Assignment ID required for grade posting (discovered via separate lookup)
- Private submission comments instead of public discussion replies
- Comprehensive error handling with retry logic

#### Path 3: JSON Communication Protocol
```python
# Standardized input format to grader:
{
    "student_name": "...",
    "student_login": "...", 
    "submission_text": "...",
    "word_count": 123,
    "timestamp": "..."
}

# Expected output format from grader:
{
    "grade": "7",
    "comment": "Detailed feedback...",
    "points": 7,
    "word_count": 123,
    "meets_word_count": true,
    "improvement_suggestions": [...]
}
```

**Key Decisions:**
- JSON stdin/stdout communication for clean separation
- Standardized schema across all grader implementations
- Rich feedback structure supporting multiple grading criteria

## System Constraints & Design Decisions

### Performance Patterns
- **Sequential Processing**: Processes students one at a time to avoid Canvas API rate limits
- **Timeout Management**: 30-second timeout per grader execution prevents hangs
- **Resource Cleanup**: Comprehensive cleanup on both success and failure paths

### Error Handling Patterns
- **Graceful Degradation**: Individual grading failures don't stop batch processing
- **Comprehensive Logging**: DEBUG level logging for troubleshooting
- **Safe Defaults**: Dry-run mode as default prevents accidental operations

### Security Patterns
- **Credential Isolation**: Canvas API keys in separate config files (.gitignored)
- **Environment Isolation**: UV environments prevent code injection via dependencies
- **Input Validation**: Strict validation of Canvas IDs and student parameters

### Maintainability Patterns
- **Minimal Dependencies**: Only `requests` library for maximum compatibility
- **Clear Separation**: Business logic separate from Canvas API and UV wrapper
- **Comprehensive Documentation**: README files for both regular and UV usage patterns
