from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.resume_parser.parser import parse_resume
from app.matcher.semantic_matcher import extract_skills as keyword_match
from sentence_transformers import SentenceTransformer, util
from app.routes.resume import router as resume_router
from app.routes.job import router as job_router
from app.routes.matcher import router as matcher_router
import tempfile
import shutil
import os

app = FastAPI(title="AI Resume Matcher", description="Semantic skill matching for resumes and job descriptions")

# ✅ Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register modular routers
app.include_router(resume_router, prefix="/api")
app.include_router(job_router, prefix="/api")
app.include_router(matcher_router, prefix="/api")

# ✅ Load sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# ✅ Resume matcher endpoint
@app.post("/match-resume-job")
async def match_resume_job(resume: UploadFile, job_text: str = Form(...)):
    suffix = os.path.splitext(resume.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name

    try:
        raw_resume_text = parse_resume(tmp_path)
        print("✅ Resume parsed successfully.")
        print("🔍 Raw Resume Text Preview:", raw_resume_text[:500])
    except Exception as e:
        os.remove(tmp_path)
        print("❌ Resume parsing failed:", str(e))
        return {"error": f"Failed to parse resume: {str(e)}"}

    os.remove(tmp_path)

    # ✅ Clean and lowercase resume text
    resume_text = " ".join([
        line.strip().lower()
        for line in raw_resume_text.split("\n")
        if len(line.strip()) > 3
    ])
    print("🧠 Cleaned Resume Text:", resume_text[:500])

    # ✅ Extract and lowercase skills from both sources
    resume_skills = [skill.lower() for skill in keyword_match(resume_text)]
    job_skills = [skill.lower() for skill in keyword_match(job_text)]

    print("📌 Extracted Resume Skills:", resume_skills)
    print("📌 Extracted Job Skills:", job_skills)

    if not job_skills:
        return {
            "match_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": resume_skills,
            "job_skills": [],
            "breakdown": {},
            "error": "No skills extracted from job description."
        }

    # ✅ Semantic matching: compare each job skill to resume sentences
    resume_sentences = [s.strip().lower() for s in resume_text.split('.') if len(s.strip()) > 3]
    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)

    breakdown = {}
    threshold = 0.2  # You can tune this

    for skill in job_skills:
        skill_embedding = model.encode(skill, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(skill_embedding, resume_embeddings)[0]
        max_sim = float(similarities.max())
        breakdown[skill] = {
            "matched": max_sim >= threshold,
            "similarity": round(max_sim, 3)
        }

    matched_skills = [skill for skill, info in breakdown.items() if info["matched"]]
    missing_skills = [skill for skill in job_skills if skill not in matched_skills]
    match_score = round((len(matched_skills) / len(job_skills)) * 100, 2)

    print(f"✅ Match Score: {match_score}%")
    print("✅ Matched Skills:", matched_skills)
    print("❌ Missing Skills:", missing_skills)

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "breakdown": breakdown
    }