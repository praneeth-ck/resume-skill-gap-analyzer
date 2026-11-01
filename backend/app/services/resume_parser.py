from io import BytesIO

import pymupdf as fitz
from docx import Document
from fastapi import HTTPException, status

from app.services.text_preprocessor import normalize_text


def extract_pdf_text(data: bytes) -> str:
    try:
        with fitz.open(stream=data, filetype="pdf") as document:
            if document.is_encrypted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Encrypted PDFs are not supported. Upload an unlocked resume.",
                )
            pages = []
            for page in document:
                pages.append(page.get_text("text"))
            text = "\n".join(pages)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read this PDF. The file may be corrupted.",
        )
    return _require_text(text)


def extract_docx_text(data: bytes) -> str:
    try:
        document = Document(BytesIO(data))
        chunks: list[str] = []
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                chunks.append(paragraph.text)
        for table in document.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    chunks.append(" | ".join(cells))
        text = "\n".join(chunks)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read this DOCX file. The file may be corrupted.",
        )
    return _require_text(text)


def extract_resume_text(data: bytes, file_type: str) -> str:
    if file_type == "pdf":
        return extract_pdf_text(data)
    if file_type == "docx":
        return extract_docx_text(data)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type.")


def _require_text(text: str) -> str:
    cleaned = normalize_text(text)
    if len(cleaned) < 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No readable text was found in this file. Try a text-based PDF or DOCX.",
        )
    return cleaned
