import React, { useState } from 'react';

function QuizConfig({ totalQuestions, onConfigure, loading }) {
  const [start, setStart] = useState(1);
  const [end, setEnd] = useState(Math.min(100, totalQuestions));
  const [count, setCount] = useState(10);
  const [error, setError] = useState('');

  const handleConfigure = (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (start < 1) {
      setError('Start number must be at least 1');
      return;
    }
    if (end > totalQuestions) {
      setError(`End number cannot exceed total questions (${totalQuestions})`);
      return;
    }
    if (start > end) {
      setError('Start number must be less than or equal to end number');
      return;
    }
    const available = end - start + 1;
    if (count > available) {
      setError(
        `Not enough questions in range. Available: ${available}, Requested: ${count}`
      );
      return;
    }

    onConfigure({ start, end, count });
  };

  return (
    <form onSubmit={handleConfigure}>
      <p style={{ marginBottom: '25px', color: '#666' }}>
        Total questions in PDF: <strong>{totalQuestions}</strong>
      </p>

      <div className="form-group">
        <label htmlFor="start">Start Question #</label>
        <input
          id="start"
          type="number"
          value={start}
          onChange={(e) => setStart(Number(e.target.value))}
          min="1"
          max={totalQuestions}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="end">End Question #</label>
        <input
          id="end"
          type="number"
          value={end}
          onChange={(e) => setEnd(Number(e.target.value))}
          min="1"
          max={totalQuestions}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="count">Number of Questions</label>
        <input
          id="count"
          type="number"
          value={count}
          onChange={(e) => setCount(Number(e.target.value))}
          min="1"
          max={end - start + 1}
          disabled={loading}
        />
      </div>

      {error && <p className="error">✗ {error}</p>}

      <button type="submit" disabled={loading}>
        {loading ? <div className="spinner"></div> : 'Generate Quiz'}
      </button>
    </form>
  );
}

export default QuizConfig;
