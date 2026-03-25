"""
ChromaDB Adapter — Facade for the ChromaDB vector database.

Implements: FR-CHROMA-010–013, DR-CHROMA-001–003.
"""

from typing import Any, Optional


class ChromaDBAdapter:
    """Facade for querying the pre-seeded ChromaDB knowledge base.

    Collections (pre-seeded at build time):
    - architectural_patterns: C4/UML diagram templates
    - quality_attributes: ISO 25010 quality taxonomy
    - plantuml_syntax: PlantUML syntax reference
    - scoring_rubrics: SA evaluation criteria/examples
    """

    COLLECTIONS = [
        "architectural_patterns",
        "quality_attributes",
        "plantuml_syntax",
        "scoring_rubrics",
    ]

    def __init__(self, base_url: str) -> None:
        """Initialize adapter.

        Args:
            base_url: ChromaDB HTTP server URL (e.g., "http://i-architect-chromadb:8000").
        """
        self.base_url = base_url

    def query(
        self,
        collection_name: str,
        query_text: str,
        n_results: int = 5,
        where_filter: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """Query a collection for relevant documents (FR-CHROMA-010).

        Args:
            collection_name: Target collection name.
            query_text: Natural language query string.
            n_results: Maximum number of results to return.
            where_filter: Optional metadata filter.

        Returns:
            List of matched document chunks with metadata and distances.
        """
        raise NotImplementedError

    def get_collection_info(self, collection_name: str) -> dict[str, Any]:
        """Get metadata about a collection (FR-CHROMA-012).

        Args:
            collection_name: Collection to inspect.

        Returns:
            Dict with 'name', 'count', 'metadata'.
        """
        raise NotImplementedError

    def health_check(self) -> bool:
        """Check ChromaDB server and collection availability (DR-CHROMA-002).

        Returns:
            True if server is reachable and all 4 collections exist.
        """
        raise NotImplementedError
