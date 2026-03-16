import os
import io
import logging
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pypdf import PdfReader
from dotenv import load_dotenv

# --- config ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

logger = logging.getLogger("job_scout")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing—set it in.env")

from backend.job_service import get_job_intelligence # expects api_key arg

app = FastAPI(
    title="AI Job Scout API 2026",
    description="Next-gen job intelligence with Gemini integration.",
    version="2.5.0"
)

@app.post("/search_jobs")
async def search_jobs(
    title: str = Form(...),
    location: str = Form("Pune"),
    exp: int = Form(2),
    skills: str = Form(...),
    resume: Optional[UploadFile] = File(None)
):
    resume_text = ""
    if resume:
        if not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF resumes are supported")
        try:
            pdf_bytes = await resume.read()
            reader = PdfReader(io.BytesIO(pdf_bytes))
            resume_text = " ".join(
                p.extract_text() or "" for p in reader.pages
            ).strip()
            if not resume_text:
                raise HTTPException(status_code=400, detail="PDF contains no extractable text")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"PDF read error: {e}")
            raise HTTPException(status_code=400, detail="Failed to read PDF")

    result = get_job_intelligence(
        api_key=GEMINI_API_KEY,
        title=title,
        location=location,
        intel={"exp": exp, "skills": skills},
        resume_text=resume_text,
    )
    return result

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "Gemini-ready"}