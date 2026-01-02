from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.job_normalizer import normalize_job_data
from utils.classifier import classify_job_priority

app = FastAPI(title="Job Automation Intelligence API")

# --- Data Models ---
class JobRaw(BaseModel):
    title: str
    company: str
    url: str
    description: str
    source: str = "Unknown"

class ClassificationRequest(BaseModel):
    role_title: str

class ScoreRequest(BaseModel):
    job_description: str
    resume_text: str
    role_title: str

class CoverLetterRequest(BaseModel):
    company: str
    role_title: str
    my_name: str
    skills: str = "Python, Automation, and Data Analysis"

# --- Endpoints ---

@app.get("/")
def health_check():
    return {"status": "running", "service": "Job Automation Intelligence Engine"}

@app.post("/normalize")
def api_normalize(job: JobRaw):
    data = job.model_dump()
    normalized = normalize_job_data(data)
    if not normalized:
        raise HTTPException(status_code=400, detail="Could not normalize job data")
    return normalized

@app.post("/classify")
def api_classify(req: ClassificationRequest):
    domains = {
        "Data Science": ["data scientist", "machine learning", "ai", "nlp", "analyst"],
        "Software Engineering": ["software", "developer", "engineer", "stack", "backend", "web"],
        "Business": ["business", "manager", "operations", "marketing"]
    }
    return classify_job_priority(req.role_title, domains)

@app.post("/score")
def api_score(req: ScoreRequest):
    from ats_scorer import ATSScorer
    scorer = ATSScorer()
    try:
        return scorer.calculate_score(req.job_description, req.resume_text, req.role_title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_cover_letter")
def api_cover_letter(req: CoverLetterRequest):
    """
    Generates a generic, professional cover letter without using paid LLMs.
    """
    template = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {req.role_title} position at {req.company}. 

With my background in {req.skills}, I am confident in my ability to contribute effectively to your team. I have been following {req.company}'s work and admire your commitment to innovation. 

I have attached my resume for your review. Thank you for your time and consideration.

Sincerely,
{req.my_name}
"""
    return {"content": template}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
