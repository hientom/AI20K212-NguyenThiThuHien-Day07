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
```
## ⚙️ Cấu hình và Cài đặt (Setup & Configuration)
Để hệ thống chạy mượt mà, vui lòng thực hiện đúng 2 bước cấu hình dưới đây:

**1. Cài đặt thư viện môi trường**

Mở Terminal tại thư mục gốc của dự án và chạy lệnh sau để cài đặt các package cần thiết:
```
pip install pytest python-dotenv sentence-transformers openai
```
**2. Thiết lập file biến môi trường (.env)**

Tạo một file có tên chính xác là .env tại thư mục gốc (ngang hàng với thư mục src). Tùy vào nhu cầu sử dụng, hãy copy và dán một trong hai cấu hình sau vào file:

**🔹 Lựa chọn A: Dùng Local Model (Khuyên dùng)**

Chạy offline, hoàn toàn miễn phí và không bị lỗi giới hạn lượt gọi (Rate Limit 429). Khi chạy lần đầu, máy sẽ tự động tải model all-MiniLM-L6-v2 về.
```
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
```
**🔹 Lựa chọn B: Dùng OpenAI API (Yêu cầu có Key)**

Dành cho trường hợp muốn test sức mạnh thực sự của mô hình xịn từ OpenAI. Lưu ý nếu dùng Key miễn phí (như Github Token) có thể bị giới hạn 150 requests/ngày.

```
EMBEDDING_PROVIDER=openai
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=dán_api_key_của_bạn_vào_đây
```

## 🚀 Hướng dẫn sử dụng (Usage)
**1. Chạy Unit Test kiểm tra Core Implementation:**
Chạy toàn bộ test case do giảng viên cung cấp để đảm bảo source code hoạt động chuẩn xác:

```
pytest tests/ -v
```
