# BÁO CÁO PHẦN 1: THIẾT KẾ VÀ CÀI ĐẶT CƠ SỞ DỮ LIỆU TECHSTORE

---

## 1. TỔNG QUAN VÀ KHẢO SÁT NGHIỆP VỤ HỆ THỐNG TECHSTORE

### 1.1. Bối cảnh và Mục tiêu đề tài
Trong kỷ nguyên chuyển đổi số và thương mại điện tử phát triển bùng nổ, việc xây dựng một hệ thống cơ sở dữ liệu (CSDL) vững chắc, có khả năng mở rộng, đảm bảo tính toàn vẹn và an toàn dữ liệu là yếu tố sống còn của doanh nghiệp. Đề tài **"Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore"** hướng tới giải quyết bài toán quản lý chuỗi cung ứng thiết bị công nghệ, bao gồm:
- Quản lý danh mục hàng hóa, nhà cung cấp, và kiểm soát tồn kho theo thời gian thực.
- Quản lý thông tin khách hàng, lịch sử giao dịch và tự động phân loại hạng thành viên (Loyalty program).
- Quy trình xử lý đơn hàng đa kênh (đặt hàng trực tuyến, xử lý đơn, xuất hóa đơn tài chính).
- Quản lý cơ cấu nhân sự, phân cấp quản lý đệ quy và phân quyền vai trò (Role-Based Access Control).
- Hệ thống đánh giá, phản hồi chất lượng sản phẩm từ khách hàng thực tế.

### 1.2. Mô tả quy tắc nghiệp vụ (Business Rules)
1. **Danh mục & Nhà cung cấp**: Một danh mục sản phẩm (Category) có thể chứa nhiều sản phẩm khác nhau; mỗi sản phẩm bắt buộc thuộc về một danh mục duy nhất. Một nhà cung cấp (Supplier) có thể cung ứng nhiều sản phẩm; mỗi sản phẩm do một nhà cung cấp chính phân phối.
2. **Sản phẩm & Giá bán**: Mỗi sản phẩm có mã định danh duy nhất (`MaSP`), giá nhập và giá bán. Quy tắc nghiệp vụ bắt buộc: `GiaBan >= GiaNhap` và `SoLuongTon >= 0`.
3. **Khách hàng & Tài khoản**: Khách hàng đăng ký tài khoản với Email và Số điện thoại duy nhất. Mật khẩu không lưu dạng bản rõ (plaintext) mà được băm bằng thuật toán SHA-256 kèm chuỗi Salt ngẫu nhiên nhằm bảo vệ an toàn thông tin theo chuẩn OWASP.
4. **Đơn hàng & Chi tiết**: Một khách hàng có thể đặt nhiều đơn hàng (`1 - N`). Mỗi đơn hàng bao gồm một hoặc nhiều sản phẩm (`N - N`), được ánh xạ qua bảng trung gian `CHI_TIET_DON_HANG`. Số lượng đặt phải `> 0`, chiết khấu trong khoảng từ `0%` đến `100%`.
5. **Hóa đơn tài chính**: Sau khi đơn hàng được thanh toán, hệ thống xuất một hóa đơn duy nhất tương ứng với đơn hàng đó (`1 - 1`). Hóa đơn ghi nhận mã giao dịch ngân hàng/cổng thanh toán để đối soát tài chính.
6. **Nhân viên & Quản lý**: Mỗi nhân viên có một vai trò cụ thể (`VAI_TRO`). Nhân viên có thể có một người quản lý trực tiếp (`MaQuanLy`) - mối kết hợp đệ quy (Recursive relationship) phản ánh cấu trúc cây tổ chức của công ty.

---

## 2. MÔ HÌNH THỰC THỂ - LIÊN KẾT (ERD)

