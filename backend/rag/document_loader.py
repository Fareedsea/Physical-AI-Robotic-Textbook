"""
Document loader for the Physical AI & Humanoid Robotics Textbook
Handles loading and parsing textbook content for RAG system
"""

import os
import glob
from typing import List, Dict, Any
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class TextbookDocumentLoader:
    """Load and parse textbook content from Docusaurus markdown files"""

    def __init__(self, docs_path: str = "my-website/docs"):
        self.docs_path = Path(docs_path)
        self.supported_extensions = ['.md', '.mdx']

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Load all textbook documents from the docs directory
        Returns a list of documents with metadata
        """
        documents = []

        # Find all markdown files in the docs directory
        for ext in self.supported_extensions:
            pattern = str(self.docs_path / f"**/*{ext}")
            files = glob.glob(pattern, recursive=True)

            for file_path in files:
                try:
                    doc = self._load_single_document(file_path)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    logger.error(f"Error loading document {file_path}: {str(e)}")
                    continue

        logger.info(f"Loaded {len(documents)} documents from {self.docs_path}")
        return documents

    def _load_single_document(self, file_path: str) -> Dict[str, Any]:
        """Load and parse a single markdown document"""
        file_path = Path(file_path)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse markdown to extract content and metadata
        # First, separate frontmatter if present
        lines = content.split('\n')
        frontmatter = {}
        content_body = content

        if lines and lines[0].strip() == '---':
            # Find the end of frontmatter
            end_frontmatter_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_frontmatter_idx = i
                    break

            if end_frontmatter_idx > 0:
                frontmatter_content = '\n'.join(lines[1:end_frontmatter_idx])
                content_body = '\n'.join(lines[end_frontmatter_idx + 1:])

                # Parse frontmatter (simplified - in real implementation, use pyyaml)
                for line in frontmatter_content.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip().strip('"\'')

        # Convert markdown to plain text for indexing
        html = markdown.markdown(content_body)
        soup = BeautifulSoup(html, 'html.parser')
        plain_text = soup.get_text()

        # Extract chapter/section information from path
        relative_path = file_path.relative_to(self.docs_path)
        path_parts = str(relative_path).split('/')

        # Determine chapter information
        chapter_info = self._extract_chapter_info(path_parts, frontmatter)

        document = {
            'id': str(file_path),
            'content': plain_text,
            'metadata': {
                'source': str(file_path),
                'relative_path': str(relative_path),
                'chapter': chapter_info.get('chapter', ''),
                'section': chapter_info.get('section', ''),
                'title': frontmatter.get('title', ''),
                'sidebar_position': frontmatter.get('sidebar_position'),
                'raw_frontmatter': frontmatter
            }
        }

        return document

    def _extract_chapter_info(self, path_parts: List[str], frontmatter: Dict[str, Any]) -> Dict[str, str]:
        """Extract chapter and section information from file path and frontmatter"""
        chapter = ""
        section = ""

        # Look for chapter indicators in the path
        for part in path_parts:
            if 'chapter' in part.lower():
                chapter = part
                break

        # If no chapter found in path, try to infer from frontmatter
        if not chapter and frontmatter.get('title'):
            title = frontmatter['title'].lower()
            if 'chapter' in title:
                chapter = frontmatter['title']

        # Section is typically the filename without extension
        if path_parts:
            section = Path(path_parts[-1]).stem

        return {
            'chapter': chapter,
            'section': section
        }

def load_textbook_documents(docs_path: str = "my-website/docs") -> List[Dict[str, Any]]:
    """
    Convenience function to load all textbook documents
    """
    loader = TextbookDocumentLoader(docs_path)
    return loader.load_documents()

if __name__ == "__main__":
    # Test the document loader
    docs = load_textbook_documents()
    print(f"Loaded {len(docs)} documents")
    if docs:
        print(f"First document: {docs[0]['metadata']['title'] if docs[0]['metadata']['title'] else docs[0]['metadata']['relative_path']}")