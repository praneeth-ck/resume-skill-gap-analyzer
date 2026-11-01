from io import BytesIO

import pymupdf as fitz
from docx import Document
from fastapi.testclient import TestClient

from app.services.resume_parser import extract_docx_text, extract_pdf_text


RESUME_BODY = (
    "Jane Doe\nSoftware Engineer\nSkills: Python, FastAPI, React, PostgreSQL, Docker, Git, "
    "machine learning with scikit-learn and pandas. Built REST APIs and CI/CD pipelines."
)


def _pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    data = document.tobytes()
    document.close()
    return data


def _docx_bytes(text: str) -> bytes:
    document = Document()
    document.add_paragraph(text)
    table = document.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Skills"
    table.rows[0].cells[1].text = "Python | FastAPI"
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_pdf_and_docx_extraction() -> None:
    pdf_text = extract_pdf_text(_pdf_bytes(RESUME_BODY))
    assert "Python" in pdf_text
    docx_text = extract_docx_text(_docx_bytes(RESUME_BODY))
    assert "Python" in docx_text
    assert "FastAPI" in docx_text


def test_upload_and_analysis_flow(client: TestClient, auth_headers: dict[str, str]) -> None:
    upload = client.post(
        "/api/resumes/upload",
        headers=auth_headers,
        files={"file": ("resume.pdf", _pdf_bytes(RESUME_BODY), "application/pdf")},
    )
    assert upload.status_code == 201
    resume_id = upload.json()["id"]
    assert "Python" in upload.json()["extracted_text"]

    job = client.post(
        "/api/jobs",
        headers=auth_headers,
        json={
            "title": "Backend Engineer",
            "company": "Acme",
            "description": (
                "We need a backend engineer. Required: Python, FastAPI, PostgreSQL, AWS. "
                "Preferred: Kubernetes. Experience with REST APIs is expected."
            ),
        },
    )
    assert job.status_code == 201
    job_id = job.json()["id"]
    assert job.json()["required_skills"]

    analysis = client.post(
        "/api/analyses",
        headers=auth_headers,
        json={"resume_id": resume_id, "job_id": job_id},
    )
    assert analysis.status_code == 201
    body = analysis.json()
    matched_names = {item["name"] for item in body["matched_skills"]}
    missing_names = {item["name"] for item in body["missing_skills"]}
    assert "Python" in matched_names
    assert "AWS" in missing_names
    assert isinstance(body["match_score"], float)
    assert body["recommendations"]

    listed = client.get("/api/analyses", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.json()["total"] >= 1


def test_authorization_isolation(client: TestClient, auth_headers: dict[str, str]) -> None:
    upload = client.post(
        "/api/resumes/upload",
        headers=auth_headers,
        files={"file": ("resume.pdf", _pdf_bytes(RESUME_BODY), "application/pdf")},
    )
    resume_id = upload.json()["id"]
    other = client.post(
        "/api/auth/register",
        json={"name": "Other User", "email": "other@example.com", "password": "password123"},
    )
    other_headers = {"Authorization": f"Bearer {other.json()['access_token']}"}
    forbidden = client.get(f"/api/resumes/{resume_id}", headers=other_headers)
    assert forbidden.status_code == 404


def test_reject_bad_files(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/resumes/upload",
        headers=auth_headers,
        files={"file": ("notes.txt", b"not a resume", "text/plain")},
    )
    assert response.status_code == 400
