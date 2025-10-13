import spacy

# ✅ Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ✅ Define skill keywords (can be expanded or loaded from external source)
SKILL_KEYWORDS = {
    "Python", "Java", "C++", "SQL", "FastAPI", "Flask", "React",
    "Machine Learning", "NLP", "Git", "Docker", "REST", "TensorFlow",
    "Node.js", "HTML", "CSS", "MongoDB", "Pandas", "NumPy", "Excel",
    "Power BI", "Tableau", "Jupyter", "Scikit-learn", "Matplotlib", "Postman", "GraphQL"
}

def extract_skills(text: str) -> list:
    """Extract skills from text using keyword matching and basic NLP."""
    if not text or len(text.strip()) < 10:
        print("⚠️ Input text too short or empty.")
        return []

    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.add(skill)

    print(f"✅ Skills extracted: {sorted(found_skills)}")
    return sorted(found_skills)