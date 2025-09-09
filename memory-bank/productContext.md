# Canvas API Grader - Product Context

## Why This Project Exists

### Problem Statement
Educational institutions using Canvas LMS need efficient, consistent ways to grade student discussion posts and assignments. Manual grading is time-intensive and can be inconsistent across large classes. Existing solutions either:
- Require complex Canvas SDK integrations with heavy dependencies
- Lack proper environment isolation leading to dependency conflicts
- Don't provide safe testing mechanisms for iterative development
- Post public replies instead of private feedback, violating student privacy expectations

### Core Problems Solved
1. **Environment Isolation**: Eliminates dependency conflicts when running external grading scripts
2. **API Complexity**: Simplifies Canvas API interaction with direct REST calls instead of complex SDKs
3. **Privacy Protection**: Ensures student feedback remains private via submission comments rather than public posts
4. **Testing Safety**: Provides robust dry-run and single-student testing modes
5. **Operational Reliability**: Offers comprehensive logging and error handling for production use

## How It Should Work

### User Experience Flow
1. **Setup Phase**: Instructor configures Canvas API credentials and grader script locations
2. **Testing Phase**: Uses `--only-student` flag to test grading logic on individual students safely
3. **Validation Phase**: Runs in dry-run mode to review all grades and comments before posting
4. **Production Phase**: Executes live grading with full logging and error recovery

### Key Interactions
- **Command Line Interface**: Simple, scriptable CLI for automated workflows
- **JSON Communication**: Clean data exchange between main system and external graders
- **Canvas Integration**: Seamless posting of grades and private comments
- **Environment Isolation**: Transparent execution of graders in separate UV environments

## User Experience Goals

### Primary Users: Course Instructors and TAs
- **Simplicity**: Single command execution with clear parameter options
- **Safety**: Default dry-run mode prevents accidental grade posting
- **Transparency**: Comprehensive logging shows exactly what the system is doing
- **Flexibility**: Support for custom grading logic via external scripts
- **Reliability**: Robust error handling and recovery mechanisms

### Secondary Users: System Administrators  
- **Maintainability**: Clean codebase with minimal external dependencies
- **Deployment**: Simple Python 3.12 + UV setup process
- **Monitoring**: Clear logging and error reporting for troubleshooting
- **Security**: Secure credential handling with example configurations

## Success Metrics
1. **Time Savings**: Reduce grading time from hours to minutes for large classes
2. **Consistency**: Ensure uniform grading criteria across all student submissions
3. **Safety**: Zero accidental grade postings during development/testing phases
4. **Reliability**: 99%+ successful grade posting rate in production
5. **Usability**: Instructors can use system with minimal technical training

## User Scenarios

### Scenario 1: New Assignment Grading
Instructor has a new discussion assignment with 100+ student responses. They:
1. Test grading logic on 1-2 students using `--only-student`
2. Run full dry-run to review all proposed grades
3. Execute live grading with confidence in the results

### Scenario 2: Iterative Grader Development
TA is developing/refining grading criteria and needs to:
1. Run isolated tests without affecting live grades
2. Compare grading results across different criteria versions
3. Safely deploy improved grading logic to production

### Scenario 3: Large-Scale Production Grading
Institution processes hundreds of submissions weekly and needs:
1. Reliable, automated grading execution
2. Comprehensive audit trails for grade justification
3. Error recovery for network/API failures
4. Consistent performance across different grader types
