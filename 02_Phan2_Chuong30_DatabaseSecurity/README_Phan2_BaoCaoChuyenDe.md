# BÁO CÁO PHẦN 2: NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30 - DATABASE SECURITY (AN TOÀN VÀ BẢO MẬT CƠ SỞ DỮ LIỆU)

---

## 1. GIỚI THIỆU CHƯƠNG VÀ TỔNG QUAN VỀ AN TOÀN CƠ SỞ DỮ LIỆU (MỤC 30.1)

### 1.1. Khái niệm và Mục tiêu của Bảo mật Cơ sở Dữ liệu
Bảo mật cơ sở dữ liệu (Database Security) là tập hợp các chính sách, quy trình công nghệ, cơ chế kiểm soát kỹ thuật và biện pháp quản trị nhằm bảo vệ CSDL khỏi các truy cập trái phép, sự sửa đổi ngoài ý muốn, sự phá hoại hoặc rò rỉ dữ liệu nhạy cảm.

Mục tiêu cốt lõi của an toàn CSDL xoay quanh **Tam giác bảo mật CIA (CIA Triad)**:
1. **Tính bảo mật (Confidentiality)**: Đảm bảo dữ liệu chỉ được truy cập bởi những chủ thể (người dùng, ứng dụng, tiến trình) có thẩm quyền hợp pháp. Ngăn chặn việc lộ lọt dữ liệu nội bộ ra bên ngoài hoặc giữa các phòng ban.
2. **Tính toàn vẹn (Integrity)**: Đảm bảo tính chính xác, nhất quán và đáng tin cậy của dữ liệu trong suốt vòng đời lưu trữ và xử lý. Dữ liệu không bị thay đổi, xóa bỏ hoặc làm sai lệch bởi các thao tác trái phép hoặc sự cố hệ thống.
3. **Tính sẵn sàng (Availability)**: Đảm bảo dữ liệu và các dịch vụ CSDL luôn sẵn sàng phục vụ người dùng hợp pháp khi có nhu cầu, duy trì khả năng hoạt động liên tục trước các cuộc tấn công từ chối dịch vụ (DoS/DDoS) hoặc thảm họa phần cứng.

### 1.2. Các cấp độ bảo mật trong Hệ thống CSDL
- **Mức độ Pháp lý và Đạo đức (Legal and Ethical Issues)**: Tuân thủ các quy định pháp luật về bảo vệ dữ liệu cá nhân (ví dụ: Nghị định 13/2023/NĐ-CP tại Việt Nam, GDPR tại Châu Âu, HIPAA trong y tế).
- **Mức độ Chính sách tổ chức (Policy Issues)**: Quy định cấp công ty về quyền truy cập tài nguyên thông tin, quy trình cấp phát và thu hồi tài khoản.
- **Mức độ Hệ thống & Mạng (System and Network Level)**: Bảo vệ hệ điều hành máy chủ, tường lửa mạng (Firewall), cô lập mạng CSDL (Database DMZ / Private Subnet).
- **Mức độ Hệ quản trị CSDL (DBMS Level)**: Các cơ chế nội tại do chính RDBMS cung cấp: xác thực người dùng (Authentication), phân quyền (Authorization), mã hóa lưu trữ (TDE), và kiểm toán (Audit Trail).

### 1.3. Vai trò của Quản trị viên CSDL (DBA) và Cơ chế Kiểm toán (Audit Trail)
- **Tài khoản đặc quyền (Privileged Account - Superuser/sa/SYSDBA)**: DBA nắm giữ quyền tối cao trên CSDL (tạo cấu trúc, quản lý không gian đĩa, cấp quyền). Việc lạm dụng tài khoản DBA hoặc bị chiếm đoạt tài khoản này sẽ gây hậu quả khôn lường. Nguyên tắc bảo mật hiện đại yêu cầu phân tách quyền hạn (Separation of Duties).
- **Kiểm toán CSDL (Database Auditing)**: Ghi lại toàn bộ nhật ký các thao tác đăng nhập, truy vấn dữ liệu nhạy cảm, thay đổi quyền hạn hoặc cấu trúc CSDL vào nhật ký kiểm toán (Audit Log) không thể chỉnh sửa, giúp phát hiện sớm các hành vi bất thường và phục vụ công tác điều tra số (Forensics).

