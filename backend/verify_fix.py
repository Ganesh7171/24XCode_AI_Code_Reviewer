import os
import sys
import traceback
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from llm.reviewer import CodeReviewer

def verify():
    load_dotenv()
    print("Initializing CodeReviewer...")
    try:
        reviewer = CodeReviewer()
        print(f"LLM initialized: {reviewer.llm}")
        
        # Test with a very simple code snippet
        code = "def add(a, b): return a + b"
        description = "A simple addition function"
        standards = [] # Empty standards for testing
        
        print("\nAttempting to review code...")
        result = reviewer.review_code(code, description, standards)
        
        print("\nReview results:")
        if result.get('issues') and "Error during review" in result['issues'][0]:
            print(f"ERROR: {result['issues'][0]}")
            print(f"Explanation: {result.get('explanation')}")
        else:
            print(f"Issues: {result.get('issues')}")
            print(f"Risks: {result.get('risks')}")
            print(f"Explanation: {result.get('explanation')[:100]}...")
        
        if result.get('issues') and "Error during review" in str(result.get('issues')):
            print("\nFAILED: Still getting error during review.")
        else:
            print("\nSUCCESS: Code review completed successfully.")
            
    except Exception as e:
        print(f"\nCRITICAL ERROR during verification:")
        traceback.print_exc()

if __name__ == "__main__":
    verify()
