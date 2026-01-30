# Development Guide

## Project Overview

**PDF Quiz Generator** is an MVP application that converts PDF documents into interactive quizzes with random question selection from specified ranges.

**Goal:** Allow users to upload PDFs with Q&A content, then generate random quizzes for testing.

## Getting Started

### 1. Initial Setup (One-time)

```bash
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Then visit:** http://localhost:3000

## Project Structure

```
unecai/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── __init__.py              # Package marker
│   │   ├── main.py                  # API endpoints & app setup
│   │   ├── parser.py                # Regex-based question parser
│   │   ├── pdf_handler.py           # PDF storage & extraction
│   │   └── models.py                # Pydantic data models
│   ├── requirements.txt             # Python dependencies
│   ├── test_api.py                  # Basic tests
│   ├── test_parser.py               # Parser functionality tests
│   └── pdfs/                        # Storage (created at runtime)
│
├── frontend/                         # React frontend
│   ├── public/
│   │   └── index.html               # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── PDFUpload.js        # Upload component
│   │   │   ├── QuizConfig.js       # Configuration component
│   │   │   └── Quiz.js             # Quiz display component
│   │   ├── App.js                   # Main app component
│   │   ├── App.css                  # Global styling
│   │   └── index.js                 # React entry point
│   └── package.json                 # npm dependencies
│
├── README.md                        # Main documentation
├── QUICKSTART.md                    # Quick start guide
├── API.md                           # API reference
├── ARCHITECTURE.md                  # Architecture & design
├── DEPLOYMENT.md                    # Deployment guide
├── .gitignore                       # Git ignore rules
└── .vscode/settings.json            # VS Code settings
```

## Detailed File Descriptions

### Backend Files

#### `app/main.py` (API Server)
- **Imports:** FastAPI, File, UploadFile, CORS, random
- **Initializes:** FastAPI app, PDF handler, Question parser
- **Endpoints:**
  - `GET /` - Health check
  - `POST /upload-pdf` - Upload and parse PDF
  - `POST /generate-quiz` - Generate random quiz
- **Key functions:**
  - `upload_pdf()` - Save PDF, extract text, parse questions
  - `generate_quiz()` - Filter range, randomize, return questions

#### `app/parser.py` (Question Extraction)
- **Class:** `PDFQuestionParser`
- **Regex patterns:**
  - Question: `r'^\s*(\d+)\.\s+(.+?)$'` (matches "101. Question text?")
  - Option: `r'^\s*([A-D])\)\s*(.+)$'` (matches "A) Option text")
- **Methods:**
  - `parse_questions(text)` - Main parsing logic
  - `filter_by_range(questions, start, end)` - Filter by ID range
- **Returns:** List of `QuestionModel` objects

#### `app/pdf_handler.py` (File Management)
- **Class:** `PDFHandler`
- **Constructor:** Takes storage directory path
- **Methods:**
  - `save_pdf(filename, content)` - Save PDF with UUID, returns pdf_id
  - `extract_text(pdf_id)` - Use pdfplumber to extract all text
  - `get_pdf_path(pdf_id)` - Get file path for a PDF ID
  - `cleanup_pdf(pdf_id)` - Delete PDF file
- **Storage:** Uses UUID filenames for security

#### `app/models.py` (Data Validation)
- **Models:**
  - `PDFUploadResponse` - Response from `/upload-pdf` endpoint
  - `QuizGenerateRequest` - Request body for `/generate-quiz`
  - `QuestionResponse` - Single question with options
  - `QuizResponse` - List of questions
  - `QuestionModel` - Internal question representation

### Frontend Files

#### `src/App.js` (Main Component)
- **State management:**
  - `currentStep` - "upload" | "config" | "quiz"
  - `pdfId` - UUID from backend
  - `totalQuestions` - Count from backend
  - `quiz` - Questions from API
- **Handlers:**
  - `handlePdfUploaded()` - Move to config step
  - `handleQuizConfigured()` - Call API to generate quiz
  - `handleQuizComplete()` - Reset to upload step
- **Component hierarchy:**
  ```
  App
  ├── (if upload) → PDFUpload
  ├── (if config) → QuizConfig
  └── (if quiz) → Quiz
  ```

#### `src/components/PDFUpload.js` (Upload Form)
- **State:**
  - `file` - Selected PDF file
  - `loading` - Upload in progress
  - `error` - Error message
- **Features:**
  - File type validation (PDF only)
  - File selection feedback
  - Loading spinner
  - Error display
- **API call:**
  ```javascript
  POST /upload-pdf
  Content-Type: multipart/form-data
  ```

#### `src/components/QuizConfig.js` (Range Selection)
- **State:**
  - `start` - Start question number
  - `end` - End question number
  - `count` - Number of questions to select
  - `error` - Validation errors
- **Validations:**
  - Start ≥ 1
  - End ≤ totalQuestions
  - Start ≤ End
  - Count ≤ (end - start + 1)
- **API call:**
  ```javascript
  POST /generate-quiz
  Content-Type: application/json
  {
    "pdf_id": "...",
    "start": 100,
    "end": 300,
    "count": 20
  }
  ```

#### `src/components/Quiz.js` (Quiz Display)
- **State:**
  - `currentIndex` - Current question index
  - `answers` - User answers {question_id: optionIndex}
- **Features:**
  - Question display with number
  - 4 radio button options
  - Progress bar
  - Previous/Next buttons
  - Finish button on last question
- **Styling:** Quiz.css for component-specific styles

#### `src/App.css` (Global Styling)
- **Features:**
  - Gradient background
  - Card-based layout
  - Smooth animations
  - Form styling
  - Button states (hover, disabled)
  - Responsive design
  - Loading spinner

#### `src/components/Quiz.css` (Quiz Styling)
- **Features:**
  - Progress bar animation
  - Radio button customization
  - Option hover effects
  - Navigation button styling
  - Question formatting

## Development Workflow

### Adding a New Feature

1. **Backend Feature:**
   ```python
   # 1. Add to parser.py or create new module
   # 2. Add tests in test_api.py
   # 3. Add endpoint in main.py
   # 4. Update models.py if needed
   ```

2. **Frontend Feature:**
   ```javascript
   // 1. Create component in src/components/
   // 2. Add to App.js
   // 3. Add CSS styling
   // 4. Test in browser
   ```

### Testing Locally

```bash
# Backend tests
cd backend
python test_parser.py
python test_api.py

