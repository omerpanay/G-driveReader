from abc import ABC, abstractmethod
from typing import Sequence, List, Any
from llama_index.core import Document
from llama_index.core.schema import BaseNode


class EmbeddingMethod(ABC):
    """Abstract base class for embedding methods."""

    @abstractmethod
    def get_documents(self, *args, **kwargs) -> Sequence[Document]:
        pass

    @abstractmethod
    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        pass

    @abstractmethod
    def process(
        self,
        vector_store: Any,
        task_manager: Any,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        """
        Belgeleri alır, node'lara çevirir ve vector_store'a yazar.
        task_manager gibi parametreler gerçek üretimde progress raporu için kullanılabilir.
        """
        pass