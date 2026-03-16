
import requests
from dotenv import load_dotenv
from backend.sources.base_source import BaseSource

load_dotenv()


class JSearchProvider(BaseSource):

    def __init__(self):
        import os
        self.api_key = os.getenv("RAPIDAPI_KEY")

        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")

        self.url = "https://jsearch.p.rapidapi.com/search"


    def search_jobs(self, query: str, location: str) -> list:

        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        params = {
            "query": f"{query} in {location}",
            "num_pages": "1"
        }

        try:
            response = requests.get(
                self.url,
                headers=headers,
                params=params,
                timeout=15
            )

            print(f"DEBUG Status Code: {response.status_code}")

            if response.status_code != 200:
                print("DEBUG API Error:", response.text)
                return []

            data = response.json()

            jobs = []

            for item in data.get("data", []):

                job = {
                    "title": item.get("job_title", "Unknown title"),
                    "company": item.get("employer_name", "Unknown company"),
                    "location": item.get("job_city", location),
                    "link": item.get("job_apply_link")
                }

                jobs.append(job)

            print(f"DEBUG Jobs fetched: {len(jobs)}")

            return jobs


        except Exception as e:
            print(f"DEBUG Unexpected error: {str(e)}")
            return []