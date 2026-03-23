import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# PHẦN 1: LOGIC B-TREE VÀ DATABASE (Cây Bậc 3)
# ==========================================
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []       
        self.data_ptrs = []  
        self.children = []   

class BTree:
    def __init__(self, t=2): # t=2 => Cây bậc 3 (Max 2 keys, 3 children)
        self.root = BTreeNode(True)
        self.t = t 

    def search(self, k, x=None):
        if x is None: x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]: i += 1
        if i < len(x.keys) and k == x.keys[i]: return x.data_ptrs[i]
        elif x.leaf: return None
        else: return self.search(k, x.children[i])

    def insert(self, k, ptr):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k, ptr)
        else:
            self._insert_non_full(root, k, ptr)

    def _insert_non_full(self, x, k, ptr):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            x.data_ptrs.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                x.data_ptrs[i + 1] = x.data_ptrs[i]
                i -= 1
            x.keys[i + 1] = k
            x.data_ptrs[i + 1] = ptr
        else:
            while i >= 0 and k < x.keys[i]: i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]: i += 1
            self._insert_non_full(x.children[i], k, ptr)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        x.data_ptrs.insert(i, y.data_ptrs[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        z.data_ptrs = y.data_ptrs[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        y.data_ptrs = y.data_ptrs[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    def delete_ptr(self, k):
        node_ptr = self._find_node(k, self.root)
        if node_ptr:
            node, idx = node_ptr
            node.data_ptrs[idx] = -1 # Lazy Deletion trên Index
            return True
        return False

    def _find_node(self, k, x):
        i = 0
        while i < len(x.keys) and k > x.keys[i]: i += 1
        if i < len(x.keys) and k == x.keys[i]: return (x, i)
        elif x.leaf: return None
        else: return self._find_node(k, x.children[i])

    def get_tree_string(self, x=None, l=0):
        if x is None: x = self.root
        res = "    " * l + f"Level {l} -> Keys: {x.keys} | Pointers: {x.data_ptrs}\n"
        for child in x.children:
            res += self.get_tree_string(child, l + 1)
        return res

class StudentDB:
    def __init__(self):
        self.raw_data = []  
        self.index = BTree(t=2) 

    def add(self, sv_id, name, gender, lop, quoc_tich, ngay_sinh):
        if self.index.search(sv_id) is not None and self.index.search(sv_id) != -1:
            return False, "Mã SV đã tồn tại!"
        
        # Bảng gốc lưu FULL thông tin
        record = {
            "MaSV": sv_id, "HoTen": name, "GioiTinh": gender, 
            "Lop": lop, "QuocTich": quoc_tich, "NgaySinh": ngay_sinh, 
            "IsDeleted": False
        }
        self.raw_data.append(record)
        
        # Index chỉ lưu Khóa và Vị trí
        self.index.insert(sv_id, len(self.raw_data) - 1)
        return True, "Thêm thành công!"

    def delete(self, sv_id):
        ptr = self.index.search(sv_id)
        if ptr is not None and ptr != -1:
            self.raw_data[ptr]["IsDeleted"] = True
            self.index.delete_ptr(sv_id)
            return True, "Xóa thành công!"
        return False, "Không tìm thấy Mã SV!"

    def search_id(self, sv_id):
        ptr = self.index.search(sv_id)
        if ptr is not None and ptr != -1:
            if not self.raw_data[ptr]["IsDeleted"]:
                return [self.raw_data[ptr]]
        return []

    def search_name(self, name):
        return [r for r in self.raw_data if name.lower() in r["HoTen"].lower() and not r["IsDeleted"]]


# ==========================================
# PHẦN 2: GIAO DIỆN UI 
# ==========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini SQL Server - Student Management (B-Tree Index)")
        self.geometry("1050x750")
        self.db = StudentDB()

        # --- Frame 1: Nhập liệu thông tin ---
        top_frame = tk.LabelFrame(self, text="Công cụ thao tác (GUI)", padx=10, pady=5)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(top_frame, text="Mã SV:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_id = tk.Entry(top_frame, width=12)
        self.entry_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(top_frame, text="Họ Tên:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.entry_name = tk.Entry(top_frame, width=20)
        self.entry_name.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(top_frame, text="Giới Tính:").grid(row=0, column=4, sticky=tk.W, pady=2)
        self.cb_gender = ttk.Combobox(top_frame, values=["Nam", "Nữ"], width=8)
        self.cb_gender.grid(row=0, column=5, padx=5, pady=2)
        self.cb_gender.current(0)

        tk.Label(top_frame, text="Lớp:").grid(row=0, column=6, sticky=tk.W, pady=2)
        self.entry_class = tk.Entry(top_frame, width=10)
        self.entry_class.grid(row=0, column=7, padx=5, pady=2)

        tk.Label(top_frame, text="Quốc Tịch:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_nat = tk.Entry(top_frame, width=12)
        self.entry_nat.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(top_frame, text="Ngày Sinh:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.entry_dob = tk.Entry(top_frame, width=20)
        self.entry_dob.grid(row=1, column=3, padx=5, pady=2)

        btn_frame = tk.Frame(top_frame)
        btn_frame.grid(row=2, column=0, columnspan=8, pady=5, sticky=tk.W)
        tk.Button(btn_frame, text="Thêm SV", bg="#4CAF50", fg="white", command=self.do_insert).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa SV (Theo Mã)", bg="#f44336", fg="white", command=self.do_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Làm mới Bảng", command=self.refresh_all).pack(side=tk.LEFT, padx=5)

        # --- Frame 2: Cửa sổ nhập lệnh SQL (New Feature) ---
        sql_frame = tk.LabelFrame(self, text="New Query (SQL Editor)", padx=10, pady=5, bg="#f0f8ff")
        sql_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry_sql = tk.Entry(sql_frame, width=100, font=("Consolas", 12))
        self.entry_sql.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        self.entry_sql.insert(0, "SELECT * FROM SinhVien WHERE MaSV = 'SV02'")

        tk.Button(sql_frame, text="▶ Execute", bg="#008CBA", fg="white", font=("Arial", 10, "bold"), command=self.execute_sql).pack(side=tk.LEFT, padx=5)

        # --- Frame 3: Bảng hiển thị kết quả ---
        mid_frame = tk.LabelFrame(self, text="Results (Data Storage)", padx=10, pady=5)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        columns = ("Index", "MaSV", "HoTen", "GioiTinh", "Lop", "QuocTich", "NgaySinh", "TrangThai")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings", height=6)
        headings = ["Pointer", "Mã SV", "Họ và Tên", "Giới Tính", "Lớp", "Quốc Tịch", "Ngày Sinh", "Trạng Thái"]
        widths = [60, 80, 150, 70, 80, 100, 100, 100]
        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- Frame 4: Console Log / Index Structure ---
        bot_frame = tk.LabelFrame(self, text="Messages & B-Tree Execution Plan", padx=10, pady=5)
        bot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_index = tk.Text(bot_frame, height=10, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11))
        self.text_index.pack(fill=tk.BOTH, expand=True)

    # --- CÁC HÀM XỬ LÝ SỰ KIỆN (Giữ nguyên do_insert, do_delete, refresh_all, update_table, log_message) ---
    def do_insert(self):
        sv_id, name, gender = self.entry_id.get().strip(), self.entry_name.get().strip(), self.cb_gender.get()
        lop, nat, dob = self.entry_class.get().strip(), self.entry_nat.get().strip(), self.entry_dob.get().strip()
        if not sv_id or not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập Mã SV và Họ Tên!")
            return
        success, msg = self.db.add(sv_id, name, gender, lop, nat, dob)
        if success:
            self.refresh_all()
            self.log_message(f"-> [INSERT] Đã thêm bản ghi vào cuối bảng gốc. Đã cập nhật B-Tree với Khóa '{sv_id}'.")
        else:
            messagebox.showerror("Lỗi", msg)

    def do_delete(self):
        sv_id = self.entry_id.get().strip()
        if not sv_id: return
        success, msg = self.db.delete(sv_id)
        if success:
            self.refresh_all()
            self.log_message(f"-> [DELETE] Đã đánh dấu xóa Mã SV '{sv_id}' trên Index và Bảng gốc.")
        else: messagebox.showerror("Lỗi", msg)

    # --- TÍNH NĂNG MỚI: TRÌNH PHÂN GIẢI LỆNH SQL ---
    def execute_sql(self):
        query = self.entry_sql.get().strip().upper()
        self.log_message(f"\n>>> Đang thực thi: {query}")

        if query == "SELECT * FROM SINHVIEN":
            self.update_table(self.db.raw_data)
            self.log_message("-> [Execution Plan]: TABLE SCAN (Quét toàn bộ bảng - O(n))")
            
        elif query.startswith("SELECT * FROM SINHVIEN WHERE MASV ="):
            try:
                # Cắt chuỗi để lấy mã SV (ví dụ: 'SV02')
                masv = self.entry_sql.get().split("=")[1].strip().strip("'").strip('"')
                results = self.db.search_id(masv)
                self.update_table(results)
                self.log_message(f"-> [Execution Plan]: INDEX SEEK (Duyệt cây B-Tree tìm khóa '{masv}' - O(log n))")
                if not results:
                    self.log_message(f"Không tìm thấy dữ liệu cho mã '{masv}'.")
            except Exception as e:
                messagebox.showerror("Lỗi cú pháp", "Cú pháp chuẩn: SELECT * FROM SinhVien WHERE MaSV = 'SV02'")
                
        else:
            messagebox.showwarning("Lỗi", "Trình giả lập SQL hiện chỉ hỗ trợ:\n1. SELECT * FROM SinhVien\n2. SELECT * FROM SinhVien WHERE MaSV = '...'")

    def refresh_all(self):
        self.update_table(self.db.raw_data, show_deleted=True)
        self.text_index.delete(1.0, tk.END)
        self.text_index.insert(tk.END, "TRẠNG THÁI CÂY B-TREE BẬC 3 HIỆN TẠI:\n" + "-"*40 + "\n")
        tree_str = self.db.index.get_tree_string()
        self.text_index.insert(tk.END, tree_str if tree_str.strip() else "(Cây rỗng)\n")

    def update_table(self, data_list, show_deleted=False):
        for row in self.tree.get_children(): self.tree.delete(row)
        for i, row in enumerate(self.db.raw_data):
            if row in data_list:
                if row["IsDeleted"] and not show_deleted: continue
                status = "ĐÃ XÓA (-)" if row["IsDeleted"] else "ACTIVE (+)"
                self.tree.insert("", "end", values=(i, row["MaSV"], row["HoTen"], row["GioiTinh"], row["Lop"], row["QuocTich"], row["NgaySinh"], status))

    def log_message(self, msg):
        self.text_index.insert(tk.END, msg + "\n")
        self.text_index.see(tk.END)

if __name__ == "__main__":
    app = App()
    
    # --- CHÈN DỮ LIỆU MẪU BAN ĐẦU ---
    # Mã SV được cố tình xếp lộn xộn để test tính năng tự sắp xếp và tách nút của B-Tree
    sample_data = [
        ("SV10", "Nguyen Van A", "Nam", "KTPM01", "Việt Nam", "01/01/2003"),
        ("SV02", "Tran Thi B", "Nữ", "KTPM02", "Việt Nam", "15/05/2003"),
        ("SV15", "John Doe", "Nam", "HTTT01", "Mỹ", "20/11/2002"),
        ("SV05", "Le Ngoc C", "Nữ", "KTPM01", "Việt Nam", "10/10/2003"),
        ("SV20", "Hoang Van D", "Nam", "KHMT01", "Việt Nam", "05/04/2002"),
        ("SV08", "Pham Thi E", "Nữ", "KTPM02", "Việt Nam", "22/12/2003"),
        ("SV01", "Vu Van F", "Nam", "MMT01", "Việt Nam", "14/02/2003"),
        ("SV12", "Alice Smith", "Nữ", "HTTT01", "Anh", "08/08/2003"),
        ("SV18", "Trinh Van G", "Nam", "KHMT02", "Việt Nam", "30/04/2002"),
        ("SV07", "Ngo Thi H", "Nữ", "KTPM01", "Việt Nam", "02/09/2003"),
        ("SV14", "Bui Van I", "Nam", "KTPM03", "Việt Nam", "19/05/2003"),
        ("SV04", "Dao Thi K", "Nữ", "KHMT01", "Việt Nam", "08/03/2003")
    ]

    for data in sample_data:
        app.db.add(data[0], data[1], data[2], data[3], data[4], data[5])

    app.refresh_all()
    
    # In ra một thông báo chào mừng nhỏ ở phần log
    app.log_message("-> [HỆ THỐNG]: Đã nạp thành công 12 bản ghi dữ liệu mẫu.")
    app.log_message("-> [HỆ THỐNG]: Cây B-Tree đã tự động phân tầng. Sẵn sàng nhận lệnh!")
    
    app.mainloop()