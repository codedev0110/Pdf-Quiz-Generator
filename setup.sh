#!/bin/bash

# PDF Quiz Generator - Quick Setup Script
# Run this to set up both backend and frontend

echo "🚀 Setting up PDF Quiz Generator MVP..."

# Backend Setup
echo ""
echo "📦 Setting up Backend..."
cd backend
python -m venv venv

# Activate venv (Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Frontend Setup
echo ""
echo "📦 Setting up Frontend..."
cd ../frontend
npm install
echo "✅ Frontend dependencies installed"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
