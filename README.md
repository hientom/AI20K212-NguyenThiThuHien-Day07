# 📚 Lab 7: Data Foundations - Embedding & Vector Store

**Họ và tên:** Nguyễn Thị Thu Hiền  
**Lớp/Mã lớp:** AI20K212  
**Nhóm:** 30  
**Ngày hoàn thành:** 10/04/2026

---

## 📖 Giới thiệu (Overview)
Dự án này là bài tập thực hành Lab 7, tập trung vào việc xây dựng nền tảng dữ liệu (Data Foundations) cho một hệ thống RAG (Retrieval-Augmented Generation). 
Hệ thống được thiết kế để xử lý, lưu trữ và truy xuất thông tin dựa trên ngữ nghĩa (Semantic Search).

**Domain dữ liệu áp dụng:** Truyện ngắn & Tiểu thuyết tình yêu.

## 📂 Cấu trúc thư mục (Project Structure)
Dự án được tổ chức theo cấu trúc sau:

```text
AI20K212-NguyenThiThuHien-Day07/
├── report/
│   └── REPORT.md         # Báo cáo phân tích chi tiết các chiến lược Chunking & Kết quả đánh giá
├── src/
│   ├── agent.py          # Class KnowledgeBaseAgent xử lý prompt và tích hợp LLM
│   ├── chunking.py       # Chứa các thuật toán chia nhỏ văn bản (FixedSize, Sentence, Recursive)
│   └── store.py          # Class EmbeddingStore xử lý lưu trữ vector và tìm kiếm (Cosine Similarity)
├── data/                 # (Chứa các file .txt tiểu thuyết gốc)
├── .env                  # File cấu hình biến môi trường (Local / OpenAI)
└── README.md             # Tài liệu hướng dẫn (File này)
