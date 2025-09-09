# Canvas Local Speed Grader

A standalone Python program that acts as a local speed grader interface for Canvas discussions. This tool focuses purely on Canvas API interactions while delegating all grading logic to external executables.

## Architecture

The system has a clean separation of concerns:
- **`canvas_speedgrader.py`**: Handles all Canvas API interactions (reading discussions, posting grades/comments)
- **External Grader**: Your custom grading logic (separate executable that you provide)

## Workflow

1. **Fetch Data**: Reads discussion submissions and course roster from Canvas
2. **Grade Submissions**: For each student submission, calls your external grader
3. **Post Results**: Posts grades and comments back to Canvas (if not in dry-run mode)

## Features

- **Pure API Focus**: Only handles Canvas interactions - no embedded grading logic
- **Student Verification**: Includes Login IDs to ensure correct student identification
- **External Grader Interface**: Clean JSON-based interface to your grading executable
- **Dry Run Mode**: Safe testing without posting to Canvas
- **Comprehensive Logging**: All API calls and errors logged
- **Error Resilience**: Individual failures don't stop the entire process

## Requirements

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Canvas API developer key
- Access to Canvas instance
- Your external grading executable

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency management and requires Python 3.12+.

1. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone or download this repository

3. Initialize the project environment:
   ```bash
   uv sync
   ```

4. The project will automatically use Python 3.12 and install all required dependencies.

### Legacy Installation (if not using uv)

If you prefer to use traditional pip:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

You can configure the Canvas connection in three ways:

### Option 1: Environment Variables (Recommended)
```bash
export CANVAS_URL="https://your-institution.instructure.com"
export CANVAS_API_KEY="your_canvas_api_developer_key_here"
```

### Option 2: Configuration File
1. Copy the example config file:
   ```bash
   cp canvas_config.json.example canvas_config.json
   ```
2. Edit `canvas_config.json` with your Canvas URL and API key

### Option 3: Command Line Arguments
Use `--canvas-url` and `--api-key` arguments when running the script

## Getting Your Canvas API Key

1. Log into your Canvas instance
2. Go to Account → Settings
3. Scroll down to "Approved Integrations"
4. Click "+ New Access Token"
5. Enter a purpose (e.g., "Discussion Grading Tool")
6. Generate and copy the token

## Usage

### Basic Usage (Dry Run)

Test without posting anything to Canvas:

```bash
# Using uv (recommended)
uv run python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py

# Using traditional python
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py
```

### Live Grading

Actually post grades and comments to Canvas:

```bash
# Using uv (recommended)
uv run python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py --live

# Using traditional python
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py --live
```

### Graded Discussion

For discussions with grades, include the assignment ID:

```bash
# Using uv (recommended)
uv run python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --assignment-id 54321 --grader ./my_grader.py --live

# Using traditional python
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --assignment-id 54321 --grader ./my_grader.py --live
```

### Save Results

Save detailed results to a JSON file:

```bash
# Using uv (recommended)
uv run python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py --output results.json

# Using traditional python
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 --grader ./my_grader.py --output results.json
```

## Command Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--course-id` | Yes | Canvas course ID |
| `--discussion-id` | Yes | Canvas discussion topic ID |
| `--grader` | Yes | Path to your external grading executable |
| `--assignment-id` | No | Assignment ID (required for posting grades) |
| `--live` | No | Actually post grades/comments (default is dry run) |
| `--canvas-url` | No | Canvas instance URL (overrides config) |
| `--api-key` | No | Canvas API key (overrides config) |
| `--output` | No | Output file for results (JSON format) |

## Finding Canvas IDs

### Course ID
- Go to your Canvas course
- Look at the URL: `https://your-canvas.com/courses/12345`
- The number after `/courses/` is your course ID

### Discussion ID
- Go to the specific discussion
- Look at the URL: `https://your-canvas.com/courses/12345/discussion_topics/67890`
- The number after `/discussion_topics/` is your discussion ID

### Assignment ID (for graded discussions)
- Go to the assignment associated with the discussion
- Look at the URL: `https://your-canvas.com/courses/12345/assignments/54321`
- The number after `/assignments/` is your assignment ID

## External Grader Interface

Your grading executable must:

1. **Accept JSON input via stdin** with this structure:
```json
{
  "discussion": {
    "id": 67890,
    "title": "Discussion Topic Title",
    "prompt": "The discussion prompt/instructions"
  },
  "student": {
    "user_id": 98765,
    "name": "Student Name",
    "login_id": "student123",
    "email": "student@university.edu",
    "sortable_name": "Name, Student"
  },
  "submission": {
    "entry_id": 456789,
    "message": "The student's discussion post content",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "word_count": 150
  }
}
```

2. **Output JSON result via stdout** with this structure:
```json
{
  "grade": "A",
  "comment": "Excellent analysis with good examples. Total score: 95/100 (A)"
}
```

### Required Output Fields
- `grade`: The grade value (letter grade like "A", "B" or numeric like "85", "92")
- `comment`: (Optional) Feedback comment to post as a reply

### Example Grader

