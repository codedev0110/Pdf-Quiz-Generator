from typing import List
from pydantic import BaseModel


class QuestionResponse(BaseModel):
    """Response model for a single question"""
    id: int
    question: str
    options: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "id": 101,
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"]
            }
        }


class QuizResponse(BaseModel):
    """Response model for quiz generation"""
    questions: List[QuestionResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "questions": [
                    {
                        "id": 101,
                        "question": "What is the capital of France?",
                        "options": ["London", "Paris", "Berlin", "Madrid"]
                    }
                ]
            }
        }


class PDFUploadResponse(BaseModel):
    """Response model for PDF upload"""
    pdf_id: str
    total_questions: int
    
    class Config:
        schema_extra = {
            "example": {
                "pdf_id": "550e8400-e29b-41d4-a716-446655440000",
                "total_questions": 500
            }
        }


class QuizGenerateRequest(BaseModel):
    """Request model for quiz generation"""
    pdf_id: str
    start: int
    end: int
    count: int
    
    class Config:
        schema_extra = {
            "example": {
                "pdf_id": "550e8400-e29b-41d4-a716-446655440000",
                "start": 100,
                "end": 300,
                "count": 20
            }
        }
