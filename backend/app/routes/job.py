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
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        content = parse_resume(temp_path)
        return {
            "filename": file.filename,
            "preview": content[:500]
        }
    finally:
        os.remove(temp_path)

@router.post("/upload-job-text")
async def upload_job_text(payload: JobText):
    return {
        "filename": "raw_text",
        "preview": payload.text[:500]
    }