# Frontend testing
cd frontend
# Open DevTools (F12) to see console errors
# React DevTools extension helpful
```

### Debugging

**Backend:**
```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Or use print statements (not ideal for production)
print(f"Current PDF: {pdf_id}")
```

**Frontend:**
```javascript
// Browser console
console.log("Debug message", variable);

// Network tab - see API calls
// Application tab - see local storage
```

## Common Tasks

### Updating Dependencies

**Backend:**
```bash
cd backend
# Add new package
pip install new_package
# Save to requirements
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install package-name
# OR update existing
npm update
```

### Creating Sample PDF

Use the `test_parser.py` script which includes sample questions:

```python
sample_text = """
101. What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid
"""
```

### Extending the Parser

To support different PDF formats:

1. **Add new regex patterns** in `parser.py`:
   ```python
   # Alternative question pattern
   self.alt_question_pattern = r'^\s*Q[\d\.]+\s+(.+?)$'
   ```

2. **Create format detection** logic:
   ```python
   def detect_format(text):
       if re.search(self.question_pattern, text):
           return "standard"
       elif re.search(self.alt_question_pattern, text):
           return "alternative"
   ```

3. **Use appropriate parser** for format

### Adding Answer Key Support

1. **Extend model** in `models.py`:
   ```python
   class QuestionModel(BaseModel):
       id: int
       question: str
       options: List[str]
       correct_answer: str  # NEW
   ```

2. **Update parser** to extract answers:
   ```python
   # Look for format: "Answer: B"
   answer_pattern = r'Answer:\s*([A-D])'
   ```

3. **Add scoring endpoint** in `main.py`:
   ```python
   @app.post("/check-answers")
   async def check_answers(request):
       # Compare user answers with correct answers
       # Calculate score
   ```

## Performance Tips

- **Large PDFs:** Use streaming if >100MB
- **Many Questions:** Add pagination to frontend
- **Slow Parsing:** Consider caching parsed questions
- **Database:** Replace dict with real DB for production

## Debugging Common Issues

### PDF Upload Fails
```python
# Check PDF validity
import pdfplumber
try:
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                print("Empty page detected")
except Exception as e:
    print(f"PDF error: {e}")
```

### Questions Not Parsing
```python
# Debug regex patterns
import re
pattern = r'^\s*(\d+)\.\s+(.+?)$'
test_line = "101. Question text?"
match = re.match(pattern, test_line)
print(f"Match: {match.groups() if match else 'No match'}")
```

### API Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check logs
# Windows: Look at terminal output
# Check for errors like port already in use
```

### Frontend Can't Connect
```javascript
// Check API URL in axios calls
console.log('API URL:', 'http://localhost:8000');

// Check CORS headers
// F12 → Network → request → Response Headers
// Should have Access-Control-Allow-Origin
```

## Best Practices

1. **Always validate inputs** - Both backend and frontend
2. **Handle errors gracefully** - Show user-friendly messages
3. **Use proper HTTP status codes** - 200, 400, 404, 500
4. **Test locally first** - Before pushing to production
5. **Keep components small** - Each component does one thing
6. **Reuse code** - DRY principle
7. **Document changes** - Update README when adding features
8. **Use meaningful names** - Function and variable names

## Deployment Checklist

Before deploying to production:

- [ ] All tests pass locally
- [ ] No console errors in browser (F12)
- [ ] No errors in terminal output
- [ ] Environment variables set correctly
- [ ] CORS configured for production domains
- [ ] PDF storage path accessible
- [ ] Database configured (if not MVP)
- [ ] Logging enabled
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] SSL/HTTPS enabled

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Need help?** Check the code comments, read ARCHITECTURE.md, or review specific API documentation.
