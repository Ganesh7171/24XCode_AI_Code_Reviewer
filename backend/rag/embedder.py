"""
Embedding Module
Generates embeddings for documents using AWS Bedrock or HuggingFace models.
"""

import os
import logging
from typing import List, Optional
import boto3
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings using AWS Bedrock Titan or HuggingFace models.
    Falls back to HuggingFace if Bedrock is not configured.
    """
    
    def __init__(
        self,
        use_bedrock: bool = True,
        aws_region: Optional[str] = None,
        model_id: Optional[str] = None,
        aws_profile: Optional[str] = None
    ):
        """
        Initialize the embedding generator.
        
        Args:
            use_bedrock: Whether to use AWS Bedrock (True) or HuggingFace (False)
            aws_region: AWS region for Bedrock
            model_id: Bedrock embedding model ID
            aws_profile: AWS CLI profile to use
        """
        self.use_bedrock = use_bedrock
        self.aws_profile = aws_profile or os.getenv("AWS_PROFILE")
        self.embeddings = None
        
        if use_bedrock:
            try:
                self._init_bedrock_embeddings(aws_region, model_id)
            except Exception as e:
                logger.warning(f"Failed to initialize Bedrock embeddings: {str(e)}")
                logger.info("Falling back to HuggingFace embeddings")
                self._init_huggingface_embeddings()
        else:
            self._init_huggingface_embeddings()
    
    def _init_bedrock_embeddings(
        self,
        aws_region: Optional[str] = None,
        model_id: Optional[str] = None
    ):
        """
        Initialize AWS Bedrock embeddings.
        
        Args:
            aws_region: AWS region
            model_id: Bedrock model ID for embeddings
        """
        region = aws_region or os.getenv("AWS_REGION", "us-east-1")
        embedding_model = model_id or os.getenv(
            "BEDROCK_EMBEDDING_MODEL_ID",
            "amazon.titan-embed-text-v1"
        )
        
        logger.info(f"Initializing Bedrock embeddings with model: {embedding_model}")
        
        # Create Bedrock client with profile if provided
        if self.aws_profile:
            session = boto3.Session(profile_name=self.aws_profile)
            bedrock_client = session.client(
                service_name='bedrock-runtime',
                region_name=region
            )
        else:
            bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=region
            )
        
        self.embeddings = BedrockEmbeddings(
            client=bedrock_client,
            model_id=embedding_model
        )
        
        logger.info("Bedrock embeddings initialized successfully")
    
    def _init_huggingface_embeddings(self):
        """
        Initialize HuggingFace embeddings as fallback.
        Uses sentence-transformers model for local execution.
        """
        logger.info("Initializing HuggingFace embeddings")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        logger.info("HuggingFace embeddings initialized successfully")
    
    def get_embeddings(self):
        """
        Get the embeddings instance.
        
        Returns:
            LangChain embeddings object
        """
        return self.embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        
        Args:
            texts: List of document texts
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
