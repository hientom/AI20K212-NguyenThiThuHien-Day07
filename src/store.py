from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb  # noqa: F401

            self._client = chromadb.Client()
            self._collection = self._client.get_or_create_collection(name=self._collection_name)
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        # Lấy nội dung từ trường content (ko dùng text nữa)
        content = getattr(doc, "content", getattr(doc, "text", ""))
        metadata = getattr(doc, "metadata", {}).copy()
        
        # Bắt buộc phải gắn doc_id vào metadata để sau này hàm delete còn tìm được mà xóa
        metadata["doc_id"] = doc.id
        
        self._next_index += 1
        record_id = f"chunk_{self._next_index}"
        
        embedding = self._embedding_fn(content)
        
        return {
            "id": record_id,
            "content": content,  # Sử dụng key "content" theo đúng yêu cầu test
            "embedding": embedding,
            "metadata": metadata
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        query_embedding = self._embedding_fn(query)
        
        scored_records = []
        for record in records:
            score = _dot(query_embedding, record["embedding"])
            scored_records.append((score, record))
            
        scored_records.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, record in scored_records[:top_k]:
            result_record = record.copy()
            result_record["score"] = score
            results.append(result_record)
            
        return results

    def add_documents(self, docs: list[Document]) -> None:
        if not docs:
            return
            
        records = [self._make_record(doc) for doc in docs]

        if self._use_chroma and self._collection is not None:
            ids = [r["id"] for r in records]
            documents = [r["content"] for r in records]
            embeddings = [r["embedding"] for r in records]
            metadatas = [r["metadata"] for r in records]
            
            self._collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        else:
            self._store.extend(records)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if self._use_chroma and self._collection is not None:
            query_embedding = self._embedding_fn(query)
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            formatted_results = []
            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return formatted_results
        else:
            return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        if self._use_chroma and self._collection is not None:
            return self._collection.count()
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        if not metadata_filter:
            return self.search(query, top_k)

        if self._use_chroma and self._collection is not None:
            query_embedding = self._embedding_fn(query)
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=metadata_filter
            )
            
            formatted_results = []
            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return formatted_results
        else:
            filtered_records = []
            for record in self._store:
                is_match = True
                for key, value in metadata_filter.items():
                    if record.get("metadata", {}).get(key) != value:
                        is_match = False
                        break
                if is_match:
                    filtered_records.append(record)
                    
            return self._search_records(query, filtered_records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        if self._use_chroma and self._collection is not None:
            initial_count = self._collection.count()
            self._collection.delete(where={"doc_id": doc_id})
            return self._collection.count() < initial_count
        else:
            initial_length = len(self._store)
            self._store = [
                record for record in self._store 
                if record.get("metadata", {}).get("doc_id") != doc_id
            ]
            return len(self._store) < initial_length