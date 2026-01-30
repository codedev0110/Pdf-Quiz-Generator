# PDF Quiz Generator - MVP

Complete PDF-based quiz application with intelligent question parsing and random selection.

## 🎯 Features

- **PDF Upload & Parsing**: Upload PDF files and automatically extract questions with regex-based parsing
- **Smart Question Extraction**: Supports standard Q&A format (N. Question, A) B) C) D) options)
- **Range Selection**: Select questions from any range within the PDF
- **Random Quiz Generation**: Generate random quizzes from the specified range
- **Beautiful UI**: Modern, responsive interface with Tailwind-inspired styling
- **Fast Backend**: FastAPI with async request handling

## 📁 Project Structure

```
unecai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app & endpoints
│   │   ├── parser.py       # Regex-based question parser
│   │   ├── pdf_handler.py  # PDF storage & text extraction
│   │   └── models.py       # Pydantic models
│   ├── requirements.txt
│   └── pdfs/              # Storage for uploaded PDFs (created at runtime)
│
└── frontend/              # React frontend
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── PDFUpload.js   # Upload form
    │   │   ├── QuizConfig.js  # Question range & count selection
    │   │   └── Quiz.js        # Quiz display & interaction
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    └── package.json
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

API endpoints:
- `GET /` - Health check
- `POST /upload-pdf` - Upload and parse PDF
- `POST /generate-quiz` - Generate random quiz

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## 📝 PDF Format Requirements

The parser expects questions in this format:

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

**Key requirements:**
- Questions start with number followed by dot and space
- Options are prefixed with A) B) C) D)
- Questions must have exactly 4 options

## 🔌 API Examples

### Upload PDF

```bash
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@sample.pdf"
```

Response:
```json
{
  "pdf_id": "abc-123-def",
  "total_questions": 500
}
```

### Generate Quiz

```bash
curl -X POST http://localhost:8000/generate-quiz \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_id": "abc-123-def",
    "start": 100,
    "end": 300,
    "count": 20
  }'
```

Response:
```json
{
  "questions": [
    {
      "id": 145,
      "question": "Example question?",
      "options": ["Option A", "Option B", "Option C", "Option D"]
    }
  ]
}
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI (REST API)
- pdfplumber (PDF parsing)
- Python 3.11
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Axios (HTTP client)
- CSS3 (Vanilla CSS with modern features)

**Storage:**
- Local filesystem (MVP)
- Upgrade to S3/Cloud later

## 📚 Development Notes

### Question Parser

The regex-based parser in `app/parser.py`:
- Uses `r'^\s*(\d+)\.\s+(.+?)$'` to match questions
- Uses `r'^\s*([A-D])\)\s*(.+)$'` to match options
- Handles variable whitespace and formatting

### Limitations (MVP)

- ❌ No user accounts or login
- ❌ No answer checking or scoring
- ❌ No result/statistics saving
- ❌ Limited to single PDF format
- ❌ No PDF annotation or editing

These are planned for V2.

## 🚢 Deployment

### Backend (Railway/Render/Fly.io)

```bash
# Add Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port 8000" > Procfile
```

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy with Vercel CLI
vercel
```

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! This is a portfolio project.

---

**Made with ❤️ for effective learning through spaced repetition.**
