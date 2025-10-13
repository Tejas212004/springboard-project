import os
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.resume_parser.parser import parse_resume

router = APIRouter()

class JobText(BaseModel):
    text: str

@router.post("/upload-job")
async def upload_job(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        # ✅ Save uploaded job file temporarily
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # ✅ Parse job description content
        content = parse_resume(temp_path)
        print("✅ Job file parsed successfully.")
        print("🔍 Job Preview:", content[:500])

        return {
            "filename": file.filename,
            "preview": content[:500]
        }

    except Exception as e:
        print("❌ Job file parsing failed:", str(e))
        return {
            "error": f"Failed to process job file: {str(e)}",
            "filename": file.filename,
            "preview": ""
        }

    finally:
        # ✅ Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/upload-job-text")
async def upload_job_text(payload: JobText):
    print("✅ Raw job text received.")
    print("🔍 Job Text Preview:", payload.text[:500])

    return {
        "filename": "raw_text",
        "preview": payload.text[:500]
    }