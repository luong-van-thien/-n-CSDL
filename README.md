# 🛡️ ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU (DATABASE SYSTEMS)

> **HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG (PTIT - CƠ SỞ TP. HỒ CHÍ MINH)**  
> **Khoa Công Nghệ Thông Tin | Bộ môn Hệ Thống Thông Tin**  
> **Giảng viên hướng dẫn:** ThS. Tuyết Hải  
> **Học kỳ:** HK1 (2025 - 2026) | **Hạn nộp:** 30/11/2026  

---

## 📌 GIỚI THIỆU TỔNG QUAN

Dự án đồ án môn học Cơ sở dữ liệu bao gồm hai phần nội dung chính theo yêu cầu của Giảng viên:
1. **Phần 1: Thiết kế và Cài đặt CSDL Thực tế**: Đề tài **"Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore"** (E-Commerce & Supply Chain System).
   - Thiết kế mô hình Thực thể - Liên kết (ERD 10 thực thể).
   - Ánh xạ chuẩn tắc 7 bước sang Mô hình quan hệ.
   - Phân tích phụ thuộc hàm và **chứng minh đạt chuẩn BCNF (Boyce-Codd Normal Form)**.
   - Cài đặt toàn diện trên **Microsoft SQL Server 2022** với các ràng buộc toàn vẹn, dữ liệu mẫu phong phú và bộ sưu tập hơn **25+ câu truy vấn DQL, View, Procedure, Trigger và Transaction**.
2. **Phần 2: Nghiên cứu Chuyên sâu Chương 30 - Database Security (An toàn và Bảo mật CSDL)** trong giáo trình quốc tế *"Fundamentals of Database Systems"* (7th Edition, Ramez Elmasri & Shamkant B. Navathe).
   - Nghiên cứu Tam giác bảo mật CIA, DAC (GRANT/REVOKE), MAC (Mô hình Bell-LaPadula), RBAC (Phân quyền theo vai trò).
   - Lỗ hổng SQL Injection (Cơ chế, các dạng tấn công Auth Bypass, UNION leak và phòng thủ bằng Prepared Statements).
   - Mã hóa CSDL (Symmetric AES, Asymmetric RSA, Băm mật khẩu SHA-256 + Salt, Transparent Data Encryption - TDE).
   - Kỹ thuật Row-Level Security (RLS) và Dynamic Data Masking (DDM).
3. **Phần 3: Ứng dụng Demo Thực nghiệm (TechStore Cyber Security Lab)**:
   - Ứng dụng Web tương tác trực quan viết bằng **Python Flask + HTML5/CSS3/JavaScript**, giao diện Dark Theme phong cách An ninh mạng.
   - Cho phép người dùng và giảng viên trực tiếp thử nghiệm payload tấn công SQL Injection và đối chiếu với cơ chế an toàn Parameterized Query; trực quan hóa Ma trận phân quyền RBAC; kiểm chứng tốc độ bẻ khóa MD5 bằng Rainbow Table so với SHA-256 + Salt; kèm kịch bản T-SQL chạy trực tiếp trên SQL Server.

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```text
do an co so du lieu/
├── 01_Phan1_ThietKeCSDL/               # PHẦN 1: THIẾT KẾ & CÀI ĐẶT CSDL
│   ├── 01_DDL_Create_TechStoreDB.sql  # Script tạo Database, bảng, PK, FK, CHECK, UNIQUE
│   ├── 02_DML_Insert_SampleData.sql   # Dữ liệu mẫu hoàn chỉnh cho 10 bảng
│   ├── 03_DQL_Advanced_Queries.sql    # 25+ câu truy vấn nâng cao, View, Procedure, Trigger
│   ├── ERD_TechStore.png              # Sơ đồ Thực thể - Liên kết (ERD) chất lượng 300 DPI
│   ├── Relational_Schema_TechStore.png# Lược đồ quan hệ chuẩn BCNF (300 DPI)
│   ├── generate_erd_diagram.py        # Code Python tự động vẽ ERD
│   ├── generate_relational_schema.py  # Code Python tự động vẽ Schema
│   └── README_Phan1.md                # Tài liệu phân tích nghiệp vụ & chứng minh BCNF
│
├── 02_Phan2_Chuong30_DatabaseSecurity/# PHẦN 2: CHUYÊN ĐỀ CHƯƠNG 30 DATABASE SECURITY
│   └── README_Phan2_BaoCaoChuyenDe.md # Báo cáo chuyên sâu lý thuyết Chương 30 (Elmasri 7E)
│
├── 03_Demo_Security_App/              # PHẦN 3: ỨNG DỤNG WEB DEMO AN NINH CSDL
│   ├── app.py                         # Backend máy chủ Flask
│   ├── techstore_demo.db              # Database SQLite mô phỏng cấu trúc TechStoreDB
│   ├── run_demo.bat                   # File khởi chạy nhanh 1-click trên Windows
│   ├── SQLServer_Security_Scripts.sql # Script T-SQL cài đặt DAC, RBAC, RLS, DDM trên SQL Server
│   ├── templates/
│   │   └── index.html                 # Giao diện Web Cyber Security Lab
│   └── static/
│       ├── style.css                  # Giao diện Dark Theme hiện đại
│       └── script.js                  # Xử lý tương tác AJAX, payload demo
│
├── 04_BaoCao_Report/                  # CUỐN BÁO CÁO HOÀN CHỈNH (MẪU PTIT)
│   ├── Bao_Cao_Do_An_Mon_Hoc_CSDL.docx# File báo cáo Word hoàn chỉnh (Chuẩn mẫu nhà trường)
│   ├── Bao_Cao_Do_An_Mon_Hoc_CSDL.pdf # File PDF 22 trang sẵn sàng nộp bài
│   └── build_full_report.py           # Script tự động biên soạn báo cáo và convert PDF
│
├── 05_Slide_Presentation/            # BỘ SLIDE THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN
│   ├── Slide_Thuyet_Trinh_Do_An_CSDL.pptx# File PowerPoint 13 slide thiết kế hiện đại 16:9
│   ├── Slide_Thuyet_Trinh_Do_An_CSDL.pdf # File PDF trình chiếu phụ trợ
│   └── build_presentation.py          # Script Python tự động sinh Slides
│
├── .gitignore                         # Tệp cấu hình loại trừ file tạm của Git
└── README.md                          # Tài liệu hướng dẫn tổng quan dự án
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ TRẢI NGHIỆM

### 1. Cài đặt CSDL trên Microsoft SQL Server
1. Mở **SQL Server Management Studio (SSMS)** và kết nối tới SQL Server Instance cục bộ.
2. Mở và thực thi tệp `01_Phan1_ThietKeCSDL/01_DDL_Create_TechStoreDB.sql` để tạo Database `TechStoreDB` cùng 10 bảng và các ràng buộc toàn vẹn.
3. Mở và thực thi tệp `01_Phan1_ThietKeCSDL/02_DML_Insert_SampleData.sql` để chèn dữ liệu mẫu.
4. Mở tệp `01_Phan1_ThietKeCSDL/03_DQL_Advanced_Queries.sql` để kiểm thử các câu truy vấn SELECT, View, Stored Procedure và Trigger.

### 2. Khởi chạy Ứng dụng Web Demo Cyber Security Lab
1. Mở thư mục `03_Demo_Security_App`.
2. **Cách 1 (Khuyên dùng):** Nhấp đúp chuột vào tệp `run_demo.bat`. Hệ thống sẽ tự động khởi động server và mở trình duyệt tại `http://127.0.0.1:5000`.
3. **Cách 2:** Mở PowerShell / Command Prompt tại thư mục `03_Demo_Security_App` và chạy:
   ```bash
   pip install flask
   python app.py
   ```
