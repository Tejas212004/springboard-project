from fastapi import APIRouter
from pydantic import BaseModel
from app.matcher.semantic_matcher import match_skills, compute_similarity
from app.resume_parser.extraction import extract_skills  # ✅ Corrected import

router = APIRouter()

class MatchPayload(BaseModel):
    resume_text: str
    job_text: str

@router.post("/match-resume-job")
def match_resume_job(payload: MatchPayload):
    job_skills = extract_skills(payload.job_text)
    resume_skills = match_skills(payload.resume_text, job_skills)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))
    score = compute_similarity(payload.resume_text, payload.job_text)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": round(score * 100, 2),
        "job_skills": job_skills
    }