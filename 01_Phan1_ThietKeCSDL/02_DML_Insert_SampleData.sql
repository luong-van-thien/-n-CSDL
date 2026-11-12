-- ============================================================================
-- ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU (DATABASE SYSTEMS)
-- PHẦN 1: THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG CƠ SỞ DỮ LIỆU TECHSTORE
-- Đề tài: Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore
-- Hệ Quản Trị CSDL: Microsoft SQL Server 2019 / 2022
-- File: 02_DML_Insert_SampleData.sql
-- Mô tả: Chèn dữ liệu mẫu đa dạng, logic và hoàn chỉnh cho tất cả các bảng.
-- ============================================================================

USE TechStoreDB;
GO

-- Xóa dữ liệu cũ theo thứ tự ngược lại để không vi phạm khóa ngoại
DELETE FROM DANH_GIA_SAN_PHAM;
DELETE FROM HOA_DON;
DELETE FROM CHI_TIET_DON_HANG;
DELETE FROM DON_HANG;
DELETE FROM SAN_PHAM;
DELETE FROM NHAN_VIEN;
DELETE FROM KHACH_HANG;
DELETE FROM NHA_CUNG_CAP;
DELETE FROM DANH_MUC;
DELETE FROM VAI_TRO;
GO

-- ============================================================================
-- 1. CHÈN BẢNG VAI_TRO
-- ============================================================================
INSERT INTO VAI_TRO (MaVaiTro, TenVaiTro, MoTa, CapDoTruyCap) VALUES
('VT_ADMIN',   N'Quản trị hệ thống', N'Toàn quyền quản trị cơ sở dữ liệu và hệ thống', 3),
('VT_QUANLY',  N'Quản lý cửa hàng',  N'Quản lý doanh thu, nhân sự và phê duyệt nhập xuất', 2),
('VT_BANHANG', N'Nhân viên bán hàng',N'Tạo đơn hàng, tra cứu khách hàng và xử lý giao nhận', 1),
('VT_KHO',     N'Nhân viên kho',     N'Quản lý tồn kho, nhập hàng từ nhà cung cấp', 1);
GO

-- ============================================================================
-- 2. CHÈN BẢNG DANH_MUC
-- ============================================================================
INSERT INTO DANH_MUC (MaDanhMuc, TenDanhMuc, MoTa, TrangThai) VALUES
('DM_LAPTOP',  N'Máy tính xách tay',   N'Laptop gaming, văn phòng, đồ họa cao cấp', N'Hoạt động'),
('DM_SMART',   N'Điện thoại thông minh',N'Smartphone iOS, Android chính hãng', N'Hoạt động'),
('DM_TABLET',  N'Máy tính bảng',       N'iPad, Samsung Galaxy Tab, máy tính bảng đồ họa', N'Hoạt động'),
('DM_PHUKIEN', N'Phụ kiện công nghệ',  N'Bàn phím cơ, chuột không dây, cáp sạc, dock sạc', N'Hoạt động'),
('DM_AUDIO',   N'Âm thanh & Tai nghe', N'Tai nghe chống ồn, loa Bluetooth cao cấp', N'Hoạt động'),
('DM_MANHINH', N'Màn hình máy tính',   N'Màn hình 4K, màn hình gaming tần số quét cao', N'Hoạt động');
GO

