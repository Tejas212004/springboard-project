import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    print(f"⚠️ Page {page_num + 1} has no extractable text.")
        print("✅ PDF text extraction complete.")
        return text.strip()
    except Exception as e:
        print("❌ Failed to extract text from PDF:", str(e))
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        print(f"✅ DOCX text extraction complete. {len(paragraphs)} paragraphs found.")
        return "\n".join(paragraphs).strip()
    except Exception as e:
        print("❌ Failed to extract text from DOCX:", str(e))
        return ""

def parse_resume(file_path: str) -> str:
    """Parse resume file and extract text based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    print(f"📄 Parsing resume: {file_path} (Extension: {ext})")

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print("❌ Unsupported file format:", ext)
        return ""