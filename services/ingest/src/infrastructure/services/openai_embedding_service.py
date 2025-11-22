"""OpenAI implementation of the embedding service."""
import os
from typing import Optional
from openai import OpenAI
import math

from libs.domain.services.embedding_service import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):
    """OpenAI implementation for generating and comparing text embeddings."""

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        """
        Initialize the OpenAI embedding service.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from OPENAI_API_KEY env var.
            model: Name of the OpenAI embedding model to use. Default is text-embedding-3-small.
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text using OpenAI API.
        
        Args:
            text: Text to generate embedding for.
            
        Returns:
            List of floats representing the embedding (1536 dimensions for text-embedding-3-small).
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        response = self._client.embeddings.create(
            model=self._model,
            input=text.strip(),
        )
        
        return response.data[0].embedding

    def calculate_similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.
            
        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical).
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have the same dimension")
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in embedding1))
        magnitude2 = math.sqrt(sum(b * b for b in embedding2))
        
        # Avoid division by zero
        if magnitude1 == 0.0 or magnitude2 == 0.0:
            return 0.0
        
        # Cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        return float(similarity)

