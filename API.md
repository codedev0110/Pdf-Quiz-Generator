# API Documentation

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-backend-url.com`

## Authentication

MVP doesn't require authentication. All endpoints are publicly accessible.

## Endpoints

### 1. Health Check

**Request:**
```http
GET /
```

**Response:**
```json
{
  "message": "PDF Quiz Generator API is running"
}
```

---

### 2. Upload PDF

Upload a PDF file and extract questions from it.

**Request:**
```http
POST /upload-pdf
Content-Type: multipart/form-data

file: <binary PDF file>
```

**Response (200):**
```json
{
  "pdf_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_questions": 500
}
```

**Error Responses:**

- **400** - File is not a PDF
  ```json
  {
    "detail": "File must be a PDF"
  }
  ```

- **500** - PDF parsing failed
  ```json
  {
    "detail": "Error message describing what went wrong"
  }
  ```

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@questions.pdf"
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);

const response = await fetch('http://localhost:8000/upload-pdf', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.pdf_id, data.total_questions);
```

---

### 3. Generate Quiz

Generate a random quiz with questions from a specified range.

**Request:**
```http
POST /generate-quiz
Content-Type: application/json

{
  "pdf_id": "550e8400-e29b-41d4-a716-446655440000",
  "start": 100,
  "end": 300,
  "count": 20
}
```

**Parameters:**
- `pdf_id` (string, required): ID returned from `/upload-pdf`
- `start` (integer, required): First question number (inclusive)
- `end` (integer, required): Last question number (inclusive)
- `count` (integer, required): How many random questions to select

**Response (200):**
```json
{
  "questions": [
    {
      "id": 145,
      "question": "What is the capital of France?",
      "options": [
        "London",
        "Paris",
        "Berlin",
        "Madrid"
      ]
    },
    {
      "id": 273,
      "question": "What is 2+2?",
      "options": [
        "3",
        "4",
        "5",
        "6"
      ]
    }
  ]
}
```

**Error Responses:**

- **404** - PDF not found
  ```json
  {
    "detail": "PDF not found"
  }
  ```

- **400** - Invalid range or insufficient questions
  ```json
  {
    "detail": "Not enough questions in range 100-300. Found 150, requested 200"
  }
  ```

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/generate-quiz \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_id": "550e8400-e29b-41d4-a716-446655440000",
    "start": 100,
    "end": 300,
    "count": 20
  }'
```

**Example (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/generate-quiz', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    pdf_id: "550e8400-e29b-41d4-a716-446655440000",
    start: 100,
    end: 300,
    count: 20
  })
});

const data = await response.json();
data.questions.forEach(q => {
  console.log(q.id, q.question);
  q.options.forEach((opt, i) => {
    console.log(`  ${String.fromCharCode(65 + i)}) ${opt}`);
  });
});
```

---

## Data Models

### PDFUploadResponse

```json
{
  "pdf_id": "string (UUID)",
  "total_questions": "integer"
}
```

### QuizResponse

```json
{
  "questions": [
    {
      "id": "integer",
      "question": "string",
      "options": ["string", "string", "string", "string"]
    }
  ]
}
```

### QuestionResponse

```json
{
  "id": "integer",
  "question": "string",
  "options": ["string", "string", "string", "string"]
}
```

---

## Common Workflows

### Complete Quiz Flow

1. **Upload PDF**
   ```javascript
   const uploadResponse = await fetch('/upload-pdf', {
     method: 'POST',
     body: formData
   });
   const { pdf_id, total_questions } = await uploadResponse.json();
   ```

2. **Generate Quiz**
   ```javascript
   const quizResponse = await fetch('/generate-quiz', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       pdf_id,
       start: 100,
       end: Math.min(300, total_questions),
       count: 20
     })
   });
   const quiz = await quizResponse.json();
   ```

3. **Display Questions**
   - Show `quiz.questions[currentIndex]` to user
   - Let user select an option from `options` array
   - Move to next question

---

## Rate Limiting

MVP has no rate limiting. Production deployment should add:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/upload-pdf")
@limiter.limit("5/minute")
async def upload_pdf(...):
    # ...
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (validation error)
- `404` - Resource not found
- `500` - Server error

---

## CORS Headers

The API allows requests from any origin:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

For production, set specific origins:
```python
allow_origins=["https://yourdomain.com"]
```

---

## Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.
