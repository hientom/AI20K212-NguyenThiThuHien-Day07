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
- Tại sao tương đồng: Cùng miêu tả một sự việc (mèo ngủ trên ghế) nhưng dùng từ ngữ đồng nghĩa.

**Ví dụ LOW similarity:**
- Sentence A: "Công thức làm sữa chua lên men tự nhiên"
- Sentence B: "Giá xăng hôm nay giảm hơn hôm qua"
- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn khác nhau (Ẩm thực và Kinh tế), không có từ vựng hay ngữ nghĩa chung.

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

**Domain:** Truyện ngắn / Tiểu thuyết tình yêu.

**Tại sao nhóm chọn domain này?**
> *Tiểu thuyết chứa rất nhiều hội thoại đan xen, miêu tả nội tâm phức tạp và sử dụng dày đặc các đại từ nhân xưng (anh, cô, hắn). Việc dùng RAG cho domain này rất thử thách để kiểm tra xem hệ thống có duy trì được mạch truyện và phân biệt được các nhân vật hay không.*

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | 48 giờ yêu nhau | Truyện ngắn | 9,500 | `{"source": "48_gio_yeu_nhau.txt", "author": "Hà Thanh Phúc"}` |
| 2 | Anh đừng lỗi hẹn | Truyện ngắn | 8,200 | `{"source": "anh_dung_loi_hen.txt", "author": "Vũ Đức Nghĩa"}` |
| 3 | Ánh Mắt Yêu Thương | Tiểu thuyết | 45,000 | `{"source": "anh_mat_yeu_thuong.txt", "author": "Nguyễn Thị Phi Oanh"}` |
| 4 | Anh ơi, cùng nhau ta vượt biển | Truyện ngắn | 5,100 | `{"source": "anh_oi_cung_nhau_vuot_bien.txt", "author": "Áo Vàng"}` |
| 5 | Anh Sẽ Đến | Tiểu thuyết | 52,000 | `{"source": "anh_se_den.txt", "author": "Song Mai & Song Châu"}` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `source` | String | `"anh_se_den.txt"` | Giúp filter chính xác tài liệu cần tìm. Khi hỏi về nhân vật truyện A, ta có thể lọc bỏ toàn bộ chunks của truyện B để tránh nhiễu. |
| `author` | String | `"Hà Thanh Phúc"` | Hỗ trợ phân loại văn phong hoặc tìm kiếm các tác phẩm theo tác giả cụ thể. |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên tài liệu "48 giờ yêu nhau":

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| 48 giờ... | FixedSizeChunker (`fixed_size`) | 45 | 256 | Rất Kém (Cắt nát câu thoại) |
| 48 giờ... | SentenceChunker (`by_sentences`) | 30 | 315 | Khá (Giữ được câu, mất ý đoạn) |
| 48 giờ... | RecursiveChunker (`recursive`) | 22 | 430 | Tốt (Giữ trọn vẹn ngữ cảnh) |

### Strategy Của Tôi

**Loại:** `FixedSizeChunker` (chunk_size=256, overlap=50)

**Mô tả cách hoạt động:**
> *Chiến lược này cắt văn bản một cách cơ học dựa trên số lượng ký tự cứng. Nó sẽ lấy đúng 256 ký tự cho một chunk, sau đó lùi lại 50 ký tự (overlap khoảng 20%) và tiếp tục cắt chunk tiếp theo cho đến hết file.*

**Tại sao tôi chọn strategy này cho domain nhóm?**
> *Ban đầu, tôi chọn chiến lược này vì nó đơn giản, chạy nhanh và tạo ra các chunks có kích thước đồng đều, hy vọng giúp Embedding model (vốn giới hạn số token) xử lý trơn tru hơn.*

