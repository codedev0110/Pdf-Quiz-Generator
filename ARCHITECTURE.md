# Architecture & Design Document

## Overview

PDF Quiz Generator is a **PDF-to-Quiz** system that allows users to:
1. Upload PDFs containing questions
2. Automatically extract and parse questions
3. Generate random quizzes from specified ranges
4. Answer quizzes with a clean UI

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         React Frontend (Port 3000)                   │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │ PDFUpload   │  │ QuizConfig   │  │  Quiz      │  │   │
│  │  │ Component   │  │ Component    │  │  Component │  │   │
│  │  └──────┬──────┘  └──────┬───────┘  └────────────┘  │   │
│  │         │                │                           │   │
│  └─────────┼────────────────┼───────────────────────────┘   │
│            │ HTTP/JSON      │                               │
├────────────┼────────────────┼───────────────────────────────┤
│            │                │                               │
│  ┌─────────▼────────────────▼──────────────────────────┐   │
│  │     FastAPI Backend (Port 8000)                     │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  API Endpoints                               │   │   │
│  │  │  • POST /upload-pdf                          │   │   │
│  │  │  • POST /generate-quiz                       │   │   │
│  │  └────────────┬──────────────────────────────────┘   │   │
│  │               │                                      │   │
│  │  ┌────────────▼──────────────────────────────────┐   │   │
│  │  │  Processing Pipeline                         │   │   │
│  │  │  1. PDF Storage (pdf_handler.py)             │   │   │
│  │  │  2. PDF Text Extraction (pdfplumber)         │   │   │
│  │  │  3. Question Parsing (parser.py - regex)     │   │   │
│  │  │  4. Range Filtering & Random Selection       │   │   │
│  │  └────────────┬──────────────────────────────────┘   │   │
│  │               │                                      │   │
│  │  ┌────────────▼──────────────────────────────────┐   │   │
│  │  │  In-Memory Storage (Dict)                    │   │   │
│  │  │  Map: {pdf_id -> List[Questions]}            │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     File System Storage                          │   │
│  │     pdfs/ (uploaded PDF files)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend (React)

**Tech Stack:**
- React 18
- Axios (HTTP client)
- Vanilla CSS with modern features

**Components:**

1. **App.js** (Main orchestrator)
   - Manages state: `currentStep`, `pdfId`, `quiz`
   - Routes between Upload → Config → Quiz

2. **PDFUpload.js**
   - File input with validation
   - Calls `POST /upload-pdf`
   - Returns to QuizConfig on success

3. **QuizConfig.js**
   - Input fields: start, end, count
   - Validation (range checks)
   - Calls `POST /generate-quiz`

4. **Quiz.js**
   - Displays one question at a time
   - Radio button selection for options
   - Previous/Next navigation
   - Progress bar

**Flow:**
```
Upload PDF → Get pdf_id → Select Range → Get Questions → Show Quiz → Next → Finish
```

### Backend (FastAPI)

**Tech Stack:**
- FastAPI (async REST framework)
- pdfplumber (PDF text extraction)
- Pydantic (data validation)
- Python 3.11

**Modules:**

1. **app/main.py** (API Server)
   - Initializes FastAPI app
   - Defines endpoints with CORS
   - Request/response handling

2. **app/pdf_handler.py** (File Management)
   - `save_pdf()` - Store PDF with UUID
   - `extract_text()` - Use pdfplumber to get text
   - `get_pdf_path()` - Retrieve stored PDF path
   - `cleanup_pdf()` - Delete PDF file

3. **app/parser.py** (Question Extraction)
   - Regex patterns:
     - Questions: `r'^\s*(\d+)\.\s+(.+?)$'`
     - Options: `r'^\s*([A-D])\)\s*(.+)$'`
   - `parse_questions()` - Main parsing logic
   - `filter_by_range()` - Filter by question ID range

4. **app/models.py** (Data Schemas)
   - `PDFUploadResponse` - Response from upload
   - `QuizGenerateRequest` - Request for quiz
   - `QuizResponse` - Questions with options
   - `QuestionResponse` - Single question

## Data Flow

### Upload Flow
```
1. User selects PDF file
   ↓
2. Frontend: POST /upload-pdf with file
   ↓
3. Backend:
   - Save PDF file with UUID name
   - Extract text using pdfplumber
   - Parse text with regex parser
   - Store questions in memory
   ↓
4. Response: {pdf_id, total_questions}
   ↓
5. Frontend stores pdf_id and shows QuizConfig
```

### Quiz Generation Flow
```
1. User sets start, end, count
   ↓
2. Frontend: POST /generate-quiz
   ↓
3. Backend:
   - Retrieve parsed questions by pdf_id
   - Filter by range (start ≤ id ≤ end)
   - random.sample() to select N questions
   - Shuffle options order (future enhancement)
   ↓
4. Response: {questions: [{id, question, options}, ...]}
   ↓
5. Frontend displays Quiz component with questions
```

## Question Parsing Logic

**Input (PDF Text):**
```
101. What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid

102. What is 2+2?
A) 3
B) 4
C) 5
D) 6
```

**Parser Algorithm:**
1. Split text by newlines
2. For each line:
   - Match question pattern: `NUMBER. TEXT`
   - Match option pattern: `LETTER) TEXT`
3. Group options with questions
4. Only accept groups with exactly 4 options
5. Return list of `QuestionModel` objects