### 2.1. Danh sách các Thực thể (Entities) và Thuộc tính
1. **DANH_MUC** (**<u>MaDanhMuc</u>**, TenDanhMuc, MoTa, TrangThai)
2. **NHA_CUNG_CAP** (**<u>MaNCC</u>**, TenNCC, NguoiLienHe, SoDienThoai, Email, DiaChi, TrangThaiHoptac)
3. **SAN_PHAM** (**<u>MaSP</u>**, TenSP, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai)
4. **KHACH_HANG** (**<u>MaKH</u>**, HoTen, Email, SoDienThoai, DiaChi, NgayDangKy, MatKhauHash, Salt, TongChiTieu, HangThanhVien, TrangThaiTaiKhoan)
5. **VAI_TRO** (**<u>MaVaiTro</u>**, TenVaiTro, MoTa, CapDoTruyCap)
6. **NHAN_VIEN** (**<u>MaNV</u>**, HoTen, Email, SoDienThoai, ChucVu, LuongCoBan, NgayVaoLam, MatKhauHash, Salt, TrangThai)
7. **DON_HANG** (**<u>MaDonHang</u>**, NgayDat, TongTien, PhuongThucThanhToan, TrangThaiDonHang, DiaChiGiaoHang, GhiChu)
8. **HOA_DON** (**<u>MaHoaDon</u>**, NgayLap, SoTienThanhToan, HinhThucThanhToan, TrangThaiThanhToan, MaGiaoDichNganHang)
9. **DANH_GIA_SAN_PHAM** (**<u>MaDanhGia</u>**, DiemDanhGia, BinhLuan, NgayDanhGia)

### 2.2. Danh sách Mối kết hợp (Relationships)
- **Phân loại** (DANH_MUC - SAN_PHAM): Quan hệ $1 - N$. Một danh mục có nhiều sản phẩm.
- **Cung cấp** (NHA_CUNG_CAP - SAN_PHAM): Quan hệ $1 - N$. Một nhà cung cấp cấp nhiều sản phẩm.
- **Phân quyền** (VAI_TRO - NHAN_VIEN): Quan hệ $1 - N$. Một vai trò gán cho nhiều nhân viên.
- **Quản lý** (NHAN_VIEN - NHAN_VIEN): Quan hệ $1 - N$ đệ quy. Một nhân viên cấp cao quản lý nhiều nhân viên cấp dưới.
- **Đặt mua** (KHACH_HANG - DON_HANG): Quan hệ $1 - N$. Một khách hàng tạo nhiều đơn hàng.
- **Xử lý** (NHAN_VIEN - DON_HANG): Quan hệ $1 - N$. Một nhân viên xử lý nhiều đơn hàng.
- **Bao gồm** (DON_HANG - SAN_PHAM): Quan hệ $N - N$, có thuộc tính kết hợp: `SoLuong`, `DonGia`, `ChietKhau`, `ThanhTien`.
- **Thanh toán** (DON_HANG - HOA_DON): Quan hệ $1 - 1$. Một đơn hàng gắn với tối đa một hóa đơn thanh toán.
- **Đánh giá** (KHACH_HANG - SAN_PHAM): Quan hệ $N - N$, tạo thực thể kết hợp `DANH_GIA_SAN_PHAM` có thuộc tính `DiemDanhGia`, `BinhLuan`, `NgayDanhGia`.

*(Sơ đồ ERD chi tiết xem tại file `ERD_TechStore.png`)*

---

## 3. CHUYỂN ĐỔI ERD SANG MÔ HÌNH QUAN HỆ (RELATIONAL MAPPING)

Tuân thủ thuật toán ánh xạ 7 bước từ ER sang Mô hình Quan hệ (theo Giáo trình Elmasri & Navathe - Chapter 9):

1. **Bước 1 (Ánh xạ các thực thể thông thường - Regular Entity Types)**:
   - `DANH_MUC`(**<u>MaDanhMuc</u>**, TenDanhMuc, MoTa, TrangThai)
   - `NHA_CUNG_CAP`(**<u>MaNCC</u>**, TenNCC, NguoiLienHe, SoDienThoai, Email, DiaChi, TrangThaiHoptac)
   - `KHACH_HANG`(**<u>MaKH</u>**, HoTen, Email, SoDienThoai, DiaChi, NgayDangKy, MatKhauHash, Salt, TongChiTieu, HangThanhVien, TrangThaiTaiKhoan)
   - `VAI_TRO`(**<u>MaVaiTro</u>**, TenVaiTro, MoTa, CapDoTruyCap)

