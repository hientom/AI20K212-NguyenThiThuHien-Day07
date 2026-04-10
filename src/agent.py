from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        # Lưu lại các tham chiếu (references) để sử dụng trong các method khác
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        # 1. Truy xuất top-k chunks liên quan nhất từ vector store
        retrieved_records = self.store.search(question, top_k=top_k)
        
        # Trích xuất phần văn bản (text) từ các record trả về
        context_texts = [record.get("text", "") for record in retrieved_records]
        
        # Nối các chunk lại thành một đoạn ngữ cảnh duy nhất, phân tách bằng dấu xuống dòng
        context = "\n---\n".join(context_texts)
        
        # 2. Xây dựng prompt kết hợp ngữ cảnh và câu hỏi của người dùng
        prompt = (
            f"Please answer the following question based on the provided context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )
        
        # 3. Gọi ham LLM (được truyền vào từ __init__) để sinh ra câu trả lời cuối cùng
        return self.llm_fn(prompt)
