import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import Dict, List

from app.parser import PDFQuestionParser, QuestionModel
from app.pdf_handler import PDFHandler
from app.models import (
    QuizGenerateRequest,
    QuizResponse,
    QuestionResponse,
    PDFUploadResponse
)

app = FastAPI(title="PDF Quiz Generator API", version="1.0.0")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handlers
pdf_handler = PDFHandler()
parser = PDFQuestionParser()

# In-memory storage for parsed questions (for MVP)
# In production, use database
parsed_questions: Dict[str, List[QuestionModel]] = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "PDF Quiz Generator API is running"}


@app.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and parse PDF file.
    
    Returns:
        - pdf_id: Unique identifier for the uploaded PDF
        - total_questions: Total number of questions extracted
    """
    try:
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        content = await file.read()
        
        # Save PDF
        pdf_id = pdf_handler.save_pdf(file.filename, content)
        
        # Extract and parse questions
        text = pdf_handler.extract_text(pdf_id)
        questions = parser.parse_questions(text)
        
        # Store parsed questions
        parsed_questions[pdf_id] = questions
        
        return PDFUploadResponse(
            pdf_id=pdf_id,
            total_questions=len(questions)
        )
    
    except Exception as e:
        # Clean up on error
        if 'pdf_id' in locals():
            pdf_handler.cleanup_pdf(pdf_id)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizGenerateRequest):
    """
    Generate a quiz with randomly selected questions from a specific range.
    
    Request body:
        - pdf_id: ID of the uploaded PDF
        - start: Start of question range (inclusive)
        - end: End of question range (inclusive)
        - count: Number of random questions to select
    
    Returns:
        - questions: List of randomly selected questions with options
    """
    # Validate PDF exists
    if request.pdf_id not in parsed_questions:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    questions = parsed_questions[request.pdf_id]
    
    # Filter by range
    filtered = parser.filter_by_range(questions, request.start, request.end)
    
    # Validate range has enough questions
    if len(filtered) < request.count:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough questions in range {request.start}-{request.end}. "
                   f"Found {len(filtered)}, requested {request.count}"
        )
    
    # Random selection
    selected = random.sample(filtered, request.count)
    
    # Convert to response format
    response_questions = [
        QuestionResponse(
            id=q.id,
            question=q.question,
            options=q.options
        )
        for q in selected
    ]
    
    return QuizResponse(questions=response_questions)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
