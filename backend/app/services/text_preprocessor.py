import re
import unicodedata


def normalize_text(text: str) -> str:
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\x00", " ")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\r\n?", "\n", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def lowercase_for_matching(text: str) -> str:
    return normalize_text(text).lower()


def split_sections(text: str) -> dict[str, str]:
    """Split a job description into loosely labeled sections for weighting."""
    lowered = lowercase_for_matching(text)
    parts = re.split(r"\n(?=[A-Z][A-Za-z /&-]{2,40}:)", text)
    sections: dict[str, str] = {"full": lowered}
    for part in parts:
        header_match = re.match(r"^([A-Za-z /&-]{2,40}):", part.strip())
        if header_match:
            key = header_match.group(1).strip().lower()
            sections[key] = lowercase_for_matching(part)
    return sections
