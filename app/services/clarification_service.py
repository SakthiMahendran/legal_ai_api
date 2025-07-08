import os
from clarification.graphSearch import LegalSearchGraph
from clarification.summarize import LegalSummarizer


class ClarificationService:
    """
    Service wrapper for legal clarification/search agent logic for FastAPI integration.
    """

    def __init__(self):
        self.search_graph = LegalSearchGraph(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.summarizer = LegalSummarizer(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
        )

    def clarify_query(self, query: str, summary_type: str = "comprehensive") -> dict:
        # Run search
        search_results = self.search_graph.search_legal_query(query)
        # Summarize results
        summary = self.summarizer.summarize_search_results(search_results, summary_type)
        return {"search_results": search_results, "summary": summary}

    def summarize_results(
        self, search_results: dict, summary_type: str = "comprehensive"
    ) -> dict:
        return self.summarizer.summarize_search_results(search_results, summary_type)

    def health_check(self) -> dict:
        return {
            "status": "healthy",
            "ai_configured": bool(self.search_graph and self.summarizer),
            "modules_loaded": True,
            "debug_mode": False,
        }
