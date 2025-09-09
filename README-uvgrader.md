# UV Grader Wrapper

A robust shell wrapper for executing Python graders that run in separate `uv` virtual environments. This wrapper handles directory changes, configuration file access, signal forwarding, and error conditions to seamlessly integrate external graders with Canvas API workflows.

## Problem Statement

When you have a Python grader that:
- Lives in a separate `uv` virtual environment
- Needs to read its own configuration files (like `config/config.json`)
- Must run in its own project directory for proper operation
- Should be callable from anywhere as a grader provider

Traditional approaches fail because they can't handle the directory context, virtual environment activation, or signal management properly.

## Solution

The `uv_grader_wrapper.sh` script acts as a bridge that:
- ✅ Changes to the grader's project directory
- ✅ Activates the correct `uv` environment using `uv run`
- ✅ Forwards stdin/stdout for JSON communication
- ✅ Handles signal forwarding (Ctrl+C, etc.)
- ✅ Provides comprehensive error handling
- ✅ Can be called from any location
- ✅ Supports multiple grader configurations

## Quick Start

### Your Default Setup
```bash
# Use your default grader (no arguments needed)
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

The wrapper is preconfigured with your defaults:
- **Project Path**: `/Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General`
- **Grader Script**: `discussion-grader/canvas_speedgrader.py`

### Debug Mode
```bash
# See what's happening under the hood
UV_GRADER_DEBUG=1 python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

## Installation

1. **Copy the wrapper script** to your Canvas API project directory:
   ```bash
   # The script is already in your current directory
   ls -la uv_grader_wrapper.sh
   ```

2. **Verify it's executable** (should already be set):
   ```bash
   chmod +x uv_grader_wrapper.sh
   ```

3. **Test the wrapper** with help:
   ```bash
   ./uv_grader_wrapper.sh --help
   ```

## Usage Patterns

### 1. Default Usage (Your Setup)
```bash
# Uses your preconfigured defaults
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

### 2. Different Project Path
```bash
# Specify a different grader project
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh /path/to/other/grader"
```

### 3. Different Script Name
```bash
# Use a different script within the same project
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh /Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General custom-grader.py"
```

### 4. Completely Different Grader
```bash
# Different project and script
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh /other/project other-script.py"
```

### 5. Environment Variable Configuration
```bash
# Set via environment variables
export GRADER_PROJECT_PATH="/path/to/your/grader"
export GRADER_SCRIPT="custom-grader.py"
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

### 6. One-time Environment Variable
```bash
# Set for just this command
GRADER_PROJECT_PATH="/other/grader" python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

## Configuration

### Command Line Arguments
```bash
./uv_grader_wrapper.sh [PROJECT_PATH] [GRADER_SCRIPT]
```

- **PROJECT_PATH**: Path to the grader project directory
- **GRADER_SCRIPT**: Relative path to grader script within project

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GRADER_PROJECT_PATH` | Override project path | `/Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General` |
| `GRADER_SCRIPT` | Override grader script | `discussion-grader/canvas_speedgrader.py` |
| `UV_GRADER_DEBUG` | Enable debug output | `0` (disabled) |

### Precedence Order
1. Command line arguments (highest priority)
2. Environment variables
3. Built-in defaults (lowest priority)

## Error Handling

### Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Grader executed successfully |
| 1 | Invalid arguments | Wrong usage or arguments |
| 2 | Path error | Project path doesn't exist or isn't accessible |
| 3 | UV not found | `uv` command not available in PATH |
| 4 | Script error | Grader script doesn't exist or isn't readable |
| 130 | Interrupted | User pressed Ctrl+C |
| 143 | Terminated | Process terminated by SIGTERM |

### Error Messages
All error messages include timestamps and are sent to stderr:
```
[2024-09-09 01:15:30] ERROR: Project path does not exist: /wrong/path
[2024-09-09 01:15:30] ERROR: uv command not found in PATH
```

## Signal Handling

The wrapper properly handles Unix signals:

- **SIGINT (Ctrl+C)**: Graceful shutdown, forwards to child process
- **SIGTERM**: Clean termination, forwards to child process
- **EXIT trap**: Always cleans up and returns to original directory

### Behavior on Interruption
1. Receives signal (e.g., Ctrl+C)
2. Forwards signal to child grader process
3. Waits for graceful shutdown (1 second)
4. Force kills if necessary
5. Returns to original directory
6. Exits with appropriate code

## Debugging

### Enable Debug Mode
```bash
UV_GRADER_DEBUG=1 ./uv_grader_wrapper.sh
```

### Sample Debug Output
```
[2024-09-09 01:15:30] DEBUG: Starting UV Grader Wrapper
[2024-09-09 01:15:30] DEBUG: Project path: /Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General
[2024-09-09 01:15:30] DEBUG: Grader script: discussion-grader/canvas_speedgrader.py
[2024-09-09 01:15:30] DEBUG: Original directory: /Users/satkinson/Work/vtech/cs5740/2025/fall/Coding/canvas_api
[2024-09-09 01:15:30] DEBUG: uv command found: /opt/homebrew/bin/uv
[2024-09-09 01:15:30] DEBUG: Changing to project directory: /Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General
[2024-09-09 01:15:30] DEBUG: Grader script found: /Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General/discussion-grader/canvas_speedgrader.py
[2024-09-09 01:15:30] DEBUG: Found pyproject.toml - this appears to be a uv project
[2024-09-09 01:15:30] DEBUG: Executing: uv run python discussion-grader/canvas_speedgrader.py
[2024-09-09 01:15:30] DEBUG: Working directory: /Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General
[2024-09-09 01:15:30] DEBUG: Started child process with PID: 12345
[2024-09-09 01:15:35] DEBUG: Child process exited with code: 0
[2024-09-09 01:15:35] DEBUG: Returned to original directory: /Users/satkinson/Work/vtech/cs5740/2025/fall/Coding/canvas_api
[2024-09-09 01:15:35] DEBUG: UV Grader Wrapper completed successfully
```

