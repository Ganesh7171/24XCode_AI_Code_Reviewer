import os
import sys
import boto3
from dotenv import load_dotenv

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from llm.reviewer import CodeReviewer
from rag.embedder import EmbeddingGenerator

def test_auth():
    print("Loading environment variables...")
    load_dotenv()
    
    profile = os.getenv("AWS_PROFILE")
    region = os.getenv("AWS_REGION")
    
    print(f"Configuration:")
    print(f"  AWS_PROFILE: {profile}")
    print(f"  AWS_REGION: {region}")
    
    if not profile:
        print("\nWARNING: AWS_PROFILE is not set. Using default credentials chain or failing if none found.")
    
    try:
        print("\n--- Testing CodeReviewer Initialization ---")
        reviewer = CodeReviewer(aws_profile=profile)
        print("[PASS] CodeReviewer initialized successfully.")
        
        # Verify it has a client
        if reviewer.llm and reviewer.llm.client:
            print(f"   Client service name: {reviewer.llm.client.meta.service_model.service_name}")
            print(f"   Client region: {reviewer.llm.client.meta.region_name}")
        
    except Exception as e:
        print(f"[FAIL] CodeReviewer initialization failed: {e}")

    try:
        print("\n--- Testing EmbeddingGenerator Initialization ---")
        embedder = EmbeddingGenerator(use_bedrock=True, aws_profile=profile)
        print("[PASS] EmbeddingGenerator initialized successfully.")
        
        # Verify it has a client
        if embedder.embeddings and embedder.embeddings.client:
             print(f"   Client service name: {embedder.embeddings.client.meta.service_model.service_name}")
             print(f"   Client region: {embedder.embeddings.client.meta.region_name}")

    except Exception as e:
        print(f"[FAIL] EmbeddingGenerator initialization failed: {e}")

if __name__ == "__main__":
    test_auth()
