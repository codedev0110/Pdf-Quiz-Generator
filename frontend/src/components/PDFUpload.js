import React, { useState } from 'react';
import axios from 'axios';

function PDFUpload({ onPdfUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Please select a valid PDF file');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/upload-pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onPdfUploaded(response.data.pdf_id, response.data.total_questions);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to upload PDF. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <div className="form-group">
        <label htmlFor="pdf-input">📄 Upload PDF</label>
        <input
          id="pdf-input"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          disabled={loading}
        />
      </div>

      {file && <p className="success">✓ {file.name} selected</p>}
      {error && <p className="error">✗ {error}</p>}

      <button type="submit" disabled={!file || loading}>
        {loading ? <div className="spinner"></div> : 'Upload & Parse PDF'}
      </button>
    </form>
  );
}

export default PDFUpload;
