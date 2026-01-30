import re
from typing import List, Dict, Optional
from pydantic import BaseModel


class QuestionModel(BaseModel):
    """Model for a quiz question with options"""
    id: int
    question: str
    options: List[str]


class PDFQuestionParser:
    """Regex-based parser for extracting questions from PDF text"""
    
    def __init__(self):
        # Pattern: number. question text
        self.question_pattern = r'^\s*(\d+)\.\s+(.+?)$'
        # Pattern: A) B) C) D) options
        self.option_pattern = r'^\s*([A-D])\)\s*(.+)$'
    
    def parse_questions(self, text: str) -> List[QuestionModel]:
        """
        Parse PDF text and extract questions with options.
        
        Expected format:
        101. Question text here?
        A) Option A
        B) Option B
        C) Option C
        D) Option D
        
        102. Another question?
        ...
        """
        lines = text.split('\n')
        questions = []
        current_question = None
        current_options = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a question
            question_match = re.match(self.question_pattern, line)
            if question_match:
                # Save previous question if exists
                if current_question is not None and len(current_options) == 4:
                    questions.append(QuestionModel(
                        id=current_question['id'],
                        question=current_question['text'],
                        options=[current_options[opt] for opt in 'ABCD']
                    ))
                
                # Start new question
                q_id = int(question_match.group(1))
                q_text = question_match.group(2).strip()
                current_question = {'id': q_id, 'text': q_text}
                current_options = {}
            
            # Check if line is an option
            elif current_question is not None:
                option_match = re.match(self.option_pattern, line)
                if option_match:
                    option_letter = option_match.group(1)
                    option_text = option_match.group(2).strip()
                    current_options[option_letter] = option_text
        
        # Don't forget the last question
        if current_question is not None and len(current_options) == 4:
            questions.append(QuestionModel(
                id=current_question['id'],
                question=current_question['text'],
                options=[current_options[opt] for opt in 'ABCD']
            ))
        
        return questions
    
    def filter_by_range(self, questions: List[QuestionModel], 
                       start: int, end: int) -> List[QuestionModel]:
        """Filter questions by ID range"""
        return [q for q in questions if start <= q.id <= end]
