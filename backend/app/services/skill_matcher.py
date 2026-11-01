from app.services.skill_extractor import classify_skill_priority, extract_skills


def compare_skills(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    resume_names = {item["name"] for item in resume_skills}
    job_names = {item["name"] for item in job_skills}

    matched_names = resume_names & job_names
    missing_names = job_names - resume_names
    additional_names = resume_names - job_names

    resume_lookup = {item["name"]: item for item in resume_skills}
    job_lookup = {item["name"]: item for item in job_skills}

    matched = []
    for name in sorted(matched_names):
        priority, weight = classify_skill_priority(name, job_text)
        matched.append({**resume_lookup[name], "priority": priority, "weight": weight})

    missing = []
    for name in sorted(missing_names):
        priority, weight = classify_skill_priority(name, job_text)
        missing.append(
            {
                **job_lookup[name],
                "priority": priority,
                "weight": weight,
                "note": "Not detected in the uploaded resume. This does not prove the candidate lacks the skill.",
            }
        )

    additional = [resume_lookup[name] for name in sorted(additional_names)]

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_skills": additional,
    }


def category_breakdown(matched: list, missing: list, additional: list) -> dict[str, dict[str, int]]:
    breakdown: dict[str, dict[str, int]] = {}
    for label, items in (("matched", matched), ("missing", missing), ("additional", additional)):
        for item in items:
            category = item.get("category", "Other")
            breakdown.setdefault(category, {"matched": 0, "missing": 0, "additional": 0})
            breakdown[category][label] += 1
    return breakdown
