from app.data.skill_dictionary import SKILL_DICTIONARY

CATEGORY_GUIDANCE: dict[str, dict[str, str]] = {
    "Programming Languages": {
        "why": "This language appears in the job description, so interviewers are likely to test fluency with it.",
        "learn": "Cover syntax, idioms, and a small production-style project using the language's standard tooling.",
        "project": "Rebuild a core feature from your current stack in this language and document trade-offs.",
    },
    "Frontend Frameworks": {
        "why": "The role expects UI implementation with this library or framework.",
        "learn": "Study component structure, state management, routing, and accessibility basics.",
        "project": "Build a responsive dashboard that consumes a public API and includes loading and empty states.",
    },
    "Backend Frameworks": {
        "why": "The job description points to server-side work with this framework.",
        "learn": "Practice routing, validation, authentication, and database access in the framework.",
        "project": "Create a small authenticated REST API with tests and a README that explains the design.",
    },
    "Databases": {
        "why": "Data modeling and querying with this store are likely part of day-to-day work.",
        "learn": "Learn schema design, indexing, transactions, and common query patterns.",
        "project": "Design a schema for a realistic domain and write queries that answer reporting questions.",
    },
    "Cloud Platforms": {
        "why": "The team likely deploys or operates services on this cloud.",
        "learn": "Complete a focused path covering IAM, compute, storage, and a managed database.",
        "project": "Deploy a simple API to the cloud with environment-based configuration and basic monitoring.",
    },
    "DevOps Tools": {
        "why": "Delivery speed and reliability on this team depend on these tools.",
        "learn": "Practice containerization, pipelines, and infrastructure as code at a beginner-to-intermediate level.",
        "project": "Containerize an app and add a CI pipeline that runs tests on every push.",
    },
    "Data Science": {
        "why": "The role involves analyzing or presenting data with this tool.",
        "learn": "Work through cleaning, exploration, visualization, and a short written insight.",
        "project": "Analyze a public dataset and publish a notebook with charts and conclusions.",
    },
    "Machine Learning": {
        "why": "The posting references ML methods or libraries that would come up in technical screens.",
        "learn": "Study the core workflow: data prep, baseline model, evaluation, and limitations.",
        "project": "Train a baseline model, compare it with a stronger approach, and write up evaluation metrics.",
    },
    "Development Tools": {
        "why": "Daily collaboration and quality checks on this team likely include this tool.",
        "learn": "Use the tool on a real repo rather than only reading documentation.",
        "project": "Add tests or API documentation to an existing personal project using this tool.",
    },
    "Professional Skills": {
        "why": "The posting calls out this working style or competency alongside technical skills.",
        "learn": "Practice the skill in a concrete setting such as a team project, case write-up, or design review.",
        "project": "Document a past project with problem, constraints, decisions, and outcome so you can discuss it clearly.",
    },
}


def generate_recommendations(missing_skills: list[dict], job_title: str) -> list[dict]:
    recommendations = []
    role = job_title or "the target role"
    for skill in missing_skills:
        name = skill["name"]
        category = skill.get("category") or SKILL_DICTIONARY.get(name, {}).get("category", "Professional Skills")
        priority = skill.get("priority") or "standard"
        guidance = CATEGORY_GUIDANCE.get(category, CATEGORY_GUIDANCE["Professional Skills"])
        recommendations.append(
            {
                "skill": name,
                "category": category,
                "priority": priority,
                "why_it_matters": f"{guidance['why']} For {role}, {name} was detected in the job description but not in the resume.",
                "what_to_learn": guidance["learn"],
                "suggested_project": guidance["project"],
                "next_steps": [
                    f"Study official {name} documentation and one reputable tutorial path.",
                    f"Complete a small project that uses {name} in a realistic workflow.",
                    "Add the project to your portfolio only after you can explain what you built.",
                    "Do not list this skill on your resume until you can demonstrate it.",
                ],
            }
        )
    priority_rank = {"mandatory": 0, "standard": 1, "preferred": 2}
    recommendations.sort(key=lambda item: (priority_rank.get(item["priority"], 9), item["skill"]))
    return recommendations
