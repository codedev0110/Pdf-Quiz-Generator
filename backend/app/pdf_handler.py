import os
import uuid
import pdfplumber
from pathlib import Path
from typing import Dict, Optional


class PDFHandler:
    """Handles PDF storage and text extraction"""
    
    def __init__(self, storage_dir: str = "pdfs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.metadata: Dict[str, Dict] = {}
    
    def save_pdf(self, file_path: str, file_content: bytes) -> str:
        """
        Save PDF file and return unique PDF ID
        
        Args:
            file_path: Original file path/name
            file_content: Binary content of PDF file
            
        Returns:
            pdf_id: Unique identifier for the PDF
        """
        pdf_id = str(uuid.uuid4())
        saved_path = self.storage_dir / f"{pdf_id}.pdf"
        
        with open(saved_path, 'wb') as f:
            f.write(file_content)
        
        # Store metadata
        self.metadata[pdf_id] = {
            'original_name': file_path,
            'file_path': str(saved_path)
        }
        
        return pdf_id
    
    def extract_text(self, pdf_id: str) -> str:
        """
        Extract text from PDF using pdfplumber
        
        Args:
            pdf_id: Unique PDF identifier
            
        Returns:
            Extracted text from PDF
        """
        if pdf_id not in self.metadata:
            raise ValueError(f"PDF with id {pdf_id} not found")
        
        pdf_path = self.metadata[pdf_id]['file_path']
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n"
        
        return text
    
    def get_pdf_path(self, pdf_id: str) -> Optional[str]:
        """Get file path for a PDF ID"""
        if pdf_id in self.metadata:
            return self.metadata[pdf_id]['file_path']
        return None
    
    def cleanup_pdf(self, pdf_id: str) -> bool:
        """Delete a stored PDF"""
        if pdf_id not in self.metadata:
            return False
        
        pdf_path = self.metadata[pdf_id]['file_path']
        try:
            os.remove(pdf_path)
            del self.metadata[pdf_id]
            return True
        except Exception:
            return False
