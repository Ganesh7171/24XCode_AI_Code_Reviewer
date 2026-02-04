"""
Retriever Module
Manages FAISS vector store for similarity search of coding standards.
"""

import os
import logging
from typing import List, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StandardsRetriever:
    """
    Manages FAISS vector store for retrieving relevant coding standards.
    """
    
    def __init__(
        self,
        embeddings,
        index_path: Optional[str] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the retriever.
        
        Args:
            embeddings: LangChain embeddings instance
            index_path: Path to save/load FAISS index
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.embeddings = embeddings
        self.index_path = Path(index_path) if index_path else Path("./faiss_index")
        self.vector_store: Optional[FAISS] = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Try to load existing index
        self._load_index()
    
    def _load_index(self):
        """
        Load existing FAISS index from disk if available.
        """
        try:
            if self.index_path.exists():
                logger.info(f"Loading FAISS index from {self.index_path}")
                self.vector_store = FAISS.load_local(
                    str(self.index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("FAISS index loaded successfully")
            else:
                logger.info("No existing FAISS index found")
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            self.vector_store = None
    
    def create_index(self, documents: List[Document]):
        """
        Create a new FAISS index from documents.
        
        Args:
            documents: List of LangChain Document objects
        """
        try:
            if not documents:
                logger.warning("No documents provided for indexing")
                return
            
            logger.info(f"Creating FAISS index from {len(documents)} documents")
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks")
            
            # Create vector store
            self.vector_store = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            
            # Save index to disk
            self._save_index()
            
            logger.info("FAISS index created successfully")
            
        except Exception as e:
            logger.error(f"Error creating FAISS index: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]):
        """
        Add new documents to existing index.
        
        Args:
            documents: List of LangChain Document objects
        """
        try:
            if not documents:
                logger.warning("No documents provided")
                return
            
            logger.info(f"Adding {len(documents)} documents to index")
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            if self.vector_store is None:
                # Create new index if none exists
                self.create_index(documents)
            else:
                # Add to existing index
                self.vector_store.add_documents(chunks)
                self._save_index()
            
            logger.info("Documents added successfully")
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def _save_index(self):
        """
        Save FAISS index to disk.
        """
        try:
            if self.vector_store is not None:
                self.index_path.mkdir(parents=True, exist_ok=True)
                self.vector_store.save_local(str(self.index_path))
                logger.info(f"FAISS index saved to {self.index_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            if self.vector_store is None:
                logger.warning("No vector store available for retrieval")
                return []
            
            logger.info(f"Retrieving top {k} documents for query")
            
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)
            
            logger.info(f"Retrieved {len(results)} documents")
            return results
            
        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return []
    
    def retrieve_with_scores(self, query: str, k: int = 3) -> List[tuple]:
        """
        Retrieve relevant documents with similarity scores.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        try:
            if self.vector_store is None:
                logger.warning("No vector store available for retrieval")
                return []
            
            logger.info(f"Retrieving top {k} documents with scores")
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            logger.info(f"Retrieved {len(results)} documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return []
