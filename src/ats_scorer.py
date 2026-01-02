import re
import math
from typing import List, Dict, Tuple

class ATSScorer:
    def __init__(self):
        # In a real scenario, load NLP models or embeddings here
        pass

    def _normalize_text(self, text: str) -> str:
        return text.lower().strip()

    def _extract_keywords(self, text: str) -> set:
        # Simple regex based keyword extraction for demo
        # In production, use spaCy or KeyBERT
        words = re.findall(r'\b[a-zA-Z]{3,}\b', self._normalize_text(text))
        stop_words = {'and', 'the', 'for', 'with', 'you', 'that', 'are', 'this', 'from'}
        return set([w for w in words if w not in stop_words])

    def calculate_score(self, job_description: str, resume_text: str, role_title: str) -> Dict:
        """
        Calculates a compatibility score between 0.00 and 1.00.
        """
        jd_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(resume_text)
        
        if not jd_keywords:
            return {"score": 0.0, "reason": "Empty Job Description"}

        # 1. Keyword Match Ratio (40%)
        common_keywords = jd_keywords.intersection(resume_keywords)
        keyword_match_ratio = len(common_keywords) / len(jd_keywords)
        
        # 2. Title Similarity (Placeholder logic) (20%)
        # Check if key terms in role title exist in resume
        title_terms = set(self._extract_keywords(role_title))
        title_match = len(title_terms.intersection(resume_keywords)) / len(title_terms) if title_terms else 0
        
        # 3. Experience & Hard Skills Check (Placeholder) (40%)
        # Here we would look for specific "Must Haves" like "Python", "SQL", "3+ years"
        # For this skeleton, we assume a base heuristic
        skill_score = keyword_match_ratio * 1.2 # Boost if keywords match well
        
        # Weighted Final Score
        raw_score = (keyword_match_ratio * 0.5) + (title_match * 0.3) + (min(skill_score, 1.0) * 0.2)
        final_score = round(min(max(raw_score, 0.0), 1.0), 2)
        
        return {
            "score": final_score,
            "missing_keywords": list(jd_keywords - resume_keywords)[:10],
            "details": {
                "keyword_match": round(keyword_match_ratio, 2),
                "title_match": round(title_match, 2)
            }
        }

# Example Usage
if __name__ == "__main__":
    scorer = ATSScorer()
    
    jd = """
    We are looking for a Senior Data Scientist with Python, SQL, and Machine Learning experience.
    Must have experience with AWS and deploying models. 5+ years experience required.
    """
    
    resume = """
    Jane Doe. Data Scientist.
    Experienced in Python, SQL, and Machine Learning.
    Familiar with Azure and GCP.
    """
    
    role = "Senior Data Scientist"
    
    result = scorer.calculate_score(jd, resume, role)
    print(f"Role: {role}")
    print(f"Score: {result['score']}")
    print(f"Missing: {result['missing_keywords']}")