---

## 2. KIỂM SOÁT TRUY CẬP TÙY BIẾN (DISCRETIONARY ACCESS CONTROL - DAC) (MỤC 30.2)

### 2.1. Bản chất của mô hình DAC
Mô hình DAC (Discretionary Access Control) dựa trên khái niệm **quyền sở hữu (Ownership)** và **đặc quyền (Privileges)**:
- Người tạo ra đối tượng CSDL (bảng, khung nhìn, thủ tục) chính là chủ sở hữu (Owner) của đối tượng đó.
- Chủ sở hữu có toàn quyền trên đối tượng và có quyền tùy ý cấp quyền (GRANT) hoặc thu hồi quyền (REVOKE) truy cập đối tượng đó cho các tài khoản khác trong hệ thống.

### 2.2. Hai cấp độ đặc quyền trong RDBMS
1. **Đặc quyền cấp tài khoản (Account Level Privileges)**:
   - Cho phép người dùng thực hiện các thao tác quản trị hoặc tạo đối tượng mới: `CREATE SCHEMA`, `CREATE TABLE`, `CREATE VIEW`, `ALTER`, `DROP`.
2. **Đặc quyền cấp quan hệ/đối tượng (Relation/Object Level Privileges)**:
   - Áp dụng trên từng bảng hoặc khung nhìn cụ thể: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REFERENCES`.
   - Có thể chỉ định quyền `UPDATE` hoặc `SELECT` trên từng cột cụ thể (Column-level privileges).

### 2.3. Cú pháp SQL Chuẩn cho DAC: GRANT và REVOKE
- Cấp quyền truy cập:
  ```sql
  GRANT SELECT, INSERT ON SAN_PHAM TO NhanVienBanHang;
  GRANT UPDATE (GiaBan, SoLuongTon) ON SAN_PHAM TO QuanLyKho;
  ```
- Cấp quyền kèm khả năng ủy quyền tiếp (`WITH GRANT OPTION`):
  ```sql
  GRANT SELECT ON DON_HANG TO TruongPhong WITH GRANT OPTION;
  ```
- Thu hồi quyền:
  ```sql
  REVOKE INSERT ON SAN_PHAM FROM NhanVienBanHang;
  ```
- Khi thu hồi một quyền đã được cấp `WITH GRANT OPTION`, hệ thống hỗ trợ 2 tùy chọn:
  - `CASCADE`: Thu hồi đệ quy quyền từ người dùng này và tất cả những người dùng khác được người dùng này cấp quyền (Propagation Tree).
  - `RESTRICT`: Báo lỗi và hủy lệnh thu hồi nếu quyền này đã được người đó cấp phát tiếp cho một người khác.

### 2.4. Kiểm soát quyền thông qua Khung nhìn (Views)
Khung nhìn (View) là một cơ chế DAC cực kỳ mạnh mẽ để che giấu dữ liệu nhạy cảm:
- **Ẩn cột (Column Hiding)**: Ẩn cột lương (`LuongCoBan`) hay mã băm mật khẩu (`MatKhauHash`) khỏi nhân viên thông thường.
- **Ẩn hàng (Row Filtering)**: Chỉ cho phép nhân viên bán hàng xem các đơn hàng thuộc chi nhánh của mình thông qua mệnh đề `WHERE ChiNhanh = @UserChiNhanh`.

---

## 3. KIỂM SOÁT TRUY CẬP BẮT BUỘC (MANDATORY ACCESS CONTROL - MAC) VÀ PHÂN QUYỀN DỰA TRÊN VAI TRÒ (RBAC) (MỤC 30.3)

### 3.1. So sánh DAC và MAC
| Tiêu chí | Discretionary Access Control (DAC) | Mandatory Access Control (MAC) |
| :--- | :--- | :--- |
| **Cơ chế quyết định** | Do chủ sở hữu đối tượng tự quyết định | Do chính sách an ninh toàn hệ thống bắt buộc |
| **Tính linh hoạt** | Rất cao, phù hợp môi trường thương mại | Thắt chặt, cứng nhắc, phù hợp quân sự/chính phủ |
| **Nguy cơ rò rỉ** | Cao (dễ bị tấn công Trojan Horse/ủy quyền tùy tiện) | Rất thấp, luồng dữ liệu được kiểm soát tuyệt đối |

### 3.2. Mô hình An ninh Đa cấp Bell-LaPadula (MAC)
Mô hình Bell-LaPadula phân loại cả Chủ thể (Subjects - Users) và Đối tượng (Objects - Tables/Records) theo các cấp độ an ninh (Security Classes):
$$\text{Top Secret (TS)} > \text{Secret (S)} > \text{Confidential (C)} > \text{Unclassified (U)}$$

Mô hình thực thi 2 nguyên lý bất biến:
1. **Thuộc tính Bảo mật Đơn giản (Simple Security Property - "No Read Up")**:
   Một chủ thể ở cấp độ bảo mật $S$ chỉ được phép đọc đối tượng ở cấp độ $O$ nếu cấp độ của chủ thể lớn hơn hoặc bằng cấp độ của đối tượng:
   $$\text{Class}(S) \ge \text{Class}(O)$$
   *(Người dùng không thể đọc thông tin mật hơn cấp thẩm quyền của mình).*
2. **Thuộc tính Sao (Star-Property / $\star$-Property - "No Write Down")**:
   Một chủ thể ở cấp độ bảo mật $S$ chỉ được phép ghi (thêm, sửa) vào đối tượng ở cấp độ $O$ nếu cấp độ của chủ thể nhỏ hơn hoặc bằng cấp độ của đối tượng:
   $$\text{Class}(S) \le \text{Class}(O)$$
   *(Người dùng cấp cao không thể ghi thông tin bí mật xuống đối tượng cấp thấp để ngăn chặn rò rỉ dữ liệu ra bên ngoài).*

### 3.3. Hiện tượng Đa thể hiện (Polyinstantiation)
Trong CSDL quan hệ đa cấp, khi người dùng ở cấp độ thấp chèn một bản ghi có cùng khóa chính với một bản ghi đã tồn tại ở cấp độ bí mật cao, hệ thống không thể báo lỗi vi phạm khóa chính (vì báo lỗi sẽ làm lộ sự tồn tại của dữ liệu mật - Covert Timing/Inference). Thay vào đó, hệ thống sinh ra hai phiên bản của bản ghi ứng với hai cấp độ an ninh khác nhau, gọi là hiện tượng **Đa thể hiện (Polyinstantiation)**.

### 3.4. Mô hình Kiểm soát Truy cập Dựa trên Vai trò (RBAC - Role-Based Access Control)
Mô hình RBAC giải quyết hoàn hảo bài toán quản trị phân quyền trong các doanh nghiệp hiện đại:
- Người dùng không được gán quyền trực tiếp mà được gán vào các **Vai trò (Roles)** phản ánh chức năng công việc (ví dụ: `Admin`, `StoreManager`, `SalesStaff`, `Customer`).
- Quyền hạn (Permissions) được gán cho Vai trò: $\text{Permission} \leftrightarrow \text{Role} \leftrightarrow \text{User}$.
- **Phân cấp vai trò (Role Hierarchy)**: Vai trò quản lý kế thừa toàn bộ quyền của vai trò nhân viên cấp dưới.
- **Phân tách nhiệm vụ (Separation of Duties - SoD)**:
  - *Static SoD*: Một người không thể đồng thời giữ hai vai trò xung đột lợi ích (ví dụ: Người lập phiếu chi không thể là Người duyệt thanh toán).
  - *Dynamic SoD*: Một người có thể giữ hai vai trò nhưng không được kích hoạt cả hai vai trò trong cùng một phiên làm việc.

---

## 4. LỖ HỔNG SQL INJECTION VÀ CÁC BIỆN PHÁP PHÒNG CHỐNG (MỤC 30.4)

### 4.1. Cơ chế phát sinh lỗ hổng SQL Injection
SQL Injection (SQLi) là một trong những lỗ hổng bảo mật web và CSDL nguy hiểm nhất (liên tục đứng trong OWASP Top 10). Lỗ hổng xảy ra khi ứng dụng nhận dữ liệu đầu vào từ người dùng (User Input) và ghép trực tiếp vào chuỗi lệnh SQL mà không thực hiện kiểm tra (Sanitization) hoặc tham số hóa (Parameterization).

Khi đó, kẻ tấn công có thể chèn các ký tự điều khiển cú pháp SQL (dấu nháy đơn `'`, dấu chấm phẩy `;`, dấu comment `--` hoặc `/*`) để làm sai lệch hoàn toàn logic của câu truy vấn gốc.

