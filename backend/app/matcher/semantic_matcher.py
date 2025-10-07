from sentence_transformers import SentenceTransformer, util
import re

# ✅ Load the semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_skills(resume_text: str, skill_list: list, threshold: float = 0.5) -> list:
    """
    Matches skills from a predefined list against resume text using semantic similarity.
    """
    if not resume_text or not skill_list:
        return []

    # ✅ Normalize and filter resume sentences
    resume_sentences = [line.strip().lower() for line in resume_text.split("\n") if len(line.strip()) > 3]

    matched_skills = set()

    for skill in skill_list:
        skill_embedding = model.encode(skill.lower(), convert_to_tensor=True)
        for sentence in resume_sentences:
            sentence_embedding = model.encode(sentence, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(skill_embedding, sentence_embedding).item()

            # 🔍 Debug: print similarity scores
            print(f"Skill: {skill}, Sentence: {sentence}, Similarity: {similarity:.2f}")

            if similarity >= threshold:
                matched_skills.add(skill)
                break

    return list(matched_skills)

def compute_similarity(text1: str, text2: str) -> float:
    """
    Computes semantic similarity between resume and job description.
    """
    if not text1 or not text2:
        return 0.0

    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()

def extract_skills(text: str) -> list:
    """
    Extracts known skills from raw text using keyword matching.
    """
    if not text:
        return []

    text = text.lower()
    keywords = re.findall(r'\b[a-z][a-z\+\#\.\-]{1,}\b', text)

    # ✅ Expanded known skills with synonyms
    known_skills = {
        "python", "java", "c++", "c#", "javascript", "react", "react.js", "node.js", "nodejs",
        "sql", "docker", "kubernetes", "aws", "azure", "tensorflow", "flask",
        "fastapi", "git", "power bi", "tableau", "excel", "nlp", "pandas", "numpy", "mongodb", "html", "css"
    }

    return list(set(keywords) & known_skills)