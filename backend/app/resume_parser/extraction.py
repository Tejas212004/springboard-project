import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = {
    "Python", "Java", "C++", "SQL", "FastAPI", "Flask", "React",
    "Machine Learning", "NLP", "Git", "Docker", "REST", "TensorFlow"
}

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.add(skill)

    return list(found_skills)