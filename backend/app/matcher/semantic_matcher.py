import re
from sentence_transformers import SentenceTransformer, util

# ✅ Load the semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Known skills and aliases
known_skills = {
    "python", "java", "c++", "c#", "javascript", "react", "react.js", "node.js", "nodejs",
    "sql", "docker", "kubernetes", "aws", "azure", "tensorflow", "flask",
    "fastapi", "git", "power bi", "tableau", "excel", "nlp", "pandas", "numpy",
    "mongodb", "html", "css", "jupyter", "scikit-learn", "matplotlib", "postman", "graphql"
}

# ✅ Optional aliases for normalization
skill_aliases = {
    "react.js": "react",
    "nodejs": "node.js",
    "html5": "html",
    "css3": "css",
    "ml": "machine learning",
    "scikit": "scikit-learn"
}

def normalize_skill(skill: str) -> str:
    """Normalize skill using aliases."""
    return skill_aliases.get(skill.lower(), skill.lower())

def extract_skills(text: str) -> list:
    """Extract known skills from raw text using keyword matching."""
    if not text or len(text.strip()) < 10:
        print("⚠️ Text too short or empty for skill extraction.")
        return []

    text = text.lower()
    keywords = re.findall(r'\b[a-z][a-z\+\#\.\-]{1,}\b', text)
    normalized = [normalize_skill(k) for k in keywords]
    found = list(set(normalized) & known_skills)

    print(f"✅ Extracted Skills: {sorted(found)}")
    return sorted(found)

def match_skills(resume_text: str, skill_list: list, threshold: float = 0.65) -> list:
    """Match skills from a predefined list against resume text using semantic similarity."""
    if not resume_text or not skill_list:
        print("⚠️ Missing resume text or skill list.")
        return []

    resume_sentences = re.split(r'[.\n]', resume_text.lower())
    resume_sentences = [s.strip() for s in resume_sentences if len(s.strip()) > 3]
    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)

    matched_skills = set()

    for skill in skill_list:
        skill_norm = normalize_skill(skill)
        skill_embedding = model.encode(skill_norm, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(skill_embedding, resume_embeddings)[0]
        max_sim = float(similarities.max())

        print(f"🔍 Skill: {skill_norm}, Similarity: {max_sim:.2f}")
        if max_sim >= threshold:
            matched_skills.add(skill_norm)

    print(f"✅ Matched Skills: {sorted(matched_skills)}")
    return sorted(matched_skills)

def match_skills_with_breakdown(resume_text: str, skill_list: list, threshold: float = 0.2) -> dict:
    """Return breakdown of each skill with match status and similarity score."""
    if not resume_text or not skill_list:
        print("⚠️ Missing resume text or skill list for breakdown.")
        return {}

    resume_sentences = re.split(r'[.\n]', resume_text.lower())
    resume_sentences = [s.strip() for s in resume_sentences if len(s.strip()) > 3]
    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)

    breakdown = {}

    for skill in skill_list:
        skill_norm = normalize_skill(skill)
        skill_embedding = model.encode(skill_norm, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(skill_embedding, resume_embeddings)[0]
        max_score = float(similarities.max())
        matched = max_score >= threshold

        breakdown[skill_norm] = {
            "matched": matched,
            "similarity": round(max_score, 2)
        }

        print(f"📊 {skill_norm}: {'✅' if matched else '❌'} ({max_score:.2f})")

    return breakdown

def compute_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity between resume and job description."""
    if not text1 or not text2:
        print("⚠️ One or both texts are empty.")
        return 0.0

    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()

    print(f"🧠 Resume vs Job Similarity: {score:.2f}")
    return score