import re

def classify_job_priority(role_title: str, domain_keywords: dict) -> dict:
    """
    Classifies the domain, level, and calculates priority score.
    
    Priority Rules:
    5 (Mid) > 4 (Junior) > 3 (Associate) > 1 (Intern)
    """
    role_lower = role_title.lower()
    
    # 1. Domain Detection
    detected_domain = "Other"
    for domain, keywords in domain_keywords.items():
        if any(k in role_lower for k in keywords):
            detected_domain = domain
            break
            
    # 2. Level Detection
    level = "Mid" # Default to high priority to catch ambiguous mid-level roles
    priority = 5
    
    if "intern" in role_lower:
        level = "Intern"
        priority = 1
    elif "associate" in role_lower:
        level = "Associate"
        priority = 3
    elif "junior" in role_lower or "jr." in role_lower or "entry" in role_lower:
        level = "Junior"
        priority = 4
    elif "senior" in role_lower or "lead" in role_lower or "manager" in role_lower or "principal" in role_lower:
        # We might want to filter these out or give them lower priority if strictly targeting Mid
        level = "Senior" 
        priority = 2 # Lower priority than Mid for this specific user config? Or maybe 6?
                     # User said: Mid (Highest), Junior, Associate, Intern. 
                     # Let's assume Senior is not target, so priority 2.
    
    return {
        "domain": detected_domain,
        "level": level,
        "priority_score": priority
    }

if __name__ == "__main__":
    domains = {
        "Data Science": ["data scientist", "machine learning", "ai engineer", "analyst"],
        "Software Engineering": ["software", "developer", "full stack", "backend", "frontend"],
        "Business": ["business", "operations", "product", "manager"]
    }
    
    print(classify_job_priority("Junior Machine Learning Engineer", domains))
