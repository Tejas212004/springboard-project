import os
from fastapi import APIRouter, UploadFile, File
from app.resume_parser.parser import parse_resume
from app.matcher.semantic_matcher import match_skills

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        content = parse_resume(temp_path)
        SKILL_LIST = [
            "Python", "FastAPI", "React", "Docker", "Machine Learning",
            "Natural Language Processing", "Git", "SQL", "Flask", "TensorFlow"
        ]
        skills = match_skills(content, SKILL_LIST)

        return {
            "filename": file.filename,
            "skills": skills,
            "preview": content[:500]
        }
    finally:
        os.remove(temp_path)