2. **Bước 2 (Ánh xạ các mối kết hợp $1 - N$ nhị phân)**:
   - `SAN_PHAM`(**<u>MaSP</u>**, TenSP, *MaDanhMuc*, *MaNCC*, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai)  
     *(Khóa ngoại `MaDanhMuc` tham chiếu `DANH_MUC(MaDanhMuc)`, `MaNCC` tham chiếu `NHA_CUNG_CAP(MaNCC)`)*
   - `NHAN_VIEN`(**<u>MaNV</u>**, HoTen, Email, SoDienThoai, ChucVu, LuongCoBan, NgayVaoLam, *MaVaiTro*, *MaQuanLy*, MatKhauHash, Salt, TrangThai)  
     *(Khóa ngoại `MaVaiTro` tham chiếu `VAI_TRO(MaVaiTro)`, `MaQuanLy` tham chiếu `NHAN_VIEN(MaNV)`)*
   - `DON_HANG`(**<u>MaDonHang</u>**, *MaKH*, *MaNV*, NgayDat, TongTien, PhuongThucThanhToan, TrangThaiDonHang, DiaChiGiaoHang, GhiChu)  
     *(Khóa ngoại `MaKH` tham chiếu `KHACH_HANG(MaKH)`, `MaNV` tham chiếu `NHAN_VIEN(MaNV)`)*

3. **Bước 3 (Ánh xạ mối kết hợp $1 - 1$ nhị phân)**:
   - `HOA_DON`(**<u>MaHoaDon</u>**, *MaDonHang*, NgayLap, SoTienThanhToan, HinhThucThanhToan, TrangThaiThanhToan, MaGiaoDichNganHang)  
     *(Khóa ngoại `MaDonHang` tham chiếu `DON_HANG(MaDonHang)` với ràng buộc `UNIQUE`)*

4. **Bước 4 (Ánh xạ mối kết hợp $M - N$ nhị phân)**:
   - `CHI_TIET_DON_HANG`(**<u>*MaDonHang*</u>**, **<u>*MaSP*</u>**, SoLuong, DonGia, ChietKhau, ThanhTien)  
     *(Khóa chính phức hợp gồm `MaDonHang` tham chiếu `DON_HANG(MaDonHang)` và `MaSP` tham chiếu `SAN_PHAM(MaSP)`)*
   - `DANH_GIA_SAN_PHAM`(**<u>MaDanhGia</u>**, *MaSP*, *MaKH*, DiemDanhGia, BinhLuan, NgayDanhGia)

*(Sơ đồ Lược đồ Quan hệ xem tại file `Relational_Schema_TechStore.png`)*

---

## 4. CHUẨN HÓA MÔ HÌNH QUAN HỆ (NORMALIZATION ANALYSIS)

### 4.1. Khái niệm và Quy chuẩn Chuẩn hóa
Chuẩn hóa dữ liệu là quá trình phân rã các lược đồ quan hệ nhằm loại bỏ các bất thường (Anomalies):
- Bất thường thêm (Insertion Anomaly)
- Bất thường xóa (Deletion Anomaly)
- Bất thường sửa (Update Anomaly)
- Dư thừa dữ liệu (Data Redundancy)

### 4.2. Phân tích chi tiết từng Lược đồ Quan hệ

#### a) Quan hệ `SAN_PHAM`
- **Tập thuộc tính**: $R = \{\text{MaSP, TenSP, MaDanhMuc, MaNCC, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai}\}$
- **Tập phụ thuộc hàm $F$**:
  - $f_1: \text{MaSP} \rightarrow \text{TenSP, MaDanhMuc, MaNCC, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai}$
