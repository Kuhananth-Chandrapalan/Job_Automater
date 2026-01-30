import spacy
from typing import List, Dict, Tuple
import re

class ATSScorer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model not found, though we should ensure it's installed
            print("Warning: Spacy model 'en_core_web_sm' not found. Downloading...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def _extract_entities_and_nouns(self, text: str) -> set:
        doc = self.nlp(text)
        keywords = set()
        
        # 1. Extract Entities (ORG, PERSON, WORK_OF_ART, PRODUCT, GPE, LANGUAGE)
        valid_labels = {"ORG", "PRODUCT", "WORK_OF_ART", "LANGUAGE", "GPE"}
        for ent in doc.ents:
            if ent.label_ in valid_labels:
                keywords.add(ent.text.lower())
        
        # 2. Extract Noun Chunks (better than single words)
        for chunk in doc.noun_chunks:
            clean_chunk = chunk.text.lower().strip()
            # Filter out very common stop-word heavy chunks
            if len(clean_chunk.split()) <= 3 and clean_chunk not in self.nlp.Defaults.stop_words:
                keywords.add(clean_chunk)
                
        return keywords

    def calculate_score(self, job_description: str, resume_text: str, role_title: str) -> Dict:
        """
        Calculates a compatibility score using NLP entity and noun matching.
        """
        jd_keywords = self._extract_entities_and_nouns(job_description)
        resume_keywords = self._extract_entities_and_nouns(resume_text)
        
        if not jd_keywords:
            return {"score": 0.0, "reason": "Empty Job Description"}

        # 1. Keyword/Entity Match Ratio (50%)
        # intersection
        common_keywords = jd_keywords.intersection(resume_keywords)
        # We assume JD has the "required" set.
        keyword_match_ratio = len(common_keywords) / len(jd_keywords) if len(jd_keywords) > 0 else 0
        
        # 2. Section Analysis (Simple Check) (10%)
        # Does the resume have standard sections?
        sections = ["experience", "education", "skills", "projects", "work history"]
        resume_lower = resume_text.lower()
        section_score = sum(1 for s in sections if s in resume_lower) / len(sections)
        
        # 3. Role Title Relevance (20%)
        # Check if the role title words appear in the resume (indicating previous experience)
        role_doc = self.nlp(role_title)
        role_terms = {token.text.lower() for token in role_doc if not token.is_stop}
        title_match = 0
        if role_terms:
            title_hits = sum(1 for term in role_terms if term in resume_text.lower())
            title_match = title_hits / len(role_terms)

        # 4. Critical Skills Boost (20%)
        # If we find "years" or numeric entities near skills in JD, we could be smarter.
        # For now, we just weight the direct entity match heavily.
        
        # Weighted Final Score
        raw_score = (keyword_match_ratio * 0.5) + (section_score * 0.1) + (title_match * 0.2)
        
        # Boost if match ratio is high (bonus)
        if keyword_match_ratio > 0.5:
            raw_score += 0.1
            
        final_score = round(min(max(raw_score, 0.0), 1.0), 2)
        
        return {
            "score": final_score,
            "missing_keywords": list(jd_keywords - resume_keywords)[:15],
            "details": {
                "keyword_match_ratio": round(keyword_match_ratio, 2),
                "title_match": round(title_match, 2),
                "section_completeness": round(section_score, 2)
            }
        }

if __name__ == "__main__":
    scorer = ATSScorer()
    jd = "Seeking a Data Scientist with Python, SQL, and AWS experience."
    resume = "I am a Data Scientist. I know Python and SQL."
    print(scorer.calculate_score(jd, resume, "Data Scientist"))