### 4.2. Các dạng tấn công SQL Injection phổ biến
1. **Tấn công lừa đảo logic / Đồng nhất thức (Tautology / Auth Bypass)**:
   - Truy vấn phía backend:
     ```sql
     SELECT * FROM KHACH_HANG WHERE Email = '$input_email' AND MatKhauHash = '$input_password';
     ```
   - Kẻ tấn công nhập vào ô Email: `' OR '1'='1' --`
   - Câu lệnh thực tế được RDBMS thực thi:
     ```sql
     SELECT * FROM KHACH_HANG WHERE Email = '' OR '1'='1' --' AND MatKhauHash = '...';
     ```
   - Mệnh đề `'1'='1'` luôn đúng, toàn bộ phần kiểm tra mật khẩu bị bỏ qua bằng dấu chú thích `--`. Kẻ tấn công đăng nhập thành công với tư cách tài khoản đầu tiên trong bảng (thường là Admin).
2. **Tấn công ghép lệnh hợp nhất (UNION-Based SQL Injection)**:
   - Kẻ tấn công lợi dụng mệnh đề `UNION SELECT` để trích xuất toàn bộ dữ liệu từ các bảng nhạy cảm khác trong hệ thống (như tài khoản mật khẩu, số thẻ ngân hàng, bảng nhân viên).
