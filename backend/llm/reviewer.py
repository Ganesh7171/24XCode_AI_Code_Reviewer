"""
Code Reviewer Module
Uses AWS Bedrock LLM to review code based on retrieved standards.
"""

import os
import json
import logging
from typing import Dict, List, Optional
import boto3
from langchain_community.chat_models import BedrockChat
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeReviewer:
    """
    AI-powered code reviewer using AWS Bedrock and RAG.
    """
    
    def __init__(
        self,
        aws_region: Optional[str] = None,
        model_id: Optional[str] = None,
        aws_profile: Optional[str] = None
    ):
        """
        Initialize the code reviewer.
        
        Args:
            aws_region: AWS region for Bedrock
            model_id: Bedrock model ID for code review
            aws_profile: AWS CLI profile to use
        """
        self.region = aws_region or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv(
            "BEDROCK_MODEL_ID",
            "anthropic.claude-3.5-sonnet-20240620-v1:0"
        )
        self.aws_profile = aws_profile or os.getenv("AWS_PROFILE")
        
        self.llm = None
        self._init_llm()
        
        # Define the review prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["code", "description", "standards"],
            template="""You are an expert code reviewer. Review the following code based on the provided coding standards and best practices.

**Coding Standards and Best Practices:**
{standards}

**Code Description:**
{description}

**Code to Review:**
```
{code}
```

**Instructions:**
1. Analyze the code for issues, bugs, security vulnerabilities, and violations of the provided standards.
2. Identify risks and potential problems.
3. Suggest specific improvements.
4. Stricltly Provide full refactored code that addresses the issues.
5. Explain your reasoning.

**Output Format:**
Respond ONLY with valid JSON in the following format (no markdown, no code blocks):
{{
  "issues": ["issue 1", "issue 2", ...],
  "risks": ["risk 1", "risk 2", ...],
  "improvements": ["improvement 1", "improvement 2", ...],
  "refactored_code": "complete refactored code here",
  "explanation": "detailed explanation of changes and reasoning"
}}
"""
        )
    
    def _init_llm(self):
        """
        Initialize AWS Bedrock LLM.
        """
        try:
            logger.info(f"Initializing Bedrock LLM with model: {self.model_id}")
            
            # Create session if profile is provided
            if self.aws_profile:
                session = boto3.Session(profile_name=self.aws_profile)
                bedrock_client = session.client(
                    service_name='bedrock-runtime',
                    region_name=self.region
                )
            else:
                # Use default session
                bedrock_client = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=self.region
                )
            
            # Initialize LLM with appropriate parameters
            self.llm = BedrockChat(
                client=bedrock_client,
                model_id=self.model_id,
                model_kwargs={
                    "max_tokens": 4096,
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            )
            
            logger.info("Bedrock LLM initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Bedrock LLM: {str(e)}")
            raise
    
    def review_code(
        self,
        code: str,
        description: str,
        relevant_standards: List[Document]
    ) -> Dict:
        """
        Review code using retrieved standards and LLM.
        
        Args:
            code: Source code to review
            description: Description of the code's purpose
            relevant_standards: Retrieved relevant coding standards
            
        Returns:
            Dictionary containing review results
        """
        try:
            logger.info("Starting code review")
            
            # Format standards context
            standards_text = self._format_standards(relevant_standards)
            
            # Create prompt
            prompt = self.prompt_template.format(
                code=code,
                description=description,
                standards=standards_text
            )
            
            logger.info("Sending request to Bedrock LLM")
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            logger.info("Received response from LLM")
            
            # Extract text from response if it's a message object
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # Parse JSON response
            review_result = self._parse_response(response_text)
            
            return review_result
            
        except Exception as e:
            logger.error(f"Error during code review: {str(e)}")
            return {
                "issues": [f"Error during review: {str(e)}"],
                "risks": [],
                "improvements": [],
                "refactored_code": code,
                "explanation": "An error occurred during the review process."
            }
    
    def _format_standards(self, standards: List[Document]) -> str:
        """
        Format retrieved standards into a readable context.
        
        Args:
            standards: List of relevant standard documents
            
        Returns:
            Formatted standards text
        """
        if not standards:
            return "No specific coding standards provided. Use general best practices."
        
        formatted = []
        for i, doc in enumerate(standards, 1):
            source = doc.metadata.get('source', 'unknown')
            formatted.append(f"Standard {i} (from {source}):\n{doc.page_content}\n")
        
        return "\n".join(formatted)
    
    def _parse_response(self, response: str) -> Dict:
        """
        Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed review dictionary
        """
        try:
            # Try to extract JSON from response
            # Handle cases where LLM might wrap JSON in markdown code blocks
            response = response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith("```"):
                lines = response.split("\n")
                # Remove first and last lines (```)
                response = "\n".join(lines[1:-1])
                # Remove language identifier if present
                if response.startswith("json"):
                    response = response[4:].strip()
            
            # Parse JSON
            result = json.loads(response)
            
            # Validate required fields
            required_fields = ["issues", "risks", "improvements", "refactored_code", "explanation"]
            for field in required_fields:
                if field not in result:
                    result[field] = [] if field != "refactored_code" and field != "explanation" else ""
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response was: {response}")
            
            # Return a fallback structure with the raw response
            return {
                "issues": ["Failed to parse LLM response as JSON"],
                "risks": [],
                "improvements": [],
                "refactored_code": "",
                "explanation": f"Raw response: {response}"
            }
