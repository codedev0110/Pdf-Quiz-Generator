# Quick Start Checklist

Follow these steps to run the PDF Quiz Generator locally.

## ✅ Prerequisites

- Python 3.11+
- Node.js 16+
- Git

## 🚀 Step 1: Clone & Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the parser (optional but recommended)
python test_parser.py

# You should see ✅ and parsed questions output
```

## 🚀 Step 2: Start Backend Server

```bash
# From backend directory (with venv activated)
python -m uvicorn app.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# 
# Visit http://localhost:8000/docs to see interactive API docs
```

**Keep this terminal open!**

## 🚀 Step 3: Setup Frontend (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# This takes 2-3 minutes the first time
```

## 🚀 Step 4: Start Frontend Server

```bash
# From frontend directory
npm start

# Expected output:
# Compiled successfully!
# You can now view quiz-frontend in the browser.
# Local: http://localhost:3000

# Your browser should automatically open
```

## ✅ Testing the Application

### Via Web UI

1. **Open http://localhost:3000** in your browser
2. **Upload a PDF** with questions in this format:
   ```
   101. Question text?
   A) Option A
   B) Option B
   C) Option C
   D) Option D
   
   102. Another question?
   A) Option A
   B) Option B
   C) Option C
   D) Option D
   ```
3. **Configure quiz**:
   - Set start question (e.g., 101)
   - Set end question (e.g., 120)
   - Set number of questions (e.g., 10)
4. **Click "Generate Quiz"**
5. **Answer questions** and click "Next"
6. **Click "Finish Quiz"**

### Via API (cURL)

**1. Upload PDF:**
```bash
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@your_questions.pdf"

# Response:
# {
#   "pdf_id": "abc-123-def",
#   "total_questions": 500
# }
```

**2. Generate Quiz:**
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

### Via Interactive Docs

Visit **http://localhost:8000/docs**
- Click "Try it out" on any endpoint
- Fill in parameters
- Click "Execute"

## 🛑 Troubleshooting

### Port Already in Use

```bash
# Kill process using port 8000 (backend)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Frontend can't connect to Backend

- Ensure backend is running on http://localhost:8000
- Check that CORS is enabled (should be by default)
- Check browser console for errors (F12)

### PDF parsing shows no questions

- Verify PDF has standard Q&A format
- Questions must start with number (e.g., "101.")
- Options must be "A) B) C) D)"
- See PDF Format Requirements in README.md

### npm install fails

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and try again
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [API.md](API.md) for API reference
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Explore the code in `backend/app/` and `frontend/src/`

## 🎓 Understanding the Architecture

```
User Browser (React)
    ↓
PDFUpload Component
    ↓
HTTP POST /upload-pdf
    ↓
FastAPI Backend
    ↓
pdfplumber (extract text)
    ↓
Regex Parser (extract questions)
    ↓
Return json with pdf_id & total_questions
    ↓
User selects range & count
    ↓
HTTP POST /generate-quiz
    ↓
Backend filters by range
    ↓
random.sample() selects N questions
    ↓
Return JSON with questions
    ↓
Quiz Component displays & handles answers
```

## 💡 Key Files to Understand

- `backend/app/main.py` - API endpoints
- `backend/app/parser.py` - Question parsing logic
- `frontend/src/App.js` - Main frontend component
- `frontend/src/components/Quiz.js` - Quiz display logic

## 🚀 Ready to Deploy?

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Railway.app setup
- Render.com setup
- Fly.io setup
- Vercel frontend deployment

---

**Questions?** Check the docs or review the code comments!
