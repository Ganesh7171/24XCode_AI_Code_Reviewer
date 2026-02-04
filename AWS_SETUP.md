# AWS Bedrock SSO Setup Guide

This project supports using AWS Single Sign-On (SSO) for authentication with AWS Bedrock. This is the recommended secure way to access AWS resources.

## Prerequisites

1.  **AWS CLI v2**: Ensure you have the AWS CLI installed.
    - [Download AWS CLI](https://aws.amazon.com/cli/)
2.  **AWS Account**: Access to an AWS account with Bedrock access enable.

## Step 1: Configure AWS SSO Profile

Run the following command in your terminal (Command Prompt or PowerShell):

```powershell
aws configure sso
```

You will be prompted to enter the following information (replace with your specific details):

1.  **SSO session name**: (e.g., `my-sso`)
2.  **SSO start URL**: (e.g., `https://my-company.awsapps.com/start`)
3.  **SSO region**: (e.g., `us-east-1` - this is where your SSO is configured)
4.  **Registration scopes**: Leave default (`sso:account:access`)

The browser will open to authorize the request.

After authorization, selecting the account/role:

5.  **CLI Profile name**: Give this a meaningful name (e.g., `bedrock-dev`). **Remember this name.**

## Step 2: Login

Whenever your session expires, you simply run:

```powershell
aws sso login --profile bedrock-dev
```

## Step 3: Configure Application

Update your `.env` file in the `backend` directory (or create one from `.env.example`) to use this profile.

```ini
# .env file

# Use the profile name you defined in Step 1
AWS_PROFILE=bedrock-dev

# Region where Bedrock models are enabled (might be different from SSO region)
AWS_REGION=us-east-1

# Optional: Specific Model IDs
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

## Verification

To verify it works, run the backend locally:

```powershell
cd backend
run_local.bat
```

If you see `Bedrock LLM initialized successfully` in the logs, it is working.
