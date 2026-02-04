"""
FastAPI Main Application
AI Code Reviewer with RAG Pipeline
"""

import os
import logging
from typing import Optional, List
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from rag.loader import StandardsLoader
from rag.embedder import EmbeddingGenerator
from rag.retriever import StandardsRetriever
from llm.reviewer import CodeReviewer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
embeddings_generator = None
retriever = None
code_reviewer = None
standards_loader = None
init_error = None  # Track initialization error

# Pydantic models for request/response
class CodeReviewRequest(BaseModel):
    """Request model for code review"""
    code: str = Field(..., description="Source code to review")
    description: str = Field(..., description="Description of the code")
    language: Optional[str] = Field("python", description="Programming language")


class CodeReviewResponse(BaseModel):
    """Response model for code review"""
    issues: list[str] = Field(..., description="List of issues found")
    risks: list[str] = Field(..., description="List of potential risks")
    improvements: list[str] = Field(..., description="List of suggested improvements")
    refactored_code: str = Field(..., description="Refactored code")
    explanation: str = Field(..., description="Explanation of changes")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str
    rag_initialized: bool
    llm_initialized: bool
    error: Optional[str] = None


async def initialize_rag_pipeline():
    """
    Initialize the RAG pipeline components.
    """
    global embeddings_generator, retriever, code_reviewer, standards_loader, init_error
    
    try:
        logger.info("Initializing RAG pipeline")
        init_error = None
        
        # Get configuration from environment
        standards_dir = os.getenv("STANDARDS_DIR", "../standards")
        faiss_index_path = os.getenv("FAISS_INDEX_PATH", "./faiss_index")
        aws_profile = os.getenv("AWS_PROFILE")
        
        # Initialize standards loader
        standards_loader = StandardsLoader(standards_dir)
        
        # Initialize embeddings
        # Check if Bedrock should be used (either access key or profile present)
        use_bedrock = bool(os.getenv("AWS_ACCESS_KEY_ID") or aws_profile)
        embeddings_generator = EmbeddingGenerator(use_bedrock=use_bedrock, aws_profile=aws_profile)
        
        # Initialize retriever
        retriever = StandardsRetriever(
            embeddings=embeddings_generator.get_embeddings(),
            index_path=faiss_index_path
        )
        
        # Load and index standards if index doesn't exist
        if retriever.vector_store is None:
            logger.info("No existing index found, creating new one")
            documents = standards_loader.load_documents()
            if documents:
                retriever.create_index(documents)
            else:
                logger.warning("No standards documents found to index")
        
        # Initialize code reviewer
        code_reviewer = CodeReviewer(aws_profile=aws_profile)
        
        logger.info("RAG pipeline initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing RAG pipeline: {str(e)}")
        init_error = str(e)
        # Don't raise - allow app to start even if RAG init fails


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    """
    # Startup
    logger.info("Starting AI Code Reviewer application")
    await initialize_rag_pipeline()
    yield
    # Shutdown
    logger.info("Shutting down AI Code Reviewer application")


# Initialize FastAPI app
app = FastAPI(
    title="AI Code Reviewer",
    description="AI-powered code review using RAG and AWS Bedrock",
    version="1.0.0",
    lifespan=lifespan
)

# Configure rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "AI Code Reviewer API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload_standards": "/upload-standards",
            "review_code": "/review-code"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    global retriever, code_reviewer, init_error
    
    # Lazy init attempt if still not initialized
    if retriever is None or code_reviewer is None:
        await initialize_rag_pipeline()

    rag_initialized = retriever is not None and retriever.vector_store is not None
    llm_initialized = code_reviewer is not None and code_reviewer.llm is not None
    
    status = "healthy" if (rag_initialized and llm_initialized) else "degraded"
    
    return HealthResponse(
        status=status,
        message="AI Code Reviewer is running",
        rag_initialized=rag_initialized,
        llm_initialized=llm_initialized,
        error=init_error
    )


@app.post("/upload-standards", tags=["Standards"])
@limiter.limit(f"{os.getenv('RATE_LIMIT_REQUESTS', '10')}/minute")
async def upload_standards(
    request: Request,
    payload: dict = {},
    file: Optional[UploadFile] = File(None)
):
    """
    Upload new coding standards to the RAG system.
    
    Accepts either a file upload or text content in the request body.
    """
    try:
        if retriever is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        documents = []
        
        # Handle file upload
        if file:
            logger.info(f"Processing uploaded file: {file.filename}")
            
            # Check file size
            max_size_mb = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
            content = await file.read()
            
            if len(content) > max_size_mb * 1024 * 1024:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Max size: {max_size_mb}MB"
                )
            
            # Create document from file
            text = content.decode('utf-8')
            doc = standards_loader.load_from_text(text, source=file.filename)
            documents.append(doc)
        
        # Handle text content
        elif payload and "content" in payload:
            logger.info("Processing text content")
            text = payload["content"]
            source = payload.get("source", "uploaded_text")
            doc = standards_loader.load_from_text(text, source=source)
            documents.append(doc)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either file or content must be provided"
            )
        
        # Add documents to index
        retriever.add_documents(documents)
        
        return {
            "status": "success",
            "message": f"Added {len(documents)} document(s) to standards",
            "documents_count": len(documents)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading standards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/review-code", response_model=CodeReviewResponse, tags=["Review"])
@limiter.limit(f"{os.getenv('RATE_LIMIT_REQUESTS', '10')}/minute")
async def review_code(request: Request, review_data: CodeReviewRequest):
    """
    Review code using RAG and LLM.
    
    Retrieves relevant coding standards and uses them to review the provided code.
    """
    try:
        if retriever is None or code_reviewer is None:
            # Try to initialize if not done
            await initialize_rag_pipeline()
            if retriever is None or code_reviewer is None:
                raise HTTPException(
                    status_code=503,
                    detail=f"RAG system or code reviewer not initialized. Error: {init_error}"
                )
        
        logger.info("Processing code review request")
        
        # Create search query from code and description
        search_query = f"{review_data.description}\n\nLanguage: {review_data.language}\n\nCode snippet:\n{review_data.code[:500]}"
        
        # Retrieve relevant standards
        logger.info("Retrieving relevant standards")
        relevant_standards = retriever.retrieve(search_query, k=3)
        
        logger.info(f"Retrieved {len(relevant_standards)} relevant standards")
        
        # Review code
        review_result = code_reviewer.review_code(
            code=review_data.code,
            description=review_data.description,
            relevant_standards=relevant_standards
        )
        
        logger.info("Code review completed")
        
        return CodeReviewResponse(**review_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during code review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reload-standards", tags=["Standards"])
async def reload_standards():
    """
    Reload all standards from the standards directory.
    """
    try:
        if retriever is None or standards_loader is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        logger.info("Reloading standards from directory")
        
        # Load documents
        documents = standards_loader.load_documents()
        
        if not documents:
            return {
                "status": "warning",
                "message": "No standards documents found",
                "documents_count": 0
            }
        
        # Recreate index
        retriever.create_index(documents)
        
        return {
            "status": "success",
            "message": "Standards reloaded successfully",
            "documents_count": len(documents)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reloading standards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
