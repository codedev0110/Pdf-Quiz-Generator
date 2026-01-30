# 🎯 Quick Reference Card

## Project: PDF Quiz Generator MVP

**Status:** ✅ Complete & Ready to Use  
**Setup Time:** ~5 minutes  
**First Quiz:** ~2 minutes  

---

## 🚀 Start Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Access at:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

---

## 🚀 Start Frontend

```bash
cd frontend
npm install
npm start
```

**Access at:** http://localhost:3000

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | API endpoints |
| `backend/app/parser.py` | Question extraction |
| `frontend/src/App.js` | Main React component |
| `frontend/src/components/Quiz.js` | Quiz UI |

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/upload-pdf` | Upload and parse PDF |
| `POST` | `/generate-quiz` | Generate random quiz |
| `GET` | `/` | Health check |

---

## 🧪 Test Parser

```bash
cd backend
python test_parser.py
```

Expected: 5 questions parsed successfully ✅

---

## 📝 PDF Format (Required)

```
101. Question text here?
A) Option A
B) Option B
C) Option C
D) Option D

102. Another question?
A) Option 1
B) Option 2
C) Option 3
D) Option 4
```

**Rules:**
- Questions start with number + dot
- Exactly 4 options (A, B, C, D)
- One question per group

---

## 🎨 UI Workflow

```
Upload PDF → See total questions
    ↓
Set range & count → "Generate Quiz"
    ↓
Answer questions → Click "Next"
    ↓
Finish quiz → Back to upload
```

---

## 🛠️ Common Commands

```bash
# Kill port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Clear npm cache
npm cache clean --force

# Check Python version
python --version

# Check Node version
node --version
```

---

## 📚 Documentation Map

| Document | Content |
|----------|---------|
| [README.md](README.md) | Overview & features |
| [QUICKSTART.md](QUICKSTART.md) | Setup steps |
| [API.md](API.md) | Endpoint reference |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deploy to cloud |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Dev guide |
| [EXAMPLES.md](EXAMPLES.md) | Code examples |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview |

---

## 🔐 Deployment Checklist

- [ ] Tests pass locally
- [ ] No console errors (F12)
- [ ] Backend on Railway/Render
- [ ] Frontend on Vercel
- [ ] Update API URL in frontend
- [ ] Test production URLs
- [ ] Add environment variables
- [ ] Enable HTTPS

---

## 🐛 Troubleshooting

### Backend Won't Start
```
Error: Port 8000 in use
→ Kill process: taskkill /PID <PID> /F

Error: ModuleNotFoundError
→ Install deps: pip install -r requirements.txt
```

### Frontend Won't Start
```
Error: npm ERR!
→ Clear cache: npm cache clean --force
→ Reinstall: npm install

Error: Cannot connect to backend
→ Check backend is running
→ Check CORS settings
```

### PDF Not Parsing
```
Check:
- Is it a valid PDF?
- Does it have standard Q&A format?
- Are there exactly 4 options per question?
```

---

## 💻 Tech Stack

**Backend:** FastAPI, Python 3.11, pdfplumber, Pydantic  
**Frontend:** React 18, Axios, CSS3  
**Deployment:** Railway/Render (backend), Vercel (frontend)

---

## 📊 Project Stats

- **Total LOC:** ~1,200+
- **Backend Files:** 5
- **Frontend Files:** 6
- **Documentation:** 8 pages
- **Setup Time:** <5 minutes
- **Time to First Quiz:** <2 minutes

---

## 🚀 Next Steps

1. **Try it locally** - Follow QUICKSTART.md
2. **Understand the code** - Read ARCHITECTURE.md
3. **Deploy to cloud** - Follow DEPLOYMENT.md
4. **Add features** - See DEVELOPMENT.md

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Pydantic](https://docs.pydantic.dev/)

---

## ✅ What's Included

✅ Complete backend with async API  
✅ React frontend with modern UI  
✅ PDF parsing with regex  
✅ Question extraction & filtering  
✅ Random quiz generation  
✅ Comprehensive documentation  
✅ Sample tests  
✅ Error handling throughout  

---

## ❌ Not Included (MVP)

❌ User authentication  
❌ Answer checking/scoring  
❌ Result persistence  
❌ Statistics/analytics  
❌ Multi-format PDF support  

**These are planned for V2.**

---

## 📞 Support

- **Setup issues?** → See QUICKSTART.md
- **API questions?** → See API.md
- **Architecture?** → See ARCHITECTURE.md
- **Deployment?** → See DEPLOYMENT.md
- **Development?** → See DEVELOPMENT.md

---

## 🎉 You're All Set!

Your PDF Quiz Generator is **ready to go**.

```bash
# 2 terminals, 2 commands:
python -m uvicorn app.main:app --reload
npm start

# Then: http://localhost:3000
```

**Enjoy!** 🚀

---

**Made with ❤️ for better learning**

Last Updated: January 29, 2026
