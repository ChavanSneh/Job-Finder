import os
from google import genai
from google.genai import types
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
# Note: You may need to catch specific exceptions from the Google Gen AI SDK
# If the SDK raises a generic Exception for rate limits, adjust accordingly.
from google.genai.errors import APIError 

@retry(
    # Stop after 5 failed attempts
    stop=stop_after_attempt(5),
    # Wait 2^x * 1 second between retries, starting at 2s, maxing at 60s
    wait=wait_exponential(multiplier=1, min=2, max=60),
    # Only retry if it's a transient API error (like rate limiting)
    retry=retry_if_exception_type(APIError),
    reraise=True
)
def analyze_jobs(job_title, findings, intel, resume_text=None):
    """
    Uses the modern Google Gen AI SDK to analyze jobs with built-in retry logic.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
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
    
    # The @retry decorator handles the execution flow here.
    # If APIError is raised, tenacity will pause and retry automatically.
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