**Output:**
```python
[
  QuestionModel(
    id=101,
    question="What is the capital of France?",
    options=["London", "Paris", "Berlin", "Madrid"]
  ),
  QuestionModel(
    id=102,
    question="What is 2+2?",
    options=["3", "4", "5", "6"]
  )
]
```

## API Specification

### POST /upload-pdf

**Request:**
```
multipart/form-data
file: <binary PDF>
```

**Response (200):**
```json
{
  "pdf_id": "uuid-string",
  "total_questions": 500
}
```

**Errors:**
- 400: Not a PDF
- 500: Parsing failed

### POST /generate-quiz

**Request:**
```json
{
  "pdf_id": "string",
  "start": 100,
  "end": 300,
  "count": 20
}
```

**Response (200):**
```json
{
  "questions": [
    {
      "id": 145,
      "question": "...",
      "options": ["A", "B", "C", "D"]
    }
  ]
}
```

**Errors:**
- 404: PDF not found
- 400: Invalid range or insufficient questions

## Storage Architecture

### Current (MVP)
```
Frontend (Memory)
↓
Backend (Memory) - Dict[pdf_id -> Questions]
↓
File System - /pdfs/{uuid}.pdf
```

### Future (V2+)
```
Frontend (Memory)
↓
Backend (Memory Cache)
↓
PostgreSQL - Store questions, users, scores
↓
AWS S3 - Store PDF files
↓
Redis - Cache parsed questions
```

## Key Design Decisions

1. **Regex-based Parser**
   - ✅ Simple and fast for MVP
   - ✅ No external dependencies
   - ❌ Limited to specific format
   - Future: Machine learning approach

2. **In-Memory Storage**
   - ✅ Fast, simple
   - ✅ No database setup needed
   - ❌ Data lost on server restart
   - Future: PostgreSQL

3. **UUID for PDF IDs**
   - ✅ Unique globally
   - ✅ No collisions
   - ✅ Cannot guess IDs
   - Considered: Nanoid (shorter)

4. **Random Selection**
   - ✅ Fair distribution
   - ✅ No duplicates within quiz
   - ❌ No weighted difficulty
   - Future: Difficulty-weighted selection

5. **React for Frontend**
   - ✅ Component-based
   - ✅ Large ecosystem
   - ✅ Easy to extend
   - Alternatives: Vue, Svelte

## Error Handling

**Frontend:**
- Try-catch on all API calls
- Display user-friendly errors
- Validation before API calls

**Backend:**
- Pydantic validation
- HTTPException for errors
- Detailed error messages in response
- Logging for debugging

## Performance Considerations

**Optimizations:**
- PDF text cached in memory
- Questions filtered before randomization
- Async request handling
- CORS headers pre-checked

**Bottlenecks (Future):**
- Large PDFs (>100MB) slow parsing
- Many questions (>10k) slow filtering
- Concurrent uploads strain storage

**Solutions:**
- Chunk large PDFs
- Add indexing for questions
- Distribute to multiple workers
- Use CDN for static files

## Security Considerations (MVP)

**Current:**
- ⚠️ No authentication
- ⚠️ No rate limiting
- ⚠️ PDF files on local disk
- ⚠️ No input sanitization

**Future:**
- Add JWT authentication
- Implement rate limiting (slowapi)
- Encrypt files
- Validate PDF content

## Testing Strategy

**Unit Tests:**
- Parser regex patterns
- Range filtering logic
- Model validation

**Integration Tests:**
- Upload → Parse → Quiz flow
- API endpoint responses

**Manual Tests:**
- Various PDF formats
- Edge cases (large files, many questions)

## Deployment Strategy

**MVP (Local):**
- Python venv
- npm install
- Two terminals for backend/frontend

**Production:**
- Backend: Railway.app / Render / Fly.io
- Frontend: Vercel
- Storage: AWS S3
- Database: PostgreSQL (future)

## Future Enhancements (V2+)

1. **Answer Checking**
   - Store correct answers
   - Calculate score
   - Show results

2. **User System**
   - JWT authentication
   - Store user progress
   - Leaderboards

3. **Analytics**
   - Question difficulty
   - Time per question
   - Performance trends

4. **Advanced Features**
   - PDF annotation
   - Custom question creation
   - AI-generated explanations
   - Spaced repetition

## Files and LOC (Lines of Code)

```
backend/
  app/main.py          ~150 LOC - API endpoints
  app/parser.py        ~80 LOC  - Question parsing
  app/pdf_handler.py   ~80 LOC  - PDF management
  app/models.py        ~40 LOC  - Data models
  test_api.py          ~100 LOC - Tests
Total Backend: ~450 LOC

frontend/
  src/App.js           ~60 LOC  - Main component
  src/components/PDFUpload.js    ~50 LOC
  src/components/QuizConfig.js   ~50 LOC
  src/components/Quiz.js         ~80 LOC
  src/App.css          ~150 LOC - Styling
Total Frontend: ~390 LOC

Total MVP: ~840 LOC
```

## Conclusion

The PDF Quiz Generator is a well-architected MVP that:
- ✅ Solves the core problem (PDF → Quiz)
- ✅ Has clean, maintainable code
- ✅ Follows best practices
- ✅ Is easily extensible
- ✅ Is portfolio-ready

Perfect for demonstrating:
- Backend API design
- Frontend state management
- PDF processing
- Regex parsing
- Cloud deployment
