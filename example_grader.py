#!/usr/bin/env python3
"""
Example Grading Script

This is an example external grader that demonstrates the interface expected 
by canvas_speedgrader.py.

Input: JSON submission data via stdin
Output: JSON grading result via stdout

The grader receives complete submission data and must output:
{
  "grade": "A" or "85" or "Pass", 
  "comment": "Optional feedback comment"
}

This example implements simple word-count based grading, but you can 
replace this with any grading logic you want.
"""

import json
import sys
import re
from typing import Dict, Any


def analyze_submission(submission_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a discussion submission and return grade + feedback
    
    Args:
        submission_data: Complete submission information from Canvas
        
    Returns:
        Dictionary with 'grade' and optional 'comment'
    """
    # Extract submission details
    discussion = submission_data['discussion']
    student = submission_data['student']
    submission = submission_data['submission']
    
    message = submission['message']
    word_count = submission['word_count']
    
    # Example grading logic - customize this as needed
    
    # Basic metrics
    sentence_count = len([s for s in re.split(r'[.!?]+', message) if s.strip()])
    paragraph_count = len([p for p in message.split('\n\n') if p.strip()])
    
    # Look for specific content indicators
    has_examples = any(word in message.lower() for word in ['example', 'for instance', 'such as'])
    has_analysis = any(word in message.lower() for word in ['because', 'therefore', 'however', 'analysis'])
    has_citations = bool(re.search(r'\([^)]*\d{4}[^)]*\)', message))  # Simple citation pattern
    
    # Grading rubric (customize as needed)
    points = 0
    feedback_parts = []
    
    # Word count criterion (40 points max)
    if word_count >= 200:
        points += 40
        feedback_parts.append("Excellent length and detail in your response.")
    elif word_count >= 150:
        points += 35
        feedback_parts.append("Good length - substantial response.")
    elif word_count >= 100:
        points += 25
        feedback_parts.append("Adequate length, but could use more detail.")
    else:
        points += 15
        feedback_parts.append("Response is quite brief - consider expanding your analysis.")
    
    # Content quality (30 points max)
    content_score = 0
    if has_examples:
        content_score += 10
        feedback_parts.append("Good use of examples to support your points.")
    if has_analysis:
        content_score += 15
        feedback_parts.append("Shows analytical thinking and reasoning.")
    if has_citations:
        content_score += 5
        feedback_parts.append("Nice inclusion of citations/references.")
    
    points += content_score
    if content_score < 10:
        feedback_parts.append("Consider adding more examples or analytical depth.")
    
    # Structure criterion (20 points max)
    structure_score = 0
    if paragraph_count > 1:
        structure_score += 10
        feedback_parts.append("Well-organized with multiple paragraphs.")
    if sentence_count >= 8:
        structure_score += 10
        feedback_parts.append("Good sentence variety and complexity.")
    
    points += structure_score
    if structure_score < 15:
        feedback_parts.append("Consider improving organization and sentence structure.")
    
    # Engagement with prompt (10 points max)
    prompt_keywords = extract_keywords_from_prompt(discussion.get('prompt', ''))
    engagement_score = 0
    for keyword in prompt_keywords[:3]:  # Check top 3 keywords from prompt
        if keyword.lower() in message.lower():
            engagement_score += 3
    
    points = min(points + engagement_score, 100)  # Cap at 100
    
    if engagement_score > 5:
        feedback_parts.append("Excellent engagement with the discussion prompt.")
    else:
        feedback_parts.append("Consider addressing the key points from the prompt more directly.")
    
    # Convert points to letter grade
    if points >= 90:
        grade = "A"
    elif points >= 80:
        grade = "B"
    elif points >= 70:
        grade = "C"
    elif points >= 60:
        grade = "D"
    else:
        grade = "F"
    
    # Construct feedback comment
    comment_parts = [f"Hi {student['name'].split()[0]},"]
    comment_parts.extend(feedback_parts)
    comment_parts.append(f"Total score: {points}/100 ({grade})")
    
    comment = " ".join(comment_parts)
    
    return {
        "grade": grade,
        "comment": comment,
        "points": points,
        "metrics": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "has_examples": has_examples,
            "has_analysis": has_analysis,
            "has_citations": has_citations,
            "engagement_score": engagement_score
        }
    }


def extract_keywords_from_prompt(prompt: str) -> list:
    """
    Extract key terms from the discussion prompt
    
    Args:
        prompt: The discussion prompt text
        
    Returns:
        List of important keywords
    """
    # Simple keyword extraction - you could use more sophisticated NLP
    # Remove HTML tags
    clean_prompt = re.sub(r'<[^>]+>', '', prompt)
    
    # Split into words and filter
    words = re.findall(r'\b[a-zA-Z]{4,}\b', clean_prompt.lower())
    
    # Filter out common words
    stop_words = {
        'this', 'that', 'with', 'have', 'will', 'from', 'they', 'know',
        'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when',
        'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over',
        'such', 'take', 'than', 'them', 'well', 'were', 'what', 'your'
    }
    
    keywords = [word for word in words if word not in stop_words]
    
    # Return most frequent words (simple frequency analysis)
    from collections import Counter
    word_freq = Counter(keywords)
    return [word for word, count in word_freq.most_common(10)]


def main():
    """Main grading function"""
    try:
        # Read submission data from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            raise ValueError("No input data received")
        
        submission_data = json.loads(input_data)
        
        # Grade the submission
        result = analyze_submission(submission_data)
        
        # Output result as JSON to stdout
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error in JSON format so the main script can handle it
        error_result = {
            "error": str(e),
            "grade": "0",  # Default failing grade
            "comment": f"Grading error: {str(e)}"
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
