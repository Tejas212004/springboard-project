from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.resume_parser.parser import parse_resume
from app.matcher.semantic_matcher import match_skills as semantic_match
from app.resume_parser.extraction import extract_skills as keyword_match
from app.routes.resume import router as resume_router
from app.routes.job import router as job_router
from app.routes.matcher import router as matcher_router
import tempfile
import shutil
import os

app = FastAPI()

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

    # ✅ Combine resume lines into richer semantic context
    resume_text = " ".join([line.strip() for line in raw_resume_text.split("\n") if len(line.strip()) > 3])

    # ✅ Extract skills from job description
    job_skills = keyword_match(job_text)
    if not job_skills:
        job_skills = []

    # ✅ Semantic skill matching
    matched_skills = semantic_match(resume_text, job_skills)
    if not matched_skills:
        matched_skills = []

    # ✅ Keyword-based skill extraction from resume
    keyword_skills = keyword_match(resume_text)
    if not keyword_skills:
        keyword_skills = []

    # ✅ Combine both match sets
    combined_skills = set(matched_skills + keyword_skills)
    missing_skills = [skill for skill in job_skills if skill not in combined_skills]
    match_score = round((len(combined_skills & set(job_skills)) / len(job_skills)) * 100, 2)

    # ✅ Return structured response
    return {
        "match_score": match_score,
        "matched_skills": list(combined_skills & set(job_skills)),
        "missing_skills": missing_skills,
        "keyword_skills": keyword_skills
    }