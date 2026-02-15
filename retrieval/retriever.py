"""
Retrieval System for Insurance Document Corpus
Uses sentence transformers for embeddings and FAISS for vector search
"""

import os
from typing import List, Dict, Tuple
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle


@dataclass
class DocumentChunk:
    """Represents a chunk of a document with metadata"""
    text: str
    document_name: str
    chunk_id: int
    start_char: int
    end_char: int


class DocumentRetriever:
    """Retrieval system with embedding and vector search"""
    
    def __init__(self, documents_dir: str = "./data/documents"):
        self.documents_dir = documents_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks: List[DocumentChunk] = []
        self.index = None
        self.embeddings = None
        
    def load_documents(self) -> List[Tuple[str, str]]:
        """Load all text documents from the directory"""
        documents = []
        for filename in os.listdir(self.documents_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.documents_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append((filename, content))
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def chunk_document(self, document_name: str, content: str, 
                       chunk_size: int = 500, overlap: int = 50) -> List[DocumentChunk]:
        """Split document into overlapping chunks"""
        chunks = []
        chunk_id = 0
        
        # Split by paragraphs first to maintain context
        paragraphs = content.split('\n\n')
        current_chunk = ""
        start_char = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If adding this paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append(DocumentChunk(
                    text=current_chunk.strip(),
                    document_name=document_name,
                    chunk_id=chunk_id,
                    start_char=start_char,
                    end_char=start_char + len(current_chunk)
                ))
                chunk_id += 1
                
                # Keep overlap from previous chunk
                words = current_chunk.split()
                overlap_words = words[-overlap:] if len(words) > overlap else words
                current_chunk = ' '.join(overlap_words) + '\n\n' + para
                start_char = start_char + len(current_chunk) - len(' '.join(overlap_words)) - len(para) - 2
            else:
                if current_chunk:
                    current_chunk += '\n\n' + para
                else:
                    current_chunk = para
        
        # Add the last chunk
        if current_chunk:
            chunks.append(DocumentChunk(
                text=current_chunk.strip(),
                document_name=document_name,
                chunk_id=chunk_id,
                start_char=start_char,
                end_char=start_char + len(current_chunk)
            ))
        
        return chunks
    
    def build_index(self, force_rebuild: bool = False):
        """Build FAISS index from documents"""
        index_path = "./data/faiss_index.pkl"
        
        # Try to load existing index
        if not force_rebuild and os.path.exists(index_path):
            print("Loading existing index...")
            with open(index_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.chunks = saved_data['chunks']
                self.embeddings = saved_data['embeddings']
                self.index = saved_data['index']
            print(f"Loaded index with {len(self.chunks)} chunks")
            return
        
        print("Building new index...")
        # Load and chunk all documents
        documents = self.load_documents()
        self.chunks = []
        
        for doc_name, content in documents:
            doc_chunks = self.chunk_document(doc_name, content)
            self.chunks.extend(doc_chunks)
        
        print(f"Created {len(self.chunks)} chunks from {len(documents)} documents")
        
        # Generate embeddings
        print("Generating embeddings...")
        chunk_texts = [chunk.text for chunk in self.chunks]
        self.embeddings = self.model.encode(chunk_texts, show_progress_bar=True)
        
        # Build FAISS index
        print("Building FAISS index...")
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        # Save index
        print("Saving index...")
        with open(index_path, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'embeddings': self.embeddings,
                'index': self.index
            }, f)
        
        print("Index built and saved successfully")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for relevant chunks with citations"""
        # Encode query
        query_embedding = self.model.encode([query])[0]
        
        # Search in FAISS
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'), k
        )
        
        # Prepare results with citations
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            chunk = self.chunks[idx]
            results.append({
                'text': chunk.text,
                'document': chunk.document_name,
                'chunk_id': chunk.chunk_id,
                'citation': f"[{chunk.document_name}, chunk_{chunk.chunk_id}]",
                'relevance_score': float(1 / (1 + dist))  # Convert distance to similarity
            })
        
        return results
    
    def get_chunk_by_citation(self, document_name: str, chunk_id: int) -> str:
        """Retrieve specific chunk by citation reference"""
        for chunk in self.chunks:
            if chunk.document_name == document_name and chunk.chunk_id == chunk_id:
                return chunk.text
        return None


def initialize_retriever(force_rebuild: bool = False) -> DocumentRetriever:
    """Initialize and return the document retriever"""
    retriever = DocumentRetriever()
    retriever.build_index(force_rebuild=force_rebuild)
    return retriever