from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.text_preprocessor import normalize_text


def compute_text_similarity(resume_text: str, job_text: str) -> tuple[float, str | None]:
    resume = normalize_text(resume_text)
    job = normalize_text(job_text)
    if not resume or not job:
        return 0.0, "Text similarity was skipped because one of the documents was empty."
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        matrix = vectorizer.fit_transform([resume, job])
        if matrix.shape[1] == 0:
            return 0.0, "Text similarity was skipped because no comparable terms were found."
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
        return round(max(0.0, min(score, 100.0)), 2), None
    except ValueError:
        return 0.0, "Text similarity could not be computed for these documents."


def compute_skill_coverage(matched_count: int, required_count: int) -> tuple[float, str | None]:
    if required_count == 0:
        return 0.0, "Skill coverage is unavailable because no required skills were detected in the job description."
    return round((matched_count / required_count) * 100, 2), None


def compute_weighted_skill_coverage(matched: list, missing: list) -> tuple[float, str | None]:
    required = matched + missing
    if not required:
        return 0.0, "Weighted skill coverage is unavailable because no job skills were detected."
    total_weight = sum(float(item.get("weight") or 0.8) for item in required)
    if total_weight <= 0:
        return 0.0, "Weighted skill coverage is unavailable due to missing skill weights."
    earned = sum(float(item.get("weight") or 0.8) for item in matched)
    return round((earned / total_weight) * 100, 2), None


def compute_overall_score(weighted_coverage: float, text_similarity: float, notes: list[str]) -> float:
    if any("unavailable" in note.lower() or "skipped" in note.lower() for note in notes):
        if "no required skills" in " ".join(notes).lower() and "no job skills" in " ".join(notes).lower():
            return 0.0
    return round((0.7 * weighted_coverage) + (0.3 * text_similarity), 2)