3. **Tấn công ghép câu lệnh thực thi (Piggybacked Queries)**:
   - Sử dụng dấu chấm phẩy `;` để thực thi thêm câu lệnh thứ hai nguy hiểm:
     ```sql
     ; DROP TABLE DON_HANG; --
     ```
4. **Tấn công mù (Blind SQL Injection - Boolean & Time-based)**:
   - Khai thác khi ứng dụng không trả về thông báo lỗi chi tiết. Kẻ tấn công đo lường thời gian phản hồi (hàm `WAITFOR DELAY '0:0:5'`) hoặc so sánh phản hồi True/False để đoán từng ký tự mật khẩu.

### 4.3. Giải pháp Phòng chống Toàn diện
1. **Sử dụng Truy vấn Tham số hóa / Prepared Statements (Biện pháp cốt lõi)**:
   - Tách rời hoàn toàn phần mã lệnh SQL và dữ liệu tham số. CSDL biên dịch cú pháp lệnh trước (Pre-compiled), sau đó mới đưa giá trị người dùng vào dưới dạng tham số thuần túy (Literal values). Ký tự `'` được xem là ký tự chuỗi thông thường, không thể thay đổi cấu trúc cây phân tích cú pháp (Parse Tree).
2. **Sử dụng Thư viện ORM (Object-Relational Mapping)**: Hibernate, Entity Framework, SQLAlchemy.
3. **Nguyên tắc Đặc quyền Tối thiểu (Principle of Least Privilege)**: Tài khoản kết nối CSDL từ web server không dùng tài khoản `sa` hay `root`, chỉ được cấp quyền `SELECT`, `INSERT`, `UPDATE` trên các bảng cần thiết, cấm quyền DDL (`DROP`, `ALTER`).
4. **Kiểm tra và xác thực dữ liệu đầu vào (Input Validation & Whitelisting)**.
5. **Triển khai Web Application Firewall (WAF)**.

---

