import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_job_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes job data from various sources (Gmail, RSS) into a standard format.
    """
    try:
        # Extract fields with safe defaults
        job_url = raw_data.get('url') or raw_data.get('link', '')
        
        # Generate deterministic ID
        job_id = hashlib.sha256(job_url.encode('utf-8')).hexdigest() if job_url else None
        
        if not job_id:
            logging.warning("Skipping job with no URL")
            return None

        normalized = {
            "job_id": job_id,
            "date_found": datetime.now().isoformat(),
            "company": raw_data.get('company', 'Unknown'),
            "role_title": raw_data.get('title', 'Unknown'),
            "location": raw_data.get('location', 'Remote'), # Default to Remote if missing
            "description": raw_data.get('description', ''),
            "job_url": job_url,
            "source": raw_data.get('source', 'Unknown'),
            "apply_method": "Email" if "@" in raw_data.get('description', '') else "Portal", # Basic heuristic
            "status": "New"
        }
        
        return normalized

    except Exception as e:
        logging.error(f"Error normalizing job data: {e}")
        return None

# Example Usage for n8n Function Item Node
# In n8n, you would use: return normalize_job_data(items[0].json)
if __name__ == "__main__":
    sample_raw = {
        "title": "Senior Data Scientist",
        "company": "Tech Corp",
        "url": "https://techcorp.com/jobs/123",
        "description": "Send resume to careers@techcorp.com",
        "source": "Gmail Alert"
    }
    print(json.dumps(normalize_job_data(sample_raw), indent=2))
