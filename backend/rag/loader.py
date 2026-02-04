"""
Document Loader Module
Loads coding standards and best practices from the standards directory.
"""

import os
import logging
from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StandardsLoader:
    """
    Loads coding standards documents from a specified directory.
    Supports .md, .txt, and other text-based files.
    """
    
    def __init__(self, standards_dir: str):
        """
        Initialize the loader with the standards directory path.
        
        Args:
            standards_dir: Path to the directory containing standards documents
        """
        self.standards_dir = Path(standards_dir)
        if not self.standards_dir.exists():
            logger.warning(f"Standards directory does not exist: {standards_dir}")
            self.standards_dir.mkdir(parents=True, exist_ok=True)
    
    def load_documents(self) -> List[Document]:
        """
        Load all documents from the standards directory.
        
        Returns:
            List of LangChain Document objects
        """
        try:
            logger.info(f"Loading documents from {self.standards_dir}")
            
            documents = []
            
            # Load markdown files
            if list(self.standards_dir.glob("*.md")):
                md_loader = DirectoryLoader(
                    str(self.standards_dir),
                    glob="**/*.md",
                    loader_cls=TextLoader,
                    loader_kwargs={'encoding': 'utf-8'}
                )
                documents.extend(md_loader.load())
            
            # Load text files
            if list(self.standards_dir.glob("*.txt")):
                txt_loader = DirectoryLoader(
                    str(self.standards_dir),
                    glob="**/*.txt",
                    loader_cls=TextLoader,
                    loader_kwargs={'encoding': 'utf-8'}
                )
                documents.extend(txt_loader.load())
            
            logger.info(f"Loaded {len(documents)} documents")
            
            # Add metadata to documents
            for doc in documents:
                if not doc.metadata.get('source'):
                    doc.metadata['source'] = 'standards'
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            return []
    
    def load_from_text(self, text: str, source: str = "uploaded") -> Document:
        """
        Create a document from raw text.
        
        Args:
            text: Raw text content
            source: Source identifier for the document
            
        Returns:
            LangChain Document object
        """
        return Document(
            page_content=text,
            metadata={"source": source}
        )
