# 🚀 Mini SQL Server - Student Management (B-Tree Indexing)

Ứng dụng mô phỏng cơ chế vận hành của một hệ quản trị cơ sở dữ liệu (DBMS) sử dụng cấu trúc dữ liệu **B-Tree bậc 3** làm chỉ mục (Index) để tối ưu hóa hiệu suất truy vấn.

## ⚙️ Cơ chế vận hành hệ thống

Ứng dụng được thiết kế dựa trên nguyên lý tách biệt giữa dữ liệu vật lý và bộ chỉ mục (Indexing):

### 1. Phân tách bộ nhớ (Memory Architecture)
* **Heap Table (Bảng gốc):** Lưu trữ toàn bộ thông tin sinh viên bao gồm: *Mã SV, Họ Tên, Giới tính, Lớp, Quốc tịch, Ngày sinh*. Dữ liệu được thêm theo cơ chế **Append-only** (luôn thêm vào cuối bảng), đảm bảo tốc độ ghi $O(1)$.
* **B-Tree Index (Chỉ mục):** Một cây B-Tree bậc 3 tự động sắp xếp theo khóa `MaSV`. Mỗi nút trên cây chỉ lưu cặp giá trị `(Mã SV, Pointer)`, trong đó Pointer là vị trí dòng dữ liệu tương ứng trong bảng gốc.

### 2. Thuật toán xử lý trên B-Tree bậc 3
* **Cơ chế Tách nút (Splitting):** Tuân thủ quy tắc cây bậc 3 (2-3 Tree). Khi một nút đạt ngưỡng 3 khóa, hệ thống tự động thực hiện thuật toán `Split` để đẩy khóa trung tâm lên làm nút cha, duy trì độ cao cây ở mức $\log_3(n)$.
* **Tìm kiếm tối ưu (Index Seek):** Sử dụng thuật toán duyệt cây để tìm kiếm theo Mã SV với độ phức tạp $O(\log n)$, thay vì quét toàn bộ bảng $O(n)$.
* **Xóa dữ liệu (Lazy Deletion):** Để đảm bảo hiệu năng và tránh việc tái cấu trúc cây liên tục, ứng dụng sử dụng cơ chế xóa mềm: Đánh dấu `IsDeleted = True` tại bảng gốc và gán `Pointer = -1` trên Index.

---

## 💻 Trình giả lập lệnh SQL (SQL Editor)

Ứng dụng tích hợp bộ phân giải lệnh SQL cơ bản để người dùng thao tác trực tiếp bằng câu lệnh:

| Câu lệnh SQL | Cơ chế thực thi (Execution Plan) | Mục tiêu |
| :--- | :--- | :--- |
| `SELECT * FROM SinhVien` | **Full Table Scan** | Hiển thị toàn bộ dữ liệu trong bảng gốc. |
| `SELECT * FROM SinhVien WHERE MaSV = 'SV01'` | **Index Seek** | Truy cập nhanh qua B-Tree để lấy dữ liệu. |

---

## 🛠 Hướng dẫn chạy ứng dụng

### 1. Sử dụng file thực thi (.exe)
* Truy cập mục **Releases** trên thanh Menu bên phải.
* Tải file `MiniSQLServer.exe` và chạy trực tiếp trên Windows (Không cần cài đặt môi trường).

### 2. Chạy từ mã nguồn Python
Yêu cầu Python 3.x trở lên:
```bash
# Di chuyển vào thư mục chứa code
cd src
# Khởi chạy ứng dụng
python mini_sql_server.py
