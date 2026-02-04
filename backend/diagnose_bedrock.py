import os
import boto3
import botocore.exceptions
from dotenv import load_dotenv

def check_bedrock():
    print("Loading environment variables...")
    load_dotenv()
    
    profile = os.getenv("AWS_PROFILE")
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
    
    print(f"Configuration:")
    print(f"  Profile: {profile}")
    print(f"  Region: {region}")
    print(f"  Model ID: {model_id}")
    
    try:
        print("\nAttempting to create generic boto3 session...")
        if profile:
            session = boto3.Session(profile_name=profile)
            print(f"  Session created using profile '{profile}'")
        else:
            session = boto3.Session()
            print("  Session created using default credentials")
            
        print("\nAttempting to create Bedrock Runtime client...")
        client = session.client(service_name='bedrock-runtime', region_name=region)
        print("  Client created successfully")
        
        print(f"\nAttempting to invoke model '{model_id}' (dry run/test)...")
        # Try a simple invoke to verify access
        try:
             # Just checking if we can even talk to the service, listing models is 'bedrock' not 'bedrock-runtime'
             # But CodeReviewer uses runtime.
             # We won't actually invoke because it costs money/needs payload.
             # We'll switch to 'bedrock' control plane to list foundation models to verify access.
             
             control_client = session.client(service_name='bedrock', region_name=region)
             print("  Control plane client created. Checking model access...")
             
             response = control_client.get_foundation_model(modelIdentifier=model_id)
             print(f"  SUCCESS: Model '{model_id}' is available and accessible.")
             
        except client.exceptions.AccessDeniedException:
             print("  ERROR: Access Denied. You might not have permissions (bedrock:GetFoundationModel).")
        except client.exceptions.ResourceNotFoundException:
             print(f"  ERROR: Model '{model_id}' not found in region '{region}'. Check region or model ID.")
        except Exception as e:
             print(f"  ERROR during model check: {e}")

    except botocore.exceptions.ProfileNotFound as e:
        print(f"\nCRITICAL ERROR: AWS Profile '{profile}' not found.")
        print("Run 'aws configure sso' and ensure you name the profile exactly matching AWS_PROFILE.")
    except botocore.exceptions.NoCredentialsError:
        print("\nCRITICAL ERROR: No AWS credentials found.")
        print("If using profile, ensure you have logged in: 'aws sso login --profile <name>'")
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")

if __name__ == "__main__":
    check_bedrock()