## Advanced Usage

### Multiple Graders in a Workflow
```bash
# Grade with your primary grader
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"

# Grade with a different grader for comparison
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh /path/to/alt/grader"
```

### Integration with Scripts
```bash
#!/bin/bash
# Example: Grade multiple discussions with different graders

DISCUSSIONS=(12345 12346 12347)
GRADERS=(
    "/Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General"
    "/path/to/alt/grader"
    "/path/to/experimental/grader"
)

for i in "${!DISCUSSIONS[@]}"; do
    discussion_id="${DISCUSSIONS[$i]}"
    grader_path="${GRADERS[$i]}"
    
    echo "Grading discussion $discussion_id with grader $grader_path"
    python canvas_speedgrader.py \
        --course-id 54321 \
        --discussion-id "$discussion_id" \
        --grader "./uv_grader_wrapper.sh $grader_path"
done
```

### Environment Setup
```bash
# Create a grader environment file
cat > grader_env.sh << 'EOF'
export GRADER_PROJECT_PATH="/Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General"
export GRADER_SCRIPT="discussion-grader/canvas_speedgrader.py"
export UV_GRADER_DEBUG=1
EOF

# Source and use
source grader_env.sh
python canvas_speedgrader.py --grader "./uv_grader_wrapper.sh"
```

## Troubleshooting

### Common Issues

#### "uv command not found"
```bash
# Install uv if not available
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or via homebrew
brew install uv
```

#### "Project path does not exist"
```bash
# Verify the path exists
ls -la "/Users/satkinson/Work/vtech/cs5740/2025/spring/Grading/Discussion-General"

# Use absolute paths to avoid confusion
./uv_grader_wrapper.sh "/absolute/path/to/project"
```

#### "Grader script does not exist"
```bash
# Check the script exists in the project
ls -la "/path/to/project/discussion-grader/canvas_speedgrader.py"

# Make sure you're using the relative path within the project
./uv_grader_wrapper.sh "/path/to/project" "discussion-grader/canvas_speedgrader.py"
```

#### Permission Issues
```bash
# Ensure the wrapper is executable
chmod +x uv_grader_wrapper.sh

# Ensure the grader script is readable
chmod +r "/path/to/grader/script.py"
```

#### JSON Communication Issues
The wrapper preserves stdin/stdout for JSON communication. If you're seeing JSON parsing errors:

1. Enable debug mode: `UV_GRADER_DEBUG=1`
2. Check that your grader outputs valid JSON to stdout
3. Ensure error messages go to stderr, not stdout

#### Signal Handling Issues
If Ctrl+C doesn't work properly:

1. Check that your grader handles signals correctly
2. Enable debug mode to see signal forwarding
3. The wrapper will force-kill after 1 second if needed

### Testing the Wrapper

#### Test basic functionality:
```bash
# Test help output
./uv_grader_wrapper.sh --help

# Test with debug mode but no input (will likely fail gracefully)
echo '{}' | UV_GRADER_DEBUG=1 ./uv_grader_wrapper.sh
```

#### Test with your actual grader:
```bash
# Create a test JSON input
cat > test_input.json << 'EOF'
{
  "discussion": {
    "id": 12345,
    "title": "Test Discussion",
    "prompt": "This is a test prompt"
  },
  "student": {
    "user_id": 67890,
    "name": "Test Student",
    "login_id": "test123"
  },
  "submission": {
    "entry_id": 11111,
    "message": "This is a test submission with enough words to trigger grading logic.",
    "created_at": "2024-09-09T01:00:00Z",
    "word_count": 12
  }
}
EOF

# Test the wrapper
UV_GRADER_DEBUG=1 ./uv_grader_wrapper.sh < test_input.json
```

## Requirements

- **Bash 4.0+** (for associative arrays and modern features)
- **uv command** in PATH ([installation guide](https://docs.astral.sh/uv/))
- **Target grader project** with `uv` environment set up
- **Grader script** that accepts JSON via stdin and outputs JSON via stdout

## Integration with canvas_speedgrader.py

The wrapper is designed to be a drop-in replacement for direct grader scripts:

```python
# Instead of:
speed_grader = LocalSpeedGrader(canvas_client, "/path/to/grader.py")

# Use:
speed_grader = LocalSpeedGrader(canvas_client, "./uv_grader_wrapper.sh")
```

The wrapper handles all the complexity of:
- Directory management
- Virtual environment activation
- Signal forwarding
- Error propagation
- Exit code handling

## Contributing

To modify or extend the wrapper:

1. **Test thoroughly** with debug mode enabled
2. **Preserve stdin/stdout** for JSON communication
3. **Send logs to stderr** only
4. **Handle signals properly** for clean shutdown
5. **Use appropriate exit codes** for different error conditions

## License

This wrapper script is part of your Canvas grading workflow and follows the same licensing as your project.
