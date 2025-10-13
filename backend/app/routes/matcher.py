from fastapi import APIRouter
from pydantic import BaseModel
from app.matcher.semantic_matcher import match_skills, match_skills_with_breakdown, compute_similarity
from app.resume_parser.extraction import extract_skills  # ✅ Corrected import

router = APIRouter()

class MatchPayload(BaseModel):
    resume_text: str
    job_text: str

@router.post("/match-resume-job")
def match_resume_job(payload: MatchPayload):
    try:
        # ✅ Extract skills from job description
        job_skills = extract_skills(payload.job_text)
        print("📌 Extracted Job Skills:", job_skills)

        # ✅ Match resume against job skills
        resume_skills = match_skills(payload.resume_text, job_skills)
        print("📌 Matched Resume Skills:", resume_skills)

        # ✅ Compute matched and missing skills
        matched = list(set(resume_skills) & set(job_skills))
        missing = list(set(job_skills) - set(resume_skills))

        # ✅ Compute semantic similarity score
        score = compute_similarity(payload.resume_text, payload.job_text)
        print(f"✅ Match Score: {round(score * 100, 2)}%")

        # ✅ Skill similarity breakdown
        breakdown = match_skills_with_breakdown(payload.resume_text, job_skills)

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_score": round(score * 100, 2),
            "job_skills": job_skills,
            "breakdown": breakdown
        }

    except Exception as e:
        print("❌ Matching failed:", str(e))
        return {
            "error": f"Failed to match resume and job description: {str(e)}",
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0.0,
            "job_skills": [],
            "breakdown": {}
        }