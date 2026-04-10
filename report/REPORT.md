# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Thị Thu Hiền

**Nhóm:** 30

**Ngày:** 10/04/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> *Góc giữa hai vector rất nhỏ (gần 0 độ), thể hiện rằng hai đoạn văn bản có nội dung, ngữ nghĩa hoặc ngữ cảnh rất giống nhau.*

**Ví dụ HIGH similarity:**
- Sentence A: "Con mèo đang ngủ bên ngoài nắng bên sân vườn"
- Sentence B: "Chú mèo mun đang say giấc trên ghế sofa"
- Tại sao tương đồng:Cùng miêu tả một sự việc (mèo ngủ trên ghế) nhưng dùng từ ngữ đồng nghĩa.

**Ví dụ LOW similarity:**
- Sentence A:"Công thức làm sữa chưa lên men tự nhiên"
- Sentence B: "Giá xăng hôm nay giảm hơn hôm qua

- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn kahsc nhau (Ẩm thực và Kinh tế), không có từ vựng hay ngữ nghĩa chung

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> *Vì Cosine Similarity chỉ quan tâm đến hướng của vector (nghĩa của từ/câu) mà bỏ qua độ dài vector (tần suất xuất hiện từ hay độ dài câu), giúp so sánh các đoạn văn bản ngắn dài khác nhau công bằng hơn.*

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> *Kích thước thực tế bước nhảy (step) = chunk_size - overlap = 500 - 50 = 450. Số chunk = (10000 - 50) / 450 = 22.11 -> Làm tròn lên là 23 chunks.*
> *Đáp án: 23 chunks.*

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> *Nếu overlap=100, step = 400. Số chunk = (10000 - 100) / 400 = 24.75 -> Tăng lên thành 25 chunks.*

> *Chúng ta muốn overlap nhiều hơn để bảo toàn ngữ cảnh (context) giữa các đoạn cắt, đặc biệt trong tiểu thuyết, việc này giúp tránh làm đứt gãy mạch cảm xúc hoặc các câu thoại quan trọng bị chia làm đôi.*

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Truyện ngắn / Tiểu thuyết tình yêu

**Tại sao nhóm chọn domain này?**
> Tiểu thuyết chứa rất nhiều hội thoại đan xen, miêu tả nội tâm phức tạp và sử dụng dày đặc các đại từ nhân xưng (anh, cô, hắn). Việc dùng RAG cho domain này rất thử thách để kiểm tra xem hệ thống có duy trì được mạch truyện và phân biệt được các nhân vật hay không.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| | | | |
| | | | |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Strategy Của Tôi

**Loại:** [FixedSizeChunker / SentenceChunker / RecursiveChunker / custom strategy]

**Mô tả cách hoạt động:**
> *Viết 3-4 câu: strategy chunk thế nào? Dựa trên dấu hiệu gì?*

**Tại sao tôi chọn strategy này cho domain nhóm?**
> *Viết 2-3 câu: domain có pattern gì mà strategy khai thác?*

**Code snippet (nếu custom):**
```python
# Paste implementation here
```

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| | best baseline | | | |
| | **của tôi** | | | |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | | | | |
| [Tên] | | | | |
| [Tên] | | | | |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> *Viết 2-3 câu:*

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> *Viết 2-3 câu: dùng regex gì để detect sentence? Xử lý edge case nào?*

**`RecursiveChunker.chunk` / `_split`** — approach:
> *Viết 2-3 câu: algorithm hoạt động thế nào? Base case là gì?*

### EmbeddingStore

**`add_documents` + `search`** — approach:
> *Viết 2-3 câu: lưu trữ thế nào? Tính similarity ra sao?*

**`search_with_filter` + `delete_document`** — approach:
> *Viết 2-3 câu: filter trước hay sau? Delete bằng cách nào?*

### KnowledgeBaseAgent

**`answer`** — approach:
> *Viết 2-3 câu: prompt structure? Cách inject context?*

### Test Results

```
# Paste output of: pytest tests/ -v
```

**Số tests pass:** __ / __

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | high / low | | |
| 2 | | | high / low | | |
| 3 | | | high / low | | |
| 4 | | | high / low | | |
| 5 | | | high / low | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> *Viết 2-3 câu:*

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu queries trả về chunk relevant trong top-3?** __ / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> *Viết 2-3 câu:*

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> *Viết 2-3 câu:*

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | / 5 |
| Document selection | Nhóm | / 10 |
| Chunking strategy | Nhóm | / 15 |
| My approach | Cá nhân | / 10 |
| Similarity predictions | Cá nhân | / 5 |
| Results | Cá nhân | / 10 |
| Core implementation (tests) | Cá nhân | / 30 |
| Demo | Nhóm | / 5 |
| **Tổng** | | **/ 100** |
