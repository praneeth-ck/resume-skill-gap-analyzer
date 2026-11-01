from __future__ import annotations

import re
from functools import lru_cache

from app.data.skill_dictionary import MANDATORY_HINTS, PREFERRED_HINTS, SKILL_DICTIONARY
from app.services.text_preprocessor import lowercase_for_matching

try:
    import spacy
    from spacy.matcher import PhraseMatcher
except ImportError:  # pragma: no cover
    spacy = None
    PhraseMatcher = None


_SPECIAL_PATTERN_CACHE: dict[str, re.Pattern] = {}


def _escape_alias(alias: str) -> str:
    return re.escape(alias).replace(r"\ ", r"[\s\-]+")


def _word_pattern(alias: str) -> re.Pattern:
    key = alias
    if key not in _SPECIAL_PATTERN_CACHE:
        escaped = _escape_alias(alias)
        if alias.startswith("."):
            pattern = rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z])"
        elif alias in {"c", "r", "go", "js", "ts", "ml", "cv", "tf"}:
            pattern = rf"(?<![A-Za-z0-9+#]){escaped}(?![A-Za-z0-9+#])"
        else:
            pattern = rf"(?<![A-Za-z0-9+#]){escaped}(?![A-Za-z0-9+#])"
        _SPECIAL_PATTERN_CACHE[key] = re.compile(pattern, re.IGNORECASE)
    return _SPECIAL_PATTERN_CACHE[key]


@lru_cache(maxsize=1)
def _load_nlp():
    from app.core.config import get_settings

    if spacy is None:
        return None
    settings = get_settings()
    try:
        nlp = spacy.load(settings.SPACY_MODEL, disable=["ner", "parser", "lemmatizer"])
    except OSError:
        nlp = spacy.blank("en")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for canonical, meta in SKILL_DICTIONARY.items():
        if meta.get("special"):
            continue
        phrases = [canonical, *meta.get("aliases", [])]
        patterns = [nlp.make_doc(phrase) for phrase in phrases if " " in phrase or len(phrase) > 2]
        if patterns:
            matcher.add(canonical, patterns)
    return nlp, matcher


def _java_false_positive(text: str, start: int, end: int) -> bool:
    window = text[max(0, start) : min(len(text), end + 6)].lower()
    return window.startswith("javascript")


def extract_skills(text: str) -> list[dict]:
    haystack = lowercase_for_matching(text)
    found: dict[str, dict] = {}

    nlp_bundle = _load_nlp()
    if nlp_bundle is not None:
        nlp, matcher = nlp_bundle
        doc = nlp(haystack)
        for match_id, start, end in matcher(doc):
            canonical = nlp.vocab.strings[match_id]
            span = doc[start:end]
            if canonical == "Java" and "javascript" in span.text.lower():
                continue
            found[canonical] = {
                "name": canonical,
                "category": SKILL_DICTIONARY[canonical]["category"],
                "aliases_matched": [span.text],
            }

    for canonical, meta in SKILL_DICTIONARY.items():
        aliases = [alias.lower() for alias in meta.get("aliases", [])]
        if not meta.get("special") or len(canonical) > 2 or any(char in canonical for char in "+#."):
            aliases = [canonical.lower(), *aliases]
        matched_aliases: list[str] = []
        for alias in aliases:
            pattern = _word_pattern(alias)
            match = pattern.search(haystack)
            if not match:
                continue
            if canonical == "Java" and _java_false_positive(haystack, match.start(), match.end()):
                continue
            matched_aliases.append(alias)
        if matched_aliases:
            existing = found.get(canonical)
            if existing:
                existing["aliases_matched"] = sorted(set(existing["aliases_matched"] + matched_aliases))
            else:
                found[canonical] = {
                    "name": canonical,
                    "category": meta["category"],
                    "aliases_matched": matched_aliases,
                }

    return sorted(found.values(), key=lambda item: (item["category"], item["name"]))


def classify_skill_priority(skill_name: str, job_text: str) -> tuple[str, float]:
    lowered = lowercase_for_matching(job_text)
    aliases = [skill_name.lower(), *[a.lower() for a in SKILL_DICTIONARY.get(skill_name, {}).get("aliases", [])]]
    windows: list[str] = []
    for alias in aliases:
        pattern = _word_pattern(alias)
        for match in pattern.finditer(lowered):
            start = max(0, match.start() - 180)
            end = min(len(lowered), match.end() + 80)
            windows.append(lowered[start:end])
    context = " ".join(windows) if windows else lowered
    if any(hint in context for hint in PREFERRED_HINTS):
        return "preferred", 0.55
    if any(hint in context for hint in MANDATORY_HINTS):
        return "mandatory", 1.0
    return "standard", 0.8
