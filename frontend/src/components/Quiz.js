import React, { useState } from 'react';
import './Quiz.css';

function Quiz({ questions, onComplete }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  const currentQuestion = questions[currentIndex];
  const isLastQuestion = currentIndex === questions.length - 1;

  const handleOptionSelect = (optionIndex) => {
    setAnswers({
      ...answers,
      [currentQuestion.id]: optionIndex,
    });
  };

  const handleNext = () => {
    if (isLastQuestion) {
      // For MVP, we don't show results, just complete
      onComplete();
    } else {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <div className="quiz">
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${((currentIndex + 1) / questions.length) * 100}%`,
          }}
        ></div>
      </div>

      <div className="quiz-content">
        <h2>
          Question {currentIndex + 1} of {questions.length}
        </h2>

        <div className="question-number">Q#{currentQuestion.id}</div>
        <h3 className="question-text">{currentQuestion.question}</h3>

        <div className="options">
          {currentQuestion.options.map((option, index) => (
            <label key={index} className="option">
              <input
                type="radio"
                name={`question-${currentQuestion.id}`}
                value={index}
                checked={answers[currentQuestion.id] === index}
                onChange={() => handleOptionSelect(index)}
              />
              <span className="option-letter">
                {String.fromCharCode(65 + index)})
              </span>
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="quiz-controls">
        <button
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          className="btn-secondary"
        >
          ← Previous
        </button>

        <button onClick={handleNext} className="btn-primary">
          {isLastQuestion ? 'Finish Quiz' : 'Next →'}
        </button>
      </div>
    </div>
  );
}

export default Quiz;