## 5. BẢO MẬT CSDL THỐNG KÊ VÀ KIỂM SOÁT LUỒNG THÔNG TIN (MỤC 30.5 & 30.6)

### 5.1. Tấn công suy diễn trong CSDL thống kê (Inference Attacks)
CSDL thống kê cho phép truy vấn các giá trị tổng hợp (SUM, AVG, COUNT, MIN, MAX) trên tập dân số mà không cho phép truy vấn dữ liệu cá nhân đơn lẻ. Tuy nhiên, kẻ tấn công có thể lợi dụng sự kết hợp các điều kiện lọc để suy diễn chính xác dữ liệu của một cá nhân cụ thể.

Ví dụ: Biết trong công ty chỉ có một nữ nhân viên 55 tuổi thuộc phòng Marketing, kẻ tấn công chạy truy vấn:
```sql
SELECT AVG(Luong) FROM NHAN_VIEN WHERE GioiTinh = 'Nu' AND Tuoi = 55 AND PhongBan = 'Marketing';
```
Kích thước tập mẫu trả về là 1, kẻ tấn công biết ngay mức lương của người đó.

**Biện pháp ngăn chặn**:
- **Giới hạn kích thước truy vấn (Query-set size control)**: Chỉ cho phép kết quả trả về nếu số lượng bản ghi thỏa mãn nằm trong khoảng an toàn $k \le |Q| \le N - k$.
- **Nhiễu dữ liệu (Perturbation / Differential Privacy)**: Thêm nhiễu ngẫu nhiên vào dữ liệu hoặc kết quả trả về để bảo vệ quyền riêng tư mà vẫn giữ độ chính xác thống kê vĩ mô.

### 5.2. Kiểm soát luồng thông tin và Kênh bí mật (Covert Channels)
- **Kiểm soát luồng (Flow Control)**: Ngăn chặn thông tin truyền từ đối tượng có mức an ninh cao xuống đối tượng có mức an ninh thấp.
- **Kênh bí mật (Covert Channel)**: Con đường truyền tin gián tiếp vi phạm chính sách an ninh hệ thống:
  - *Covert Storage Channel*: Dùng cờ tài nguyên, dung lượng đĩa hoặc sự tồn tại của khóa để truyền tín hiệu nhị phân 0/1.
  - *Covert Timing Channel*: Đo đạc độ trễ xử lý (CPU contention/clock cycle) để giải mã dữ liệu mật.

---

## 6. MÃ HÓA CSDL VÀ HẠ TẦNG KHÓA CÔNG KHAI (MỤC 30.7)

### 6.1. Thuật toán mã hóa đối xứng (Symmetric Encryption)
- Sử dụng cùng một khóa bí mật (Secret Key) cho cả quá trình mã hóa và giải mã.
- Chuẩn hiện đại: **AES (Advanced Encryption Standard)** với độ dài khóa 128, 192, 256 bits (thay thế chuẩn cũ DES/3DES đã lỗi thời). Tốc độ xử lý cực nhanh, phù hợp mã hóa khối lượng lớn dữ liệu lưu trữ.

### 6.2. Thuật toán mã hóa bất đối xứng (Asymmetric / Public Key Encryption)
- Sử dụng một cặp khóa: Khóa công khai (Public Key - dùng để mã hóa) và Khóa bí mật (Private Key - dùng để giải mã).
- Thuật toán tiêu biểu: **RSA (Rivest-Shamir-Adleman)**, Đường cong Elip (ECC).
- Ứng dụng: Thiết lập kênh truyền an toàn qua SSL/TLS, Chữ ký số (Digital Signatures), Chứng chỉ số X.509 (Digital Certificates) xác thực danh tính máy chủ CSDL.

