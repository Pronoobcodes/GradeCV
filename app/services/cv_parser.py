import os
import fitz  # PyMuPDF
from docx import Document
import re
from fastapi import HTTPException, status

class CVParserService:
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found on server"
            )
            
        if file_type.lower() == 'pdf':
            return CVParserService._extract_from_pdf(file_path)
        elif file_type.lower() in ['docx', 'doc']:
            return CVParserService._extract_from_docx(file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type for parsing"
            )
            
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return CVParserService._clean_text(text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse PDF: {str(e)}"
            )

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return CVParserService._clean_text(text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse DOCX: {str(e)}"
            )

    @staticmethod
    def _clean_text(text: str) -> str:
        # Normalize whitespace (replace multiple spaces with one)
        text = re.sub(r'[ \t]+', ' ', text)
        # Remove duplicate blank lines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