- **Khóa ứng viên (Candidate Key)**: Khóa duy nhất là $\{\text{MaSP}\}$ vì $\{\text{MaSP}\}^+ = R$.
- **Kiểm tra chuẩn**:
  - **1NF**: Tất cả các thuộc tính đều là giá trị nguyên tố (Atomic values), không chứa nhóm lặp hay thuộc tính đa trị $\Rightarrow$ Đạt 1NF.
  - **2NF**: Khóa chính là khóa đơn lẻ (1 thuộc tính `MaSP`), do đó không thể tồn tại phụ thuộc hàm bộ phận vào một phần của khóa chính $\Rightarrow$ Đạt 2NF.
  - **3NF**: Không có phụ thuộc bắc cầu từ khóa chính tới bất kỳ thuộc tính không khóa nào $\Rightarrow$ Đạt 3NF.
  - **BCNF**: Với mọi phụ thuộc hàm $X \rightarrow Y \in F$, vế trái $X = \{\text{MaSP}\}$ là một siêu khóa (Superkey) của lược đồ $\Rightarrow$ Đạt chuẩn BCNF (Boyce-Codd Normal Form).

#### b) Quan hệ `CHI_TIET_DON_HANG`
- **Tập thuộc tính**: $R = \{\text{MaDonHang, MaSP, SoLuong, DonGia, ChietKhau, ThanhTien}\}$
- **Tập phụ thuộc hàm $F$**:
  - $f_1: \{\text{MaDonHang, MaSP}\} \rightarrow \{\text{SoLuong, DonGia, ChietKhau}\}$
  - $f_2: \{\text{SoLuong, DonGia, ChietKhau}\} \rightarrow \{\text{ThanhTien}\}$ *(Thuộc tính suy diễn - Computed column)*
- **Khóa ứng viên**: $\{\text{MaDonHang, MaSP}\}$
- **Kiểm tra chuẩn**:
  - **1NF**: Đạt 1NF do mọi miền giá trị đều là nguyên tố.
  - **2NF**: Không có thuộc tính nào phụ thuộc vào riêng lẻ `MaDonHang` hay `MaSP` (Ví dụ: `TenSP` hay `GiaBanGoc` không lưu tại đây mà đã tách sang bảng `SAN_PHAM`; `NgayDat` không lưu tại đây mà ở `DON_HANG`). Do đó, không có phụ thuộc bộ phận $\Rightarrow$ Đạt 2NF.
  - **3NF & BCNF**: `ThanhTien` là cột tính toán tự động (`PERSISTED` trong SQL Server), vế trái $\{\text{MaDonHang, MaSP}\}$ là siêu khóa duy nhất $\Rightarrow$ Đạt chuẩn BCNF.

#### c) Quan hệ `DON_HANG`
- **Tập thuộc tính**: $R = \{\text{MaDonHang, MaKH, MaNV, NgayDat, TongTien, PhuongThucTT, TrangThai, DiaChiGiao, GhiChu}\}$
- **Khóa ứng viên**: $\{\text{MaDonHang}\}$
- **Phụ thuộc hàm $F$**: $\{\text{MaDonHang}\} \rightarrow \text{tất cả thuộc tính còn lại}$.
- **Kết luận**: Mọi vế trái phụ thuộc hàm đều là siêu khóa $\Rightarrow$ Đạt chuẩn BCNF.

#### d) Quan hệ `KHACH_HANG` & `NHAN_VIEN`
- Đạt chuẩn BCNF vì khóa chính lần lượt là `MaKH` và `MaNV`. Thông tin tài khoản, mật khẩu băm, và thuộc tính cá nhân đều phụ thuộc đầy đủ vào khóa chính.

**KẾT LUẬN TỔNG QUAN**: Toàn bộ 10 lược đồ quan hệ trong CSDL TechStore đều đã được thiết kế tối ưu, đạt dạng chuẩn cao nhất là **BCNF**, đảm bảo tính toàn vẹn và hoàn toàn triệt tiêu các nguy cơ dư thừa dữ liệu hay bất thường thao tác.

