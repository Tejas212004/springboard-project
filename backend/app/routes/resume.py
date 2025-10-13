import os
from fastapi import APIRouter, UploadFile, File
from app.resume_parser.parser import parse_resume
from app.matcher.semantic_matcher import match_skills

router = APIRouter()

# ✅ Define a reusable skill list
SKILL_LIST = [
    "Python", "FastAPI", "React", "Docker", "Machine Learning",
    "Natural Language Processing", "Git", "SQL", "Flask", "TensorFlow"
]

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        # ✅ Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # ✅ Parse resume content
        content = parse_resume(temp_path)
        print("✅ Resume parsed successfully.")
        print("🔍 Resume Preview:", content[:500])

        # ✅ Match skills
        skills = match_skills(content, SKILL_LIST)
        print("📌 Matched Skills:", skills)

        return {
            "filename": file.filename,
            "skills": skills,
            "preview": content[:500]
        }

    except Exception as e:
        print("❌ Resume upload failed:", str(e))
        return {
            "error": f"Failed to process resume: {str(e)}",
            "filename": file.filename,
            "skills": [],
            "preview": ""
        }

    finally:
        # ✅ Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)