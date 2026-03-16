from google import genai
from google.genai import types
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from google.genai.errors import APIError 

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type(APIError),
    reraise=True
)
def analyze_jobs(api_key, job_title, findings, intel, resume_text=None):
    """
    Uses the modern Google Gen AI SDK to analyze jobs.
    api_key is now passed explicitly to avoid environment variable issues.
    """
    # Initialize client with the passed key
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a career consultant assisting Sneh Chavan. Sneh is a software engineer. 
    Analyze the following job listings for the role: {job_title}.
    
    User Profile:
    - Experience: {intel.get('exp')} years.
    - Skills: {intel.get('skills')}
    - Resume Content: {resume_text if resume_text else 'No resume provided.'}
    
    Job Listings:
    {str(findings)}
    
    Provide a concise, strategic summary for each listing.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            system_instruction="You are a career consultant assisting Sneh Chavan. "
                               "Sneh is a software engineer. Always use gender-neutral "
                               "language and refer to the user by name: Sneh."
        )
    )
    return response.text