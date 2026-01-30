import React, { useState } from 'react';
import axios from 'axios';
import PDFUpload from './components/PDFUpload';
import QuizConfig from './components/QuizConfig';
import Quiz from './components/Quiz';
import './App.css';

function App() {
  const [currentStep, setCurrentStep] = useState('upload'); // upload, config, quiz
  const [pdfId, setPdfId] = useState(null);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePdfUploaded = (pdfId, total) => {
    setPdfId(pdfId);
    setTotalQuestions(total);
    setCurrentStep('config');
  };

  const handleQuizConfigured = async (config) => {
    setLoading(true);
    try {
      const response = await axios.post('/generate-quiz', {
        pdf_id: pdfId,
        start: config.start,
        end: config.end,
        count: config.count,
      });
      setQuiz(response.data);
      setCurrentStep('quiz');
    } catch (error) {
      alert('Failed to generate quiz: ' + error.response?.data?.detail || error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizComplete = () => {
    // For MVP, just go back to upload
    setCurrentStep('upload');
    setPdfId(null);
    setQuiz(null);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>📚 PDF Quiz Generator</h1>

        {currentStep === 'upload' && (
          <PDFUpload onPdfUploaded={handlePdfUploaded} />
        )}

        {currentStep === 'config' && (
          <QuizConfig
            totalQuestions={totalQuestions}
            onConfigure={handleQuizConfigured}
            loading={loading}
          />
        )}

        {currentStep === 'quiz' && quiz && (
          <Quiz
            questions={quiz.questions}
            onComplete={handleQuizComplete}
          />
        )}
      </div>
    </div>
  );
}

export default App;
