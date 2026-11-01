from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

PDF_MAGIC = b"%PDF"
DOCX_MAGIC = b"PK"
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream",
}


async def validate_and_read_upload(file: UploadFile) -> tuple[bytes, str, str]:
    settings = get_settings()
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A filename is required.")

    original_name = Path(file.filename).name
    suffix = Path(original_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Upload a PDF or DOCX resume.",
        )

    content_type = (file.content_type or "").lower()
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported content type. Upload a PDF or DOCX resume.",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The uploaded file is empty.")
    if len(data) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the 5 MB upload limit.",
        )

    if suffix == ".pdf":
        if not data.startswith(PDF_MAGIC):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a valid PDF.")
        file_type = "pdf"
    else:
        if not data.startswith(DOCX_MAGIC):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a valid DOCX.")
        file_type = "docx"

    return data, original_name, file_type
