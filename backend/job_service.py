import os
import json
import logging
from backend.sources.jsearch import JSearchProvider
from backend.ai_analyst import analyze_jobs  # Assuming this is the correct import

# Setup logging
logger = logging.getLogger(__name__)

PROFILE_PATH = "backend/user_profile.json"

def get_persistent_profile():
    """Reads stored skills from the JSON vault with robust error handling."""
    if not os.path.exists(PROFILE_PATH):
        logger.warning(f"Profile file not found at {PROFILE_PATH}. Using defaults.")
        return {
            "name": "User",
            "skills_string": "Python, FastAPI, Docker, AI, RAG",
            "experience": 2
        }
        
    try:
        with open(PROFILE_PATH, "r") as f:
            data = json.load(f)
            
            # Normalize skills to a string for search query building
            skills_val = data.get("skills", "")
            if isinstance(skills_val, list):
                data["skills_string"] = ", ".join(skills_val)
            else:
                data["skills_string"] = str(skills_val)
                
            return data
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to read/parse user_profile.json: {e}")
        return {"skills_string": "Python, FastAPI", "experience": 2}

def get_job_intelligence(title, location, intel, resume_text=None):
    """
    Coordinates search with fallback to persistent profile.
    """
    provider = JSearchProvider()
    stored_data = get_persistent_profile()
    
    # 1. Logic: UI Input > Stored Profile > Fallback
    ui_skills = intel.get('skills', '').strip()
    if not ui_skills or ui_skills.lower() in ["python, sql", "leave blank..."]:
        final_skills = stored_data.get("skills_string", "Python, FastAPI")
    else:
        final_skills = ui_skills
        
    # Log the search attempt so you can see exactly what is being queried
    search_query = f"{title} {final_skills}"
    logger.info(f"DEBUG: Executing JSearch query: '{search_query}' in '{location}'")
    
    try:
        # 2. Search
        raw_jobs = provider.search_jobs(query=search_query, location=location)
        
        if not isinstance(raw_jobs, list):
            logger.error(f"Provider returned invalid type: {type(raw_jobs)}")
            raw_jobs = []

        # 3. Analyze
        if raw_jobs:
            ai_insight = analyze_jobs(
                job_title=title, 
                findings=raw_jobs, 
                intel={"exp": intel.get('exp', 2), "skills": final_skills},
                resume_text=resume_text
            )
        else:
            ai_insight = (f"No roles found for '{title}' in '{location}' "
                          f"with skill vector: {final_skills}. Try broadening your search.")

        return {
            "jobs": raw_jobs,
            "ai_insight": ai_insight
        }

    except Exception as e:
        logger.error(f"Error in job_intelligence: {str(e)}", exc_info=True)
        return {
            "jobs": [],
            "ai_insight": "Intelligence module encountered an error. Check logs."
        }