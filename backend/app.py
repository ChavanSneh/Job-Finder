import os
import sys
import io
from typing import Optional

# Ensure the backend directory is in the path for reliable imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables explicitly
load_dotenv()

# Import project-specific service after setting sys.path
from backend.job_service import get_job_intelligence

app = FastAPI(
    title="AI Job Scout API 2026",
    description="Next-gen job intelligence with Gemini integration.",
    version="2.5.0"
)

@app.post("/search_jobs")
async def search_jobs(
    title: str = Form(..., description="Job title to search for"),
    location: str = Form("Pune", description="City or region"),
    exp: int = Form(2, description="Years of experience"),
    skills: str = Form(..., description="Comma separated skills"),
    resume: Optional[UploadFile] = File(None)
):
    """
    Job search endpoint with optional resume analysis.
    """
    try:
        resume_text = ""

        # Resume extraction
        if resume:
            if not resume.filename.lower().endswith(".pdf"):
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF resumes are supported"
                )

            pdf_content = await resume.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            
            pages_text = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
            resume_text = " ".join(pages_text)

        # Call orchestration layer
        result = get_job_intelligence(
            title=title,
            location=location,
            intel={"exp": exp, "skills": skills},
            resume_text=resume_text
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        # Added explicit logging for debugging
        print(f"DEBUG Error in search_jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal orchestration error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "Gemini-ready"}