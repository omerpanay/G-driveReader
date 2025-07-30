from typing import Sequence, List, Protocol
from llama_index.core.schema import Document, BaseNode

class EmbeddingMethod(Protocol):
    """Common protocol for all embedding methods"""

    def get_documents(self, data_source_id: str) -> Sequence[Document]:
        """Get documents from the data source."""
        raise NotImplementedError

    def get_nodes(self, documents: Sequence[Document]) -> Sequence[BaseNode]:
        """Process documents and return nodes."""
        raise NotImplementedError

    @staticmethod
    def customize_metadata(
        document: Document, data_source_id: str, **kwargs
    ) -> Document:
        """Modify metadata of the nodes."""
        raise NotImplementedError

    def apply_rules(
        self,
        documents: Sequence[Document],
        inclusion_rules: List[str],
        exclusion_rules: List[str],
    ) -> Sequence[Document]:
        """Apply rules to the documents."""
        raise NotImplementedError

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        """Process the embedding method with the given parameters."""
        raise NotImplementedError 