**Code snippet (nếu custom):**
```python
# Nằm trong src/chunking.py (FixedSizeChunker)
def chunk(self, text: str) -> list[str]:
    chunks = []
    step = self.chunk_size - self.chunk_overlap
    for i in range(0, len(text), step):
        chunks.append(text[i:i + self.chunk_size])
    return chunks
```
### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|---|---|---|---|---|
| Anh Sẽ Đến | best baseline (Recursive) | 120 | 450 | Tốt (Giữ được bối cảnh truyện) |
| Anh Sẽ Đến | của tôi (FixedSize 256) | 250 | 256 | Tạm ổn nhưng bị đứt đoạn |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|---|---|---|---|---|
| Tôi (Hiền) | FixedSize (256, overlap 50, top_k=3) | 9.0 | Kích thước đều, model embedding tốt nên vẫn vớt vát được điểm. | Thỉnh thoảng cắt ngang câu thoại dài khiến AI bị mất gốc ngữ cảnh (sai 1 câu). |
| Hiển | FixedSize (512, overlap 30%, top_k=5) | 8.5 | Context dài hơn của tôi một chút | Vẫn bị lỗi cắt cụt lủn giữa chừng. |
| Hậu | Sentence (3 câu/chunk, top_k=3) | 6.5 | Đảm bảo trọn vẹn cấu trúc ngữ pháp | Dễ bị mất bối cảnh của cả đoạn văn mô tả dài. |
| Dương | Recursive (400, top_k=4) | 9.0 | Giữ được cấu trúc đoạn văn bản | Đôi khi chunk hơi ngắn so với diễn biến truyện. |
| An | Recursive (700, top_k=5) | 10.0 | Bao quát trọn vẹn tình tiết và hội thoại | Chunk hơi dài, có thể chứa thông tin thừa. |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> Chiến lược RecursiveChunker với size lớn (như của bạn An: 700) là tốt nhất. Tiểu thuyết luôn có các lời thoại đi kèm đại từ nhân xưng và miêu tả nội tâm. Việc dùng FixedSize (chiến lược của tôi) vô tình chẻ đôi một câu thoại dài, khiến Agent không biết nhân vật đang nói chuyện với ai, dẫn đến việc lấy thiếu đáp án. Dù model Embed có xịn đến đâu cũng không thể bù đắp hoàn toàn lỗi cắt vụn này.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk` — approach:**
> Dùng regex `re.split(r'(?<=)\s+', text)` để chia văn bản thành danh sách các câu nhưng vẫn bảo toàn dấu câu ở cuối. Sau đó dùng vòng lặp gom đủ số câu `max_sentences` lại thành một chunk.

**`RecursiveChunker.chunk` / `_split` — approach:**
> Dùng thuật toán đệ quy. Base case là đoạn văn bản hiện tại <= `chunk_size` thì trả về luôn. Nếu lớn hơn, thử cắt bằng separator đầu tiên (ví dụ `\n\n`). Nếu phần bị cắt vẫn dài, đệ quy gọi lại hàm với separator tiếp theo (`\n`, rồi đến dấu cách).

### EmbeddingStore

**`add_documents` + `search` — approach:**
> `add_documents`: Lặp qua list văn bản, gọi `_embedding_fn` để chuyển text thành vector số học, lưu vào một List Dict. `search`: Lấy vector của query, tính Cosine Similarity với toàn bộ vector trong kho, sort giảm dần và trả về Top K.

**`search_with_filter` + `delete_document` — approach:**
> Filter trước: Duyệt qua các tài liệu, chỉ giữ lại những document có metadata khớp yêu cầu, sau đó mới mang đi tính similarity (Pre-filtering). Delete bằng cách dùng list comprehension để loại các dictionary có `id` tương ứng.

### KnowledgeBaseAgent

**`answer` — approach:**
> Lấy query gọi `store.search()` để ra danh sách Top K chunks. Nối text của các chunks này lại thành một biến Context. Inject nó vào `prompt_template` (chứa Context + Question) rồi đẩy vào LLM để sinh ra câu trả lời dựa trên văn cảnh.

### Test Results

```text
================================ short test summary info ================================
42 passed in 0.35s
```

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|---|---|---|---|---|---|
| 1 | "Anh nhẹ nhàng đan những ngón tay mình vào tay cô." | "Hắn khẽ khàng nắm lấy bàn tay nhỏ bé của cô ấy." | High | 0.89 | Đúng |
| 2 | "Cô gái bỏ đi không một lời từ biệt." | "Bảng xếp hạng tiểu thuyết bán chạy nhất." | Low | 0.11 | Đúng |
| 3 | "Tình yêu khiến người ta hạnh phúc." | "Em căm thù anh ta đến tận xương tủy." | Low | 0.58 | Sai |
| 4 | "Bọn họ hiểu lầm và cãi nhau gay gắt." | "Hai người lớn tiếng tranh luận không ngừng." | High | 0.82 | Đúng |
| 5 | "Mẫn Huy say sưa tìm những mẫu cát đủ màu." | "Công ty tranh cát của Hoàng Lạc bị phá sản." | Low | 0.35 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Kết quả Pair 3 (Tình yêu hạnh phúc vs Căm thù) bất ngờ có điểm khá cao (0.58). Điều này cho thấy Embeddings không chỉ học từ đồng nghĩa/trái nghĩa mà học theo "bối cảnh xuất hiện" (Contextual proximity). Cả Yêu và Hận đều hay xuất hiện chung trong các đoạn tiểu thuyết miêu tả mối quan hệ, nên vector của chúng bị kéo lại gần nhau.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`.
(Chạy thực tế bằng mô hình của tôi - `FixedSize(256)`: Đạt 4/5 PASSED)

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|---|---|
| 1 | Trong "Anh đừng lỗi hẹn", tại sao Thuý Hằng lại ly dị chồng và nguyên nhân nào dẫn đến bệnh tim của cô? | Vì chồng tẻ nhạt, tàn nhẫn, chỉ biết kiếm tiền khiến cô lo âu. Nỗi lo âu triền miên này sinh ra bệnh tim. |
| 2 | Nhân vật "tôi" gặp người con trai trong truyện (48 giờ yêu nhau) qua phương tiện nào? | Gặp qua blog trên mạng, để lại comment, sau đó thân thiết qua email và điện thoại. |
| 3 | Trong "Ánh Mắt Yêu Thương", biến cố nào đã khiến Hồ Ngọc bị tàn phế phải ngồi xe lăn? | Phát hiện vợ ngoại tình, con không phải cốt nhục của mình. Đau khổ, anh uống say đua xe ngã gãy chân và cột sống. |
| 4 | Tại sao em bé trong truyện "Anh ơi, cùng nhau ta vượt biển" lúc mới sinh ra mặt lại xanh lè và không khóc? | Vì bé nằm ngược, đầu to bị kẹt vai, bác sĩ phải dùng kềm kéo ra. Trễ vài giây nên thiếu oxy mặt xanh lè. |
| 5 | Trong "Anh Sẽ Đến", tại sao công ty tranh cát của Hoàng Lạc lại bị phá sản? | Do làm ăn gian dối, nhuộm màu cát thường thay vì dùng cát tự nhiên, khiến tranh phai màu, khách tẩy chay. |