The included `example_grader.py` demonstrates the interface:

```bash
# Test the example grader with sample data
echo '{"discussion":{"title":"Test"},"student":{"name":"Test Student","login_id":"test123"},"submission":{"message":"This is a test response with multiple sentences. It demonstrates adequate length and some analysis.","word_count":15}}' | ./example_grader.py
```

## Creating Your Own Grader

Your grader can be written in any language (Python, R, JavaScript, etc.) as long as it:

1. Is executable (`chmod +x your_grader.py`)
2. Reads JSON from stdin
3. Outputs JSON to stdout
4. Returns non-zero exit code on error

### Python Grader Template

```python
#!/usr/bin/env python3
import json
import sys

def grade_submission(data):
    discussion = data['discussion']
    student = data['student'] 
    submission = data['submission']
    
    # Your grading logic here
    message = submission['message']
    
    # Example: Simple word count grading
    word_count = submission['word_count']
    if word_count >= 100:
        grade = "A"
        comment = f"Hi {student['name'].split()[0]}, excellent detailed response!"
    else:
        grade = "C" 
        comment = f"Hi {student['name'].split()[0]}, consider expanding your response."
    
    return {"grade": grade, "comment": comment}

if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = grade_submission(data)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e), "grade": "0"}), file=sys.stderr)
        sys.exit(1)
```

## Output

The program provides several types of output:

### Console Output
```
=== DRY RUN MODE ===
Use --live flag to actually post grades and comments
Processing discussion 67890 in course 12345
2024-01-15 10:30:15 - INFO - Fetching users for course 12345
2024-01-15 10:30:16 - INFO - Found 25 active students in roster
2024-01-15 10:30:17 - INFO - Retrieved 25 discussion entries
2024-01-15 10:30:18 - INFO - Grading submission from student123 (John Smith)

Processed 25 student submissions:
student123 (John Smith): Grade=A 
student456 (Jane Doe): Grade=B 
student789 (Bob Wilson): Grade=A 
...

Processing complete!
```

### Log File
- Detailed logging saved to `canvas_speedgrader.log`
- Includes API calls, grader executions, and error details

### JSON Output (Optional)
Complete processing results with all metadata:
```json
[
  {
    "user_id": 98765,
    "login_id": "student123",
    "student_name": "John Smith", 
    "entry_id": 456789,
    "grade": "A",
    "comment": "Excellent analysis...",
    "grader_output": {...},
    "dry_run": true
  }
]
```

## Safety Features

- **Dry Run by Default**: Without `--live` flag, no changes are made to Canvas
- **Student Verification**: Login IDs help verify correct student identification
- **Error Isolation**: Problems with individual submissions don't stop the entire process
- **Comprehensive Logging**: All actions and errors are logged
- **Timeout Protection**: Grader processes have 30-second timeout

## Troubleshooting

### Canvas API Issues
- Verify your Canvas URL is correct (include https://)
- Check that your API key is valid and not expired
- Ensure you have instructor/TA permissions in the course

### Grader Issues
- Verify your grader executable exists and is executable (`chmod +x grader.py`)
- Test your grader manually with sample data
- Check that grader outputs valid JSON
- Look at the log file for detailed error messages

### Common Issues
1. **"Grader executable not found"**: Check the path to your grader
2. **"Permission denied"**: Make sure grader is executable (`chmod +x`)
3. **"Invalid JSON from grader"**: Check grader's stdout format
4. **"Discussion not found"**: Verify course and discussion IDs
5. **"No active students found"**: Check course roster and enrollment states

## Advanced Usage

### Multiple Discussions
Process multiple discussions with a simple script:

```bash
#!/bin/bash
COURSE_ID=12345
GRADER="./my_grader.py"

discussions=(67890 67891 67892)

for disc_id in "${discussions[@]}"; do
    echo "Processing discussion $disc_id"
    python canvas_speedgrader.py \
        --course-id $COURSE_ID \
        --discussion-id $disc_id \
        --grader $GRADER \
        --live
    sleep 2  # Rate limiting courtesy
done
```

### Integration with Other Tools
Process results with other tools:

```bash
# Grade and save detailed results
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 \
    --grader ./my_grader.py --output results.json --live

# Extract specific data with jq
jq '.[] | select(.grade == "F") | .login_id' results.json  # Find failing students
jq '[.[] | .grade] | group_by(.) | map({grade: .[0], count: length})' results.json  # Grade distribution
```

### Custom Grading Workflows
You can chain multiple graders or add preprocessing:

```bash
# Multi-stage grading
python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 \
    --grader ./content_grader.py --output content_results.json

python canvas_speedgrader.py --course-id 12345 --discussion-id 67890 \
    --grader ./style_grader.py --output style_results.json

# Combine results with custom script
python combine_grades.py content_results.json style_results.json
```

## License

This tool is provided as-is for educational purposes. Please respect Canvas terms of service and your institution's policies when using automated tools.

## Contributing

Feel free to modify the code for your specific needs. The modular design makes it easy to extend functionality or adapt to different Canvas configurations.
