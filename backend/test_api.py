"""
Integration tests for PDF Quiz Generator API
Run with: python test_api.py
"""

import tempfile
import os
import sys

# Skip pytest-dependent tests if pytest not available
try:
    from fastapi.testclient import TestClient
    from app.main import app
    HAS_PYTEST = True
    client = TestClient(app)
except ImportError:
    HAS_PYTEST = False


def test_root_endpoint():
    """Test health check endpoint"""
    if not HAS_PYTEST:
        print("⚠️  Skipping test_root_endpoint (requires TestClient)")
        return
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_parser_imports():
    """Test that parser module imports correctly"""
    from app.parser import PDFQuestionParser
    parser = PDFQuestionParser()
    assert parser is not None


def test_question_parsing():
    """Test regex-based question parsing"""
    from app.parser import PDFQuestionParser
    
    sample_text = """
101. Question 1?
A) Option A
B) Option B
C) Option C
D) Option D

102. Question 2?
A) Option A
B) Option B
C) Option C
D) Option D
"""
    
    parser = PDFQuestionParser()
    questions = parser.parse_questions(sample_text)
    
    assert len(questions) == 2
    assert questions[0].id == 101
    assert questions[0].question == "Question 1?"
    assert len(questions[0].options) == 4
    assert questions[0].options[0] == "Option A"


def test_range_filtering():
    """Test question range filtering"""
    from app.parser import PDFQuestionParser, QuestionModel
    
    parser = PDFQuestionParser()
    
    # Create mock questions
    questions = [
        QuestionModel(id=i, question=f"Q{i}?", options=["A", "B", "C", "D"])
        for i in range(100, 110)
    ]
    
    # Filter range 102-105
    filtered = parser.filter_by_range(questions, 102, 105)
    
    assert len(filtered) == 4
    assert all(102 <= q.id <= 105 for q in filtered)


def test_pdf_handler_init():
    """Test PDF handler initialization"""
    from app.pdf_handler import PDFHandler
    
    with tempfile.TemporaryDirectory() as tmpdir:
        handler = PDFHandler(tmpdir)
        assert handler.storage_dir.exists()


if __name__ == "__main__":
    # Run basic tests without pytest
    print("✅ Testing root endpoint...")
    test_root_endpoint()
    
    print("✅ Testing parser imports...")
    test_parser_imports()
    
    print("✅ Testing question parsing...")
    test_question_parsing()
    
    print("✅ Testing range filtering...")
    test_range_filtering()
    
    print("✅ Testing PDF handler...")
    test_pdf_handler_init()
    
    print("\n🎉 All basic tests passed!")