### Kết Quả Của Tôi (FixedSize 256, Top K=3)

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|---|---|---|---|---|
| 1 | Trong Anh đừng lỗi hẹn, tại sao... | "...khiến em luôn cảm thấy lo âu. Có lẽ bệnh tim của em phát sinh từ đấy. Em đã trút bỏ được..." | 0.650 | Có | Thuý Hằng bị bệnh tim do lo âu triền miên về những đồng tiền chồng kiếm được. |
| 2 | Nhân vật "tôi" gặp người con trai... | "...Người nào cũng có một góc cô đơn. Tôi để lại comment. Tôi quen biết anh từ dạo đó..." | 0.710 | Có | Nhân vật tôi gặp anh qua việc để lại comment trên blog. |
| 3 | Trong Ánh Mắt Yêu Thương, biến cố... | "...đến khi ngã xe gãy đôi chân ấy. Vậy không gọi què, thì ba thằng Ngọc gọi con mình bằng gì..." | 0.580 | FAILED (Mất gốc) | Trượt ngưỡng 0.6 vì chunk chỉ nhắc đến ngã xe, bị đứt mất đoạn nguyên nhân vợ ngoại tình ở phía trước. |
| 4 | Tại sao em bé trong Anh ơi... | "...xanh lè, nên lúc ra được, bác sĩ chụp ngay thằng nhỏ, cho liền oxygene. Y tá chạy vù vù..." | 0.680 | Có | Em bé bị kẹt vai, phải dùng kềm nên mặt xanh lè và phải thở oxy. |
| 5 | Trong Anh Sẽ Đến, tại sao... | "...cát thường đem nhuộm thử hỏi làm sao mà không bị phá sản. Hoàng Lạc chống chế..." | 0.750 | Có | Vì Hoàng Lạc dùng cát thường đem nhuộm màu nên bị phá sản. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5 (80% - Đạt yêu cầu).

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Dù kết quả của em khá tốt (4/5) nhờ mô hình Embedding thông minh, nhưng em học được từ bạn An rằng với domain Tiểu thuyết, `overlap` không giải quyết triệt để được vấn đề mất bối cảnh nếu `chunk_size` quá nhỏ (như câu 3 của em bị FAILED do đứt đoạn). Việc dùng `RecursiveChunker` giúp RAG lôi được trọn vẹn ngữ cảnh.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Nhóm khác chia sẻ việc dùng API OpenAI thật sự (text-embedding-3-small) thay vì hàm Mock tự chế. AI thật sự hiểu được câu hỏi "Why nhân vật quyết vượt biển?" là ẩn dụ cho việc "đi đẻ" trong truyện, thay vì đi tìm chữ "vượt biển" trên đại dương.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Tôi sẽ vứt bỏ hoàn toàn `FixedSizeChunker` để chuyển sang `Recursive`. Ngoài ra, tôi sẽ tích hợp thêm tính năng gán Metadata Filter tên nhân vật. Trong tiểu thuyết, tên nhân vật thường xuyên lặp lại. Nếu có trường `metadata={"characters":}`, việc search sẽ chuẩn xác hơn và triệt tiêu được hiện tượng RAG bốc nhầm truyện.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|---|---|---|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 5 / 5 |
| **Tổng** | | **100 / 100** |