-- ============================================================================
-- 3. CHÈN BẢNG NHA_CUNG_CAP
-- ============================================================================
INSERT INTO NHA_CUNG_CAP (MaNCC, TenNCC, NguoiLienHe, SoDienThoai, Email, DiaChi, TrangThaiHoptac) VALUES
('NCC_APPLE',   N'Công ty TNHH Apple Việt Nam',         N'Nguyễn Minh Khôi',  '02838221144', 'contact@apple.vn',         N'Tầng 15, Bitexco, Q.1, TP.HCM', N'Đang hợp tác'),
('NCC_ASUS',    N'ASUS Global Pte Ltd - Chi nhánh VN',   N'Trần Hoàng Nam',    '02839100222', 'sales@asus.com.vn',       N'Tòa nhà Viettel, CMT8, Q.10, TP.HCM', N'Đang hợp tác'),
('NCC_DELL',    N'Dell Global B.V Việt Nam',             N'Lê Thu Trang',      '02838245566', 'support@dell.com.vn',     N'Tầng 26, Saigon Trade Center, Q.1, TP.HCM', N'Đang hợp tác'),
('NCC_SAMSUNG', N'Công ty TNHH Điện tử Samsung Vina',    N'Phạm Quốc Tuấn',    '02839157310', 'business@samsung.com.vn', N'Khu Công Nghệ Cao, TP. Thủ Đức, TP.HCM', N'Đang hợp tác'),
('NCC_SONY',    N'Công ty TNHH Sony Electronics VN',     N'Đỗ Hải Đăng',       '02838222228', 'info@sony.com.vn',        N'Tầng 6, President Place, Q.1, TP.HCM', N'Đang hợp tác'),
('NCC_LOGITECH',N'Synnex FPT - Phân phối Logitech',      N'Vũ Đức Thịnh',      '02873006666', 'distrib@synnexfpt.com.vn',N'Tòa nhà FPT, Tân Bình, TP.HCM', N'Đang hợp tác');
GO

-- ============================================================================
-- 4. CHÈN BẢNG KHACH_HANG
-- Mật khẩu đã được mã hóa bằng thuật toán SHA-256 kèm chuỗi Salt bảo mật
-- ============================================================================
INSERT INTO KHACH_HANG (MaKH, HoTen, Email, SoDienThoai, DiaChi, NgayDangKy, MatKhauHash, Salt, TongChiTieu, HangThanhVien, TrangThaiTaiKhoan) VALUES
('KH001', N'Nguyễn Văn An',     'an.nguyen@gmail.com',    '0903123456', N'123 Lê Lợi, Phường Bến Nghé, Quận 1, TP.HCM',     '2024-01-15', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 's@lt_kh001', 52500000.00,  N'Kim cương', N'Kích hoạt'),
('KH002', N'Trần Thị Bích Ngọc', 'bichngoc.tran@yahoo.com', '0918234567', N'45 Hai Bà Trưng, Phường 6, Quận 3, TP.HCM',        '2024-02-10', 'b678c12345422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae4', 's@lt_kh002', 34990000.00,  N'Vàng',      N'Kích hoạt'),
('KH003', N'Lê Hoàng Phúc',     'hoangphuc.le@outlook.com','0987345678', N'88 Nguyễn Trãi, Phường 3, Quận 5, TP.HCM',          '2024-03-05', 'c789d23456422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae5', 's@lt_kh003', 18500000.00,  N'Bạc',       N'Kích hoạt'),
('KH004', N'Phạm Thùy Linh',    'thuylinh.pham@gmail.com', '0934456789', N'220 Hoàng Văn Thụ, Phường 4, Tân Bình, TP.HCM',     '2024-04-12', 'd890e34567422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae6', 's@lt_kh004', 8200000.00,   N'Đồng',      N'Kích hoạt'),
('KH005', N'Hoàng Trọng Nghĩa', 'nghia.hoang@fpt.edu.vn',  '0976567890', N'12 Võ Văn Ngân, Linh Chiểu, TP. Thủ Đức, TP.HCM',    '2024-05-20', 'e901f45678422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae7', 's@lt_kh005', 47200000.00,  N'Vàng',      N'Kích hoạt'),
('KH006', N'Đặng Thanh Mai',    'thanhmai.dang@gmail.com', '0945678901', N'50 Phan Đăng Lưu, Phường 1, Phú Nhuận, TP.HCM',      '2024-06-08', 'f012a56789422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae8', 's@lt_kh006', 2900000.00,   N'Đồng',      N'Kích hoạt'),
('KH007', N'Vũ Quốc Bảo',       'bao.vu@techcorp.vn',      '0923789012', N'78 Nguyễn Thị Minh Khai, Đa Kao, Quận 1, TP.HCM',     '2024-07-01', 'a123b67890422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae9', 's@lt_kh007', 76000000.00,  N'Kim cương', N'Kích hoạt'),
('KH008', N'Bùi Ánh Tuyết',     'anhtuyet.bui@gmail.com',  '0967890123', N'104 Chu Văn An, Phường 26, Bình Thạnh, TP.HCM',      '2024-08-14', 'b234c78901422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27af0', 's@lt_kh008', 12300000.00,  N'Bạc',       N'Kích hoạt'),
('KH009', N'Đỗ Minh Trí',       'tri.dominh@gmail.com',    '0908901234', N'15 An Dương Vương, Phường 8, Quận 5, TP.HCM',        '2024-09-02', 'c345d89012422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27af1', 's@lt_kh009', 0.00,          N'Đồng',      N'Kích hoạt'),
('KH010', N'Ngô Gia Hân',       'giahan.ngo@gmail.com',    '0919012345', N'340 Cộng Hòa, Phường 13, Tân Bình, TP.HCM',          '2024-09-18', 'd456e90123422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27af2', 's@lt_kh010', 0.00,          N'Đồng',      N'Khóa');
GO

