#!/usr/bin/env python3
"""
Canvas Discussions API Client

A standalone Python program to read discussions, generate comments and grades,
and post them back to Canvas discussions using the Canvas API.

Requirements:
- Python 3.6+
- requests library (pip install requests)
- Canvas API developer key
- Canvas instance URL

Usage:
    python canvas_discussions.py --course-id 12345 --discussion-id 67890
"""

import requests
import json
import argparse
import logging
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
import os


class CanvasDiscussionsClient:
    """Client for interacting with Canvas Discussions API"""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Canvas client
        
        Args:
            base_url: Canvas instance URL (e.g., 'https://canvas.instructure.com')
            api_key: Canvas API developer key
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('canvas_discussions.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an API request to Canvas
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {method} {url} - {str(e)}")
            raise
    
    def get_discussion(self, course_id: int, discussion_id: int) -> Dict[str, Any]:
        """
        Get discussion topic details
        
        Args:
            course_id: Canvas course ID
            discussion_id: Canvas discussion topic ID
            
        Returns:
            Discussion topic data
        """
        self.logger.info(f"Fetching discussion {discussion_id} from course {course_id}")
        endpoint = f"courses/{course_id}/discussion_topics/{discussion_id}"
        return self._make_request('GET', endpoint)
    
    def get_discussion_entries(self, course_id: int, discussion_id: int) -> List[Dict[str, Any]]:
        """
        Get all entries (posts) in a discussion
        
        Args:
            course_id: Canvas course ID
            discussion_id: Canvas discussion topic ID
            
        Returns:
            List of discussion entries
        """
        self.logger.info(f"Fetching discussion entries for discussion {discussion_id}")
        endpoint = f"courses/{course_id}/discussion_topics/{discussion_id}/entries"
        
        entries = []
        page = 1
        per_page = 50
        
        while True:
            params = {'page': page, 'per_page': per_page}
            response = self._make_request('GET', endpoint, params=params)
            
            if not response:
                break
                
            entries.extend(response)
            
            # Check if there are more pages
            if len(response) < per_page:
                break
                
            page += 1
        
        self.logger.info(f"Retrieved {len(entries)} discussion entries")
        return entries
    
    def post_discussion_entry(self, course_id: int, discussion_id: int, 
                            message: str, parent_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Post a new entry (comment) to a discussion
        
        Args:
            course_id: Canvas course ID
            discussion_id: Canvas discussion topic ID
            message: Comment text
            parent_id: ID of parent entry (for replies)
            
        Returns:
            Created entry data
        """
        endpoint = f"courses/{course_id}/discussion_topics/{discussion_id}/entries"
        
        data = {'message': message}
        if parent_id:
            data['parent_id'] = parent_id
        
        self.logger.info(f"Posting comment to discussion {discussion_id}")
        return self._make_request('POST', endpoint, json=data)
    
    def grade_discussion_entry(self, course_id: int, assignment_id: int, 
                             user_id: int, grade: str, comment: Optional[str] = None) -> Dict[str, Any]:
        """
        Grade a discussion entry (if discussion is graded)
        
        Args:
            course_id: Canvas course ID
            assignment_id: Canvas assignment ID (for graded discussions)
            user_id: Canvas user ID to grade
            grade: Grade value (points or letter grade)
            comment: Optional comment for the grade
            
        Returns:
            Submission data
        """
        endpoint = f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"
        
        data = {
            'submission': {
                'posted_grade': grade
            }
        }
        
        if comment:
            data['comment'] = {
                'text_comment': comment
            }
        
        self.logger.info(f"Grading user {user_id} for assignment {assignment_id}: {grade}")
        return self._make_request('PUT', endpoint, json=data)
    
    def get_course_users(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get all users in a course
        
        Args:
            course_id: Canvas course ID
            
        Returns:
            List of course users
        """
        self.logger.info(f"Fetching users for course {course_id}")
        endpoint = f"courses/{course_id}/users"
        
        users = []
        page = 1
        per_page = 100
        
        while True:
            params = {'page': page, 'per_page': per_page}
            response = self._make_request('GET', endpoint, params=params)
            
            if not response:
                break
                
            users.extend(response)
            
            if len(response) < per_page:
                break
                
            page += 1
        
        self.logger.info(f"Retrieved {len(users)} course users")
        return users


class DiscussionProcessor:
    """Process discussion entries and generate grades/comments"""
    
    def __init__(self, canvas_client: CanvasDiscussionsClient):
        self.client = canvas_client
        self.logger = logging.getLogger(__name__)
    
    def analyze_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a discussion entry and generate feedback
        
        Args:
            entry: Discussion entry data from Canvas
            
        Returns:
            Analysis results with suggested grade and comment
        """
        message = entry.get('message', '')
        user_id = entry.get('user_id')
        created_at = entry.get('created_at')
        
        # Simple analysis - you can enhance this with more sophisticated logic
        word_count = len(message.split())
        
        # Basic grading logic (customize as needed)
        if word_count >= 150:
            suggested_grade = "A"
            quality_score = 95
        elif word_count >= 100:
            suggested_grade = "B"
            quality_score = 85
        elif word_count >= 50:
            suggested_grade = "C"
            quality_score = 75
        else:
            suggested_grade = "D"
            quality_score = 65
        
        # Generate feedback comment
        feedback_comment = self._generate_feedback_comment(entry, word_count, quality_score)
        
        return {
            'user_id': user_id,
            'entry_id': entry.get('id'),
            'word_count': word_count,
            'suggested_grade': suggested_grade,
            'quality_score': quality_score,
            'feedback_comment': feedback_comment,
            'created_at': created_at
        }
    
    def _generate_feedback_comment(self, entry: Dict[str, Any], word_count: int, quality_score: int) -> str:
        """
        Generate a feedback comment for a discussion entry
        
        Args:
            entry: Discussion entry data
            word_count: Number of words in the entry
            quality_score: Quality score (0-100)
            
        Returns:
            Generated feedback comment
        """
        base_comment = f"Thank you for your contribution to the discussion. "
        
        if quality_score >= 90:
            base_comment += "Your post demonstrates excellent understanding and thoughtful analysis. "
        elif quality_score >= 80:
            base_comment += "Your post shows good understanding of the topic. "
        elif quality_score >= 70:
            base_comment += "Your post addresses the topic adequately. "
        else:
            base_comment += "Your post could benefit from more detailed analysis. "
        
        if word_count < 50:
            base_comment += "Consider expanding your thoughts with more detailed examples or explanations."
        elif word_count > 200:
            base_comment += "Great detail in your response!"
        
        return base_comment
    
    def process_discussion(self, course_id: int, discussion_id: int, 
                         assignment_id: Optional[int] = None, 
                         post_grades: bool = False, post_comments: bool = False) -> List[Dict[str, Any]]:
        """
        Process all entries in a discussion
        
        Args:
            course_id: Canvas course ID
            discussion_id: Canvas discussion topic ID
            assignment_id: Assignment ID (for graded discussions)
            post_grades: Whether to actually post grades
            post_comments: Whether to actually post comments
            
        Returns:
            List of processing results
        """
        # Get discussion entries
        entries = self.client.get_discussion_entries(course_id, discussion_id)
        results = []
        
        for entry in entries:
            try:
                # Analyze the entry
                analysis = self.analyze_entry(entry)
                results.append(analysis)
                
                # Post comment if requested
                if post_comments and analysis['feedback_comment']:
                    try:
                        self.client.post_discussion_entry(
                            course_id, discussion_id,
                            analysis['feedback_comment'],
                            parent_id=entry['id']
                        )
                        analysis['comment_posted'] = True
                    except Exception as e:
                        self.logger.error(f"Failed to post comment for entry {entry['id']}: {e}")
                        analysis['comment_posted'] = False
                
                # Post grade if requested and assignment_id provided
                if post_grades and assignment_id and analysis['user_id']:
                    try:
                        self.client.grade_discussion_entry(
                            course_id, assignment_id,
                            analysis['user_id'], analysis['suggested_grade'],
                            analysis['feedback_comment']
                        )
                        analysis['grade_posted'] = True
                    except Exception as e:
                        self.logger.error(f"Failed to post grade for user {analysis['user_id']}: {e}")
                        analysis['grade_posted'] = False
                
            except Exception as e:
                self.logger.error(f"Failed to process entry {entry.get('id', 'unknown')}: {e}")
                continue
        
        return results


def load_config():
    """Load configuration from environment variables or config file"""
    config = {
        'canvas_url': os.getenv('CANVAS_URL'),
        'api_key': os.getenv('CANVAS_API_KEY')
    }
    
    # Try to load from config file if environment variables not set
    try:
        if os.path.exists('canvas_config.json'):
            with open('canvas_config.json', 'r') as f:
                file_config = json.load(f)
                for key in config:
                    if config[key] is None and key in file_config:
                        config[key] = file_config[key]
    except Exception as e:
        logging.warning(f"Could not load config file: {e}")
    
    return config


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Canvas Discussions API Client')
    parser.add_argument('--course-id', type=int, required=True, help='Canvas course ID')
    parser.add_argument('--discussion-id', type=int, required=True, help='Canvas discussion topic ID')
    parser.add_argument('--assignment-id', type=int, help='Assignment ID (for graded discussions)')
    parser.add_argument('--post-grades', action='store_true', help='Actually post grades to Canvas')
    parser.add_argument('--post-comments', action='store_true', help='Actually post comments to Canvas')
    parser.add_argument('--canvas-url', help='Canvas instance URL')
    parser.add_argument('--api-key', help='Canvas API key')
    parser.add_argument('--output', help='Output file for results (JSON format)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    canvas_url = args.canvas_url or config['canvas_url']
    api_key = args.api_key or config['api_key']
    
    if not canvas_url or not api_key:
        print("Error: Canvas URL and API key are required")
        print("Set them via --canvas-url and --api-key arguments, or")
        print("Set CANVAS_URL and CANVAS_API_KEY environment variables, or")
        print("Create a canvas_config.json file with these values")
        sys.exit(1)
    
    try:
        # Initialize Canvas client
        canvas_client = CanvasDiscussionsClient(canvas_url, api_key)
        
        # Initialize discussion processor
        processor = DiscussionProcessor(canvas_client)
        
        # Process the discussion
        print(f"Processing discussion {args.discussion_id} in course {args.course_id}")
        results = processor.process_discussion(
            args.course_id, args.discussion_id,
            assignment_id=args.assignment_id,
            post_grades=args.post_grades,
            post_comments=args.post_comments
        )
        
        # Display results
        print(f"\nProcessed {len(results)} discussion entries:")
        for result in results:
            print(f"User ID: {result['user_id']}, Grade: {result['suggested_grade']}, "
                  f"Words: {result['word_count']}, Score: {result['quality_score']}")
        
        # Save results to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results saved to {args.output}")
        
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
