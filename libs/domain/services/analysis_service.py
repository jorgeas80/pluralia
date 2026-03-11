from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple

class NewsAnalyzer(ABC):
    """Interface for analyzing news articles."""

    @abstractmethod
    async def analyze_sensationalism(self, title: str, content: str) -> Tuple[float, str, Dict]:
        """
        Analyzes the sensationalism of a news article.

        Args:
            title: The title of the article.
            content: The content/description of the article.

        Returns:
            A tuple containing:
            - score (float): The sensationalism index (0.0 - 1.0)
            - explanation (str): Brief explanation
            - metadata (dict): Raw analysis data (counts, etc.)
        """
        pass