### 6.3. Băm mật khẩu một chiều (One-Way Hashing) và Chuỗi ngẫu nhiên (Salt)
- Mật khẩu người dùng tuyệt đối không bao giờ được lưu trữ dưới dạng bản rõ (Plaintext) hoặc mã hóa có thể giải mã được.
- Sử dụng hàm băm mật mã học một chiều: SHA-256, SHA-512, hoặc các hàm băm chuyên dụng chống bẻ khóa GPU như Bcrypt, Argon2, PBKDF2.
- **Vai trò của Salt**: Chuỗi ngẫu nhiên được thêm vào mật khẩu trước khi băm, giúp vô hiệu hóa hoàn toàn các cuộc tấn công tra cứu bảng tính trước (Rainbow Table Attack) và đảm bảo hai người dùng có cùng mật khẩu vẫn có giá trị băm hoàn toàn khác nhau.

### 6.4. Các cấp độ mã hóa trong RDBMS
1. **Mã hóa truyền tải (In-Transit Encryption)**: SSL/TLS mã hóa đường truyền mạng giữa ứng dụng và SQL Server, chống nghe lén (Sniffing) và tấn công trung gian (Man-in-the-Middle).
2. **Mã hóa dữ liệu tĩnh (At-Rest Encryption / TDE - Transparent Data Encryption)**: Mã hóa toàn bộ tệp dữ liệu `.mdf` và tệp log `.ldf` trên ổ đĩa vật lý, bảo vệ CSDL khi ổ cứng hoặc file backup bị đánh cắp.
3. **Mã hóa mức cột (Column-Level / Always Encrypted)**: Dữ liệu được mã hóa ngay tại ứng dụng client trước khi gửi lên máy chủ CSDL; quản trị viên CSDL (DBA) cũng không thể đọc được nội dung bản rõ.

---

## 7. BẢO VỆ QUYỀN RIÊNG TƯ VÀ CÁC THÁCH THỨC AN NINH HIỆN ĐẠI (MỤC 30.8 - 30.10)

### 7.1. Các kỹ thuật ẩn danh hóa dữ liệu (Anonymization)
- **$k$-Anonymity**: Đảm bảo mỗi bản ghi không thể phân biệt được với ít nhất $k - 1$ cá nhân khác đối với tập thuộc tính định danh bán phần (Quasi-identifiers: Tuổi, Giới tính, Mã bưu điện).
- **$l$-Diversity**: Đảm bảo trong mỗi nhóm đồng nhất theo $k$-anonymity, thuộc tính nhạy cảm (như Tên bệnh tật, Mức thu nhập) phải có ít nhất $l$ giá trị khác nhau để chống tấn công suy luận tính chất tương đồng.
- **$t$-Closeness**: Yêu cầu phân phối xác suất của thuộc tính nhạy cảm trong nhóm tương đồng không được chênh lệch quá ngưỡng khoảng cách $t$ so với phân phối chung toàn bộ CSDL.

### 7.2. Bảo mật mức hàng (Row-Level Security - RLS) và Oracle Label Security
- RDBMS hiện đại (như MS SQL Server và Oracle VPD - Virtual Private Database) cho phép gán trực tiếp chính sách bảo mật (Security Predicate Function) vào bảng. Khi người dùng thực thi bất kỳ câu lệnh `SELECT`, hệ thống tự động chèn thêm điều kiện lọc ngầm định, đảm bảo người dùng chỉ xem được các dòng dữ liệu mà họ có quyền xem mà không cần phải thay đổi mã nguồn ứng dụng.

---

## 8. KẾT LUẬN CHUYÊN ĐỀ CHƯƠNG 30

Nghiên cứu Chương 30 khẳng định an toàn CSDL không đơn thuần là cài đặt một phần mềm diệt virus hay đặt mật khẩu phức tạp, mà là một **kiến trúc phòng thủ theo chiều sâu (Defense-in-Depth)** bao gồm:
1. Kiểm soát quyền truy cập chặt chẽ (kết hợp linh hoạt DAC và RBAC).
2. Lập trình ứng dụng an toàn (sử dụng 100% Prepared Statements triệt tiêu SQL Injection).
3. Bảo vệ dữ liệu nhạy cảm (Mã hóa đường truyền TLS, mã hóa lưu trữ TDE, băm mật khẩu với Salt).
4. Phân tách nhiệm vụ và duy trì cơ chế kiểm toán (Audit Trail) liên tục.

