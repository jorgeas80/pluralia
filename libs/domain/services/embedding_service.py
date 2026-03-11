"""Abstract interface for embedding services."""
from abc import ABC, abstractmethod
from typing import Optional


class EmbeddingService(ABC):
    """Abstract interface for generating and comparing text embeddings."""

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: Text to generate embedding for.
            
        Returns:
            List of floats representing the embedding vector.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_similarity(self, embedding1: list[float], embedding2: list[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.
            
        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical).
        """
        raise NotImplementedError