-- ============================================================================
-- 5. CHÈN BẢNG NHAN_VIEN (Kèm liên kết quản lý - recursive)
-- ============================================================================
INSERT INTO NHAN_VIEN (MaNV, HoTen, Email, SoDienThoai, ChucVu, LuongCoBan, NgayVaoLam, MaVaiTro, MaQuanLy, MatKhauHash, Salt, TrangThai) VALUES
('NV001', N'Trương Công Định', 'dinh.truong@techstore.vn', '0901000001', N'Tổng Giám Đốc',    35000000.00, '2022-01-01', 'VT_ADMIN',   NULL,    'e10adc3949ba59abbe56e057f20f883e', 's@lt_nv001', N'Đang làm việc'),
('NV002', N'Nguyễn Thúy Hằng', 'hang.nguyen@techstore.vn', '0901000002', N'Quản Lý Cửa Hàng', 22000000.00, '2022-03-15', 'VT_QUANLY',  'NV001', 'c33367701511b4f6020ec61ded352059', 's@lt_nv002', N'Đang làm việc'),
('NV003', N'Trần Minh Quân',   'quan.tran@techstore.vn',   '0901000003', N'Trưởng Bộ Phận Bán Hàng', 18000000.00, '2022-06-01', 'VT_QUANLY',  'NV002', '1bbd886460827015e5d605ed44252251', 's@lt_nv003', N'Đang làm việc'),
('NV004', N'Lê Thị Hương',     'huong.le@techstore.vn',    '0901000004', N'Nhân Viên Bán Hàng', 10500000.00, '2023-01-10', 'VT_BANHANG', 'NV003', '6512bd43d9caa6e02c990b0a82652dca', 's@lt_nv004', N'Đang làm việc'),
('NV005', N'Phạm Gia Khiêm',   'khiem.pham@techstore.vn',  '0901000005', N'Nhân Viên Bán Hàng', 10000000.00, '2023-03-01', 'VT_BANHANG', 'NV003', 'c20ad4d76fe97759aa27a0c99bff6710', 's@lt_nv005', N'Đang làm việc'),
('NV006', N'Đoàn Văn Hậu',     'hau.doan@techstore.vn',    '0901000006', N'Trưởng Kho',        16000000.00, '2022-08-15', 'VT_KHO',     'NV002', 'b59c67bf196a4758191e42f76670ceba', 's@lt_nv006', N'Đang làm việc'),
('NV007', N'Võ Tấn Tài',       'tai.vo@techstore.vn',      '0901000007', N'Nhân Viên Thủ Kho',  9500000.00,  '2023-05-10', 'VT_KHO',     'NV006', 'd6b9f291e0a9693bb474b88b0d2d386d', 's@lt_nv007', N'Đang làm việc');
GO