4. Truy cập trình duyệt tại địa chỉ: **`http://127.0.0.1:5000`**

### 3. Các kịch bản kiểm thử nổi bật trong Web Demo:
- **Tab 1 - SQL Injection Lab**:
  - Nhấp vào nút **`admin' --`** ở chế độ Lỗ hổng và nhấn *Thực thi Đăng nhập* -> Đăng nhập thành công với tư cách Admin không cần mật khẩu!
  - Chuyển sang chế độ **An toàn (Prepared Statement)** và thử lại -> Tấn công bị chặn đứng hoàn toàn!
  - Tại ô tìm kiếm sản phẩm, nhấp nút **`Lộ Bảng USERS & Lương`** -> Trích xuất toàn bộ mật khẩu và lương nhân sự bằng kỹ thuật UNION.
- **Tab 2 - Phân Quyền RBAC**: Chọn các vai trò (ADMIN, MANAGER, STAFF, CUSTOMER) và kiểm thử quyền thực thi các hành vi nhạy cảm.
- **Tab 3 - Băm Mật Khẩu**: Nhập mật khẩu để kiểm tra tốc độ bẻ khóa MD5 bằng Rainbow Table so với tính an toàn tuyệt đối của SHA-256 + Salt.
- **Tab 4 - Kịch bản T-SQL**: Tham khảo và sao chép các lệnh T-SQL triển khai Row-Level Security (RLS) và Dynamic Data Masking (DDM) trên SQL Server thật.

---

## 👥 THÀNH VIÊN NHÓM VÀ PHÂN CÔNG ĐÓNG GÓP

| STT | Họ và Tên | Mã số sinh viên | Vai trò & Nhiệm vụ phân công | Tỷ lệ đóng góp |
| :---: | :--- | :---: | :--- | :---: |
| 1 | **Nguyễn Thành Thiện** (Đại diện) | **N24DCCN076** | **Trưởng nhóm**: Khảo sát nghiệp vụ, thiết kế ERD, Schema, chuẩn hóa BCNF, lập trình DDL/DML, tổng hợp báo cáo. | **34%** |
| 2 | **Thành viên nhóm 02** | MSSV 02 | **Thành viên**: Nghiên cứu lý thuyết Chương 30 (DAC, MAC, RBAC, SQLi, Encryption), soạn thảo Slide thuyết trình. | **33%** |
| 3 | **Thành viên nhóm 03** | MSSV 03 | **Thành viên**: Phát triển ứng dụng Web Demo Flask, kịch bản T-SQL bảo mật trên SQL Server, quản trị kho GitHub. | **33%** |

---

## 📚 TÀI LIỆU THAM KHẢO

1. **Ramez Elmasri & Shamkant B. Navathe (2016)**, *Fundamentals of Database Systems*, 7th Edition, Pearson. (Đặc biệt là Chapter 30: Database Security, tr. 1121 - 1162).
2. **ThS. Tuyết Hải (2022)**, *Bài giảng môn học Cơ sở dữ liệu*, Học viện Công nghệ Bưu chính Viễn thông - Cơ sở TP. Hồ Chí Minh.
3. **Microsoft Learn (2024)**, *SQL Server Security: Row-Level Security, Dynamic Data Masking, TDE*.
4. **OWASP Foundation (2023)**, *SQL Injection Prevention Cheat Sheet*.
