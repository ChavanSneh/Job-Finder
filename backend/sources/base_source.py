from abc import ABC, abstractmethod

class BaseSource(ABC):
    @abstractmethod
    def search_jobs(self, query: str, location: str) -> list:
        """Standardized interface for all scrapers/APIs."""
        pass