-- ============================================================================
-- 6. CHÈN BẢNG SAN_PHAM
-- ============================================================================
INSERT INTO SAN_PHAM (MaSP, TenSP, MaDanhMuc, MaNCC, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai) VALUES
('SP_IP15PM', N'iPhone 15 Pro Max 256GB Titan Tự Nhiên',  'DM_SMART',   'NCC_APPLE',   27500000.00, 31990000.00, 25, N'Chiếc', N'Chip A17 Pro mạnh mẽ, camera tiềm vọng 5x, khung titan chuẩn hàng không vũ trụ.', N'Đang bán'),
('SP_MBP16M3',N'MacBook Pro 16 inch M3 Max (36GB/1TB)',   'DM_LAPTOP',  'NCC_APPLE',   65000000.00, 74990000.00, 10, N'Chiếc', N'Chip Apple M3 Max 14-core CPU, 30-core GPU, màn hình Liquid Retina XDR tuyệt đỉnh.', N'Đang bán'),
('SP_S24ULTRA',N'Samsung Galaxy S24 Ultra 5G 512GB Grey', 'DM_SMART',   'NCC_SAMSUNG', 26000000.00, 30490000.00, 18, N'Chiếc', N'Quyền năng Galaxy AI, bút S-Pen tích hợp, khung viền titan và camera 200MP zoom 100x.', N'Đang bán'),
('SP_DELLXPS',N'Dell XPS 15 9530 (i7-13700H/16GB/1TB/RTX 4050)', 'DM_LAPTOP', 'NCC_DELL', 42000000.00, 48990000.00, 12, N'Chiếc', N'Màn hình OLED 3.5K cảm ứng tràn viền, vỏ nhôm nguyên khối cắt CNC chuẩn doanh nhân.', N'Đang bán'),
('SP_ROGZEPH',N'ASUS ROG Zephyrus G16 OLED (Core Ultra 9/RTX 4070)', 'DM_LAPTOP', 'NCC_ASUS', 51000000.00, 58990000.00, 8, N'Chiếc', N'Laptop gaming cao cấp siêu mỏng nhẹ, màn hình ROG Nebula OLED 240Hz sắc nét đỉnh cao.', N'Đang bán'),
('SP_IPADM4', N'iPad Pro 11 inch M4 Wi-Fi 256GB Space Black', 'DM_TABLET', 'NCC_APPLE',   24000000.00, 27990000.00, 15, N'Chiếc', N'Thiết kế siêu mỏng 5.3mm, chip Apple M4 thế hệ mới nhất, màn hình Ultra Retina XDR OLED.', N'Đang bán'),
('SP_TAB_S9', N'Samsung Galaxy Tab S9 Ultra Wi-Fi 256GB', 'DM_TABLET',  'NCC_SAMSUNG', 21000000.00, 24500000.00, 14, N'Chiếc', N'Màn hình Dynamic AMOLED 2X 14.6 inch, chuẩn kháng nước IP68, bút S-Pen siêu nhạy.', N'Đang bán'),
('SP_SONYXM5',N'Tai nghe không dây Sony WH-1000XM5 Black', 'DM_AUDIO',   'NCC_SONY',    6500000.00,  8190000.00,  30, N'Chiếc', N'Khả năng chống ồn chủ động đầu ngành với 2 bộ xử lý và 8 mic, chất âm Hi-Res Audio.', N'Đang bán'),
('SP_MXMASTER',N'Chuột không dây Logitech MX Master 3S',  'DM_PHUKIEN', 'NCC_LOGITECH', 2100000.00,  2690000.00,  45, N'Chiếc', N'Cảm biến Quiet Clicks 8000 DPI, cuộn MagSpeed siêu nhanh, kết nối 3 thiết bị cùng lúc.', N'Đang bán'),
('SP_DELLU27',N'Màn hình Dell UltraSharp 27 inch 4K (U2723QE)', 'DM_MANHINH', 'NCC_DELL', 11500000.00, 13890000.00, 20, N'Chiếc', N'Màn hình IPS Black đầu tiên trên thế giới, độ tương phản 2000:1, chuẩn màu đồ họa 98% DCI-P3.', N'Đang bán');
GO

-- ============================================================================
-- 7. CHÈN BẢNG DON_HANG
-- ============================================================================
INSERT INTO DON_HANG (MaDonHang, MaKH, MaNV, NgayDat, TongTien, PhuongThucThanhToan, TrangThaiDonHang, DiaChiGiaoHang, GhiChu) VALUES
('DH001', 'KH001', 'NV004', '2024-05-10 09:30:00', 31990000.00, N'Thẻ tín dụng', N'Hoàn thành',   N'123 Lê Lợi, Phường Bến Nghé, Q.1, TP.HCM',     N'Giao giờ hành chính, gọi trước 15p'),
('DH002', 'KH002', 'NV005', '2024-05-15 14:15:00', 34990000.00, N'Chuyển khoản',N'Hoàn thành',   N'45 Hai Bà Trưng, Phường 6, Q.3, TP.HCM',        N'Giao hàng tận tay khách'),
('DH003', 'KH003', 'NV004', '2024-06-01 10:00:00', 16580000.00, N'Ví điện tử',  N'Hoàn thành',   N'88 Nguyễn Trãi, Phường 3, Q.5, TP.HCM',          N'Bọc màng chống sốc kỹ'),
('DH004', 'KH004', 'NV005', '2024-06-20 16:45:00', 8190000.00,  N'Tiền mặt',    N'Hoàn thành',   N'220 Hoàng Văn Thụ, P.4, Tân Bình, TP.HCM',     N'Thu tiền mặt khi nhận hàng (COD)'),
('DH005', 'KH005', 'NV004', '2024-07-05 11:20:00', 47200000.00, N'Thẻ tín dụng', N'Hoàn thành',   N'12 Võ Văn Ngân, Linh Chiểu, Thủ Đức, TP.HCM',    N'Khách yêu cầu hóa đơn VAT'),
('DH006', 'KH007', 'NV005', '2024-08-02 08:50:00', 74990000.00, N'Chuyển khoản',N'Hoàn thành',   N'78 Nguyễn Thị Minh Khai, Đa Kao, Q.1, TP.HCM', N'Hàng giá trị cao giao trực tiếp'),
('DH007', 'KH008', 'NV004', '2024-08-25 15:30:00', 12300000.00, N'Ví điện tử',  N'Hoàn thành',   N'104 Chu Văn An, P.26, Bình Thạnh, TP.HCM',      NULL),
('DH008', 'KH001', 'NV005', '2024-09-10 13:10:00', 20510000.00, N'Thẻ tín dụng', N'Hoàn thành',   N'123 Lê Lợi, Phường Bến Nghé, Q.1, TP.HCM',     N'Tặng kèm túi xách TechStore'),
('DH009', 'KH003', 'NV004', '2024-10-02 17:00:00', 2690000.00,  N'Tiền mặt',    N'Đang giao hàng',N'88 Nguyễn Trãi, Phường 3, Q.5, TP.HCM',          N'Giao buổi tối sau 18h'),
('DH010', 'KH006', 'NV005', '2024-10-15 10:40:00', 2690000.00,  N'Ví điện tử',  N'Đang xử lý',    N'50 Phan Đăng Lưu, P.1, Phú Nhuận, TP.HCM',      NULL),
('DH011', 'KH002', NULL,    '2024-10-20 09:00:00', 30490000.00, N'Chuyển khoản',N'Chờ xác nhận', N'45 Hai Bà Trưng, Phường 6, Q.3, TP.HCM',        N'Chờ khách chuyển tiền qua VietQR'),
('DH012', 'KH005', 'NV004', '2024-10-22 14:00:00', 58990000.00, N'Thẻ tín dụng', N'Đã hủy',       N'12 Võ Văn Ngân, Linh Chiểu, Thủ Đức, TP.HCM',    N'Khách đổi ý mua dòng khác');
GO

-- ============================================================================
-- 8. CHÈN BẢNG CHI_TIET_DON_HANG
-- ============================================================================
INSERT INTO CHI_TIET_DON_HANG (MaDonHang, MaSP, SoLuong, DonGia, ChietKhau) VALUES
('DH001', 'SP_IP15PM',   1, 31990000.00, 0.00),
('DH002', 'SP_S24ULTRA', 1, 30490000.00, 0.00),
('DH002', 'SP_MXMASTER', 1,  2690000.00, 0.00),
('DH003', 'SP_MXMASTER', 1,  2690000.00, 0.00),
('DH003', 'SP_DELLU27',  1, 13890000.00, 0.00),
('DH004', 'SP_SONYXM5',  1,  8190000.00, 0.00),
('DH005', 'SP_DELLXPS',  1, 48990000.00, 3.65), -- Có chiết khấu ưu đãi khách VIP
('DH006', 'SP_MBP16M3',  1, 74990000.00, 0.00),
('DH007', 'SP_SONYXM5',  1,  8190000.00, 0.00),
('DH007', 'SP_MXMASTER', 1,  2690000.00, 0.00),
('DH008', 'SP_DELLU27',  1, 13890000.00, 0.00),
('DH008', 'SP_SONYXM5',  1,  8190000.00, 5.00),
('DH009', 'SP_MXMASTER', 1,  2690000.00, 0.00),
('DH010', 'SP_MXMASTER', 1,  2690000.00, 0.00),
('DH011', 'SP_S24ULTRA', 1, 30490000.00, 0.00),
('DH012', 'SP_ROGZEPH',  1, 58990000.00, 0.00);
GO

