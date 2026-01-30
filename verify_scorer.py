
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    from ats_scorer import ATSScorer
    print("✅ Successfully imported ATSScorer")
except ImportError as e:
    print(f"❌ Failed to import ATSScorer: {e}")
    sys.exit(1)

def test_scorer():
    try:
        from api import ScoreRequest, api_score # Test via API function directly if possible, or use requests
    except ImportError:
        # Fallback to direct request via requests lib isn't possible as we don't have it installed in script
        # We will test the API logic by mocking the request object if we can import it, 
        # or simplified: we will just use curl to test the endpoint.
        pass

if __name__ == "__main__":
    # We will use curl for the real test since we need to hit the running API
    print("Please run the curl command to verify.")

if __name__ == "__main__":
    test_scorer()
