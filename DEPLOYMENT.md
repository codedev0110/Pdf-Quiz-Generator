# Deployment Guide

## Local Development

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API docs will be available at: http://localhost:8000/docs

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at: http://localhost:3000

## Production Deployment

### Option 1: Railway.app (Recommended for this project)

**Backend:**

1. Push code to GitHub
2. Sign up at [railway.app](https://railway.app)
3. Create new project → Import from GitHub
4. Select backend folder
5. Railway auto-detects Python and creates `Procfile`
6. Add environment variables if needed
7. Deploy

**Frontend:**

Deploy separately to Vercel for better performance.

### Option 2: Render.com

**Backend:**

1. Push to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Option 3: Fly.io

```bash
# Install Fly CLI
brew install flyctl

# From backend directory
flyctl launch
flyctl deploy
```

### Frontend Deployment: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# From frontend directory
cd frontend
vercel

# Connect your GitHub repo when prompted
```

**Important:** Update API endpoint in `frontend/src/App.js`:

```javascript
// Change proxy in package.json to actual backend URL
// OR set REACT_APP_API_URL environment variable
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## Environment Variables

Create `.env` file in backend:

```env
# Optional configuration
PDF_STORAGE_PATH=pdfs
MAX_PDF_SIZE=104857600  # 100MB
```

## Docker Deployment (Optional)

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/pdfs:/app/pdfs

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

Run with: `docker-compose up`

## Troubleshooting

### CORS Issues

If frontend can't communicate with backend:

1. Check backend CORS settings in `app/main.py`
2. Ensure `allow_origins=["*"]` or set specific domain
3. Verify backend URL in frontend code

### PDF Upload Fails

- Check file size limits
- Ensure PDF is valid and readable
- Check disk space on server

### Port Already in Use

```bash
# Kill process on port 8000 (backend)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

## Monitoring & Logging

For production, add logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    logger.info(f"Uploading file: {file.filename}")
    # ... rest of code
```

## Performance Tips

1. **Caching**: Add Redis for parsed questions
2. **Database**: Move from in-memory to PostgreSQL
3. **CDN**: Serve frontend from CDN
4. **PDF Optimization**: Consider chunking large PDFs
5. **Rate Limiting**: Add rate limiting for API endpoints

---

**Next steps after MVP:**
- Add user authentication
- Implement persistent storage (PostgreSQL)
- Add answer checking and scoring
- Create analytics/statistics dashboard
