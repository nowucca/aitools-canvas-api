#!/usr/bin/env python3
"""
Find Assignment ID for a Discussion

This helper script finds the assignment ID associated with a graded discussion.
"""

import json
import sys
from canvas_speedgrader import load_config, CanvasAPIClient

def main():
    if len(sys.argv) != 3:
        print("Usage: python find_assignment_id.py <course_id> <discussion_id>")
        print("Example: python find_assignment_id.py 215770 2194470")
        sys.exit(1)
    
    course_id = int(sys.argv[1])
    discussion_id = int(sys.argv[2])
    
    # Load configuration
    config = load_config()
    if not config['canvas_url'] or not config['api_key']:
        print("Error: Canvas URL and API key are required")
        sys.exit(1)
    
    # Initialize Canvas client
    canvas = CanvasAPIClient(config['canvas_url'], config['api_key'])
    
    try:
        # Get discussion details
        discussion = canvas.get_discussion(course_id, discussion_id)
        
        print(f"Discussion: {discussion.get('title', 'Unknown')}")
        print(f"Discussion ID: {discussion_id}")
        
        if 'assignment_id' in discussion and discussion['assignment_id']:
            print(f"Assignment ID: {discussion['assignment_id']}")
            print(f"\nTo run live grading for samanebk24:")
            print(f"python canvas_speedgrader.py \\")
            print(f"    --course-id {course_id} \\")
            print(f"    --discussion-id {discussion_id} \\")
            print(f"    --assignment-id {discussion['assignment_id']} \\")
            print(f"    --grader ./uv_grader_wrapper.sh \\")
            print(f"    --only-student samanebk24 \\")
            print(f"    --live \\")
            print(f"    --output live_test_samanebk24.json")
        else:
            print("This discussion is not a graded assignment.")
            print("Assignment ID: None")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