-- ============================================================================
-- 9. CHÈN BẢNG HOA_DON (1 - 1 với các đơn hàng đã thanh toán)
-- ============================================================================
INSERT INTO HOA_DON (MaHoaDon, MaDonHang, NgayLap, SoTienThanhToan, HinhThucThanhToan, TrangThaiThanhToan, MaGiaoDichNganHang) VALUES
('HD001', 'DH001', '2024-05-10 09:35:00', 31990000.00, N'Thẻ tín dụng',  N'Đã thanh toán', 'TXN_VISA_9812401'),
('HD002', 'DH002', '2024-05-15 14:20:00', 34990000.00, N'Chuyển khoản', N'Đã thanh toán', 'VCB_MB_8831920'),
('HD003', 'DH003', '2024-06-01 10:05:00', 16580000.00, N'Ví MoMo',       N'Đã thanh toán', 'MOMO_77392104'),
('HD004', 'DH004', '2024-06-20 17:30:00',  8190000.00, N'Tiền mặt COD',  N'Đã thanh toán', 'COD_REC_55102'),
('HD005', 'DH005', '2024-07-05 11:25:00', 47200000.00, N'Thẻ Master',    N'Đã thanh toán', 'TXN_MC_6619023'),
('HD006', 'DH006', '2024-08-02 08:55:00', 74990000.00, N'Chuyển khoản', N'Đã thanh toán', 'BIDV_FT_4402198'),
('HD007', 'DH007', '2024-08-25 15:35:00', 12300000.00, N'Ví ZaloPay',   N'Đã thanh toán', 'ZP_88201944'),
('HD008', 'DH008', '2024-09-10 13:15:00', 20510000.00, N'Thẻ tín dụng',  N'Đã thanh toán', 'TXN_VISA_1102934');
GO

-- ============================================================================
-- 10. CHÈN BẢNG DANH_GIA_SAN_PHAM
-- ============================================================================
INSERT INTO DANH_GIA_SAN_PHAM (MaDanhGia, MaSP, MaKH, DiemDanhGia, BinhLuan, NgayDanhGia) VALUES
('DG001', 'SP_IP15PM',   'KH001', 5, N'Điện thoại dùng rất mượt mà, khung viền titan cầm cực nhẹ tay, pin trâu.', '2024-05-12 11:00:00'),
('DG002', 'SP_S24ULTRA', 'KH002', 5, N'Tính năng AI khoanh tròn tìm kiếm cực kỳ tiện lợi, camera chụp đêm siêu nét!', '2024-05-18 19:20:00'),
('DG003', 'SP_MXMASTER', 'KH002', 5, N'Chuột làm việc đỉnh nhất từng dùng, cuộn con lăn êm ru, pin 2 tháng sạc 1 lần.', '2024-05-19 08:30:00'),
('DG004', 'SP_DELLU27',  'KH003', 5, N'Màu sắc cực chuẩn cho dân thiết kế đồ họa, cổng Type-C sạc 90W tiện dụng.', '2024-06-05 14:10:00'),
('DG005', 'SP_SONYXM5',  'KH004', 4, N'Chống ồn tốt, âm bass êm ái, đeo lâu hơi nóng tai một chút nhưng tổng thể tuyệt vời.', '2024-06-25 20:00:00'),
('DG006', 'SP_MBP16M3',  'KH007', 5, N'Cỗ máy quái vật cho lập trình và render video 8K, pin dùng liên tục 18 tiếng không cần cắm sạc.', '2024-08-05 16:40:00'),
('DG007', 'SP_DELLXPS',  'KH005', 4, N'Thiết kế đẹp mắt sang trọng, màn hình OLED đẹp nhưng quạt tản nhiệt chạy hơi ồn khi tải nặng.', '2024-07-10 10:15:00');
GO

PRINT N'>>> Đã chèn thành công toàn bộ dữ liệu mẫu đa dạng vào TechStoreDB!';
GO
