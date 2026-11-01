from app.services.recommendation import generate_recommendations
from app.services.similarity import compute_skill_coverage, compute_weighted_skill_coverage
from app.services.skill_extractor import extract_skills
from app.services.skill_matcher import compare_skills


def test_skill_aliases_and_special_tokens() -> None:
    text = (
        "Experienced with Python3, ReactJS, Postgres, JS, sklearn, C++, C#, .NET, Node.js. "
        "Also used Java for Android, not only JavaScript."
    )
    names = {item["name"] for item in extract_skills(text)}
    assert "Python" in names
    assert "React" in names
    assert "PostgreSQL" in names
    assert "JavaScript" in names
    assert "Scikit-learn" in names
    assert "C++" in names
    assert "C#" in names
    assert ".NET" in names
    assert "Node.js" in names
    assert "Java" in names


def test_false_positives_avoided() -> None:
    names = {item["name"] for item in extract_skills("I will go to the store and write a report.")}
    assert "Go" not in names
    assert "R" not in names


def test_skill_matching_sets() -> None:
    resume = "Python, FastAPI, PostgreSQL, Docker, Git"
    job = "Required: Python, FastAPI, AWS. Preferred: Kubernetes."
    result = compare_skills(resume, job)
    matched = {item["name"] for item in result["matched_skills"]}
    missing = {item["name"] for item in result["missing_skills"]}
    additional = {item["name"] for item in result["additional_skills"]}
    assert "Python" in matched
    assert "FastAPI" in matched
    assert "AWS" in missing
    assert "Kubernetes" in missing
    assert "Docker" in additional


def test_score_calculation_and_empty_job_skills() -> None:
    coverage, note = compute_skill_coverage(2, 4)
    assert coverage == 50.0
    assert note is None
    empty_coverage, empty_note = compute_skill_coverage(0, 0)
    assert empty_coverage == 0.0
    assert empty_note is not None
    weighted, _ = compute_weighted_skill_coverage(
        [{"weight": 1.0}, {"weight": 0.5}],
        [{"weight": 1.0}],
    )
    assert weighted == 60.0


def test_recommendations_are_actionable() -> None:
    missing = [{"name": "AWS", "category": "Cloud Platforms", "priority": "mandatory"}]
    recs = generate_recommendations(missing, "Backend Engineer")
    assert recs[0]["skill"] == "AWS"
    assert "Do not list this skill" in recs[0]["next_steps"][-1]
