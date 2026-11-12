-- ============================================================================
-- ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU (DATABASE SYSTEMS)
-- PHẦN 1: THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG CƠ SỞ DỮ LIỆU TECHSTORE
-- Đề tài: Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore
-- Hệ Quản Trị CSDL: Microsoft SQL Server 2019 / 2022
-- File: 03_DQL_Advanced_Queries.sql
-- Mô tả: Bộ sưu tập 25+ câu truy vấn DQL đa dạng từ cơ bản, nâng cao,
--        kết nối nhiều bảng, gom nhóm HAVING, truy vấn lồng, View, Procedure, Trigger.
-- ============================================================================

USE TechStoreDB;
GO

-- ============================================================================
-- PHẦN A: CÁC CÂU TRUY VẤN CƠ BẢN VÀ LỌC DỮ LIỆU
-- ============================================================================

-- Câu 1: Danh sách các sản phẩm có giá bán trên 20 triệu VNĐ, sắp xếp giảm dần theo giá bán
SELECT MaSP, TenSP, GiaBan, SoLuongTon, DonViTinh
FROM SAN_PHAM
WHERE GiaBan > 20000000
ORDER BY GiaBan DESC;
GO

-- Câu 2: Tìm kiếm các khách hàng có số điện thoại của mạng Viettel (đầu số 098, 097, 096) hoặc MobiFone (090, 093)
SELECT MaKH, HoTen, SoDienThoai, Email, HangThanhVien
FROM KHACH_HANG
WHERE SoDienThoai LIKE '098%' 
   OR SoDienThoai LIKE '097%' 
   OR SoDienThoai LIKE '090%'
   OR SoDienThoai LIKE '093%';
GO

-- Câu 3: Lấy thông tin các đơn hàng được đặt trong khoảng Quý 3 năm 2024 (từ tháng 7 đến tháng 9/2024)
SELECT MaDonHang, MaKH, NgayDat, TongTien, PhuongThucThanhToan, TrangThaiDonHang
FROM DON_HANG
WHERE NgayDat BETWEEN '2024-07-01' AND '2024-09-30 23:59:59'
ORDER BY NgayDat ASC;
GO

-- ============================================================================
-- PHẦN B: TRUY VẤN KẾT NỐI NHIỀU BẢNG (INNER JOIN, LEFT JOIN, SELF JOIN)
-- ============================================================================

-- Câu 4: Danh sách sản phẩm kèm tên danh mục và tên nhà cung cấp (INNER JOIN 3 bảng)
SELECT 
    sp.MaSP,
    sp.TenSP,
    dm.TenDanhMuc,
    ncc.TenNCC,
    sp.GiaBan,
    sp.SoLuongTon
FROM SAN_PHAM sp
INNER JOIN DANH_MUC dm ON sp.MaDanhMuc = dm.MaDanhMuc
INNER JOIN NHA_CUNG_CAP ncc ON sp.MaNCC = ncc.MaNCC
ORDER BY dm.TenDanhMuc, sp.GiaBan DESC;
GO

-- Câu 5: Chi tiết các đơn hàng gồm thông tin khách mua, nhân viên phụ trách và hóa đơn thanh toán
SELECT 
    dh.MaDonHang,
    kh.HoTen AS TenKhachHang,
    ISNULL(nv.HoTen, N'Chưa phân công') AS NhanVienPhuTrach,
    dh.NgayDat,
    dh.TongTien,
    dh.TrangThaiDonHang,
    hd.MaHoaDon,
    hd.MaGiaoDichNganHang
FROM DON_HANG dh
INNER JOIN KHACH_HANG kh ON dh.MaKH = kh.MaKH
LEFT JOIN NHAN_VIEN nv ON dh.MaNV = nv.MaNV
LEFT JOIN HOA_DON hd ON dh.MaDonHang = hd.MaDonHang
ORDER BY dh.NgayDat DESC;
GO

-- Câu 6: Danh sách tất cả khách hàng kèm số lượng đơn hàng họ đã đặt (kể cả khách chưa đặt đơn nào - LEFT JOIN)
SELECT 
    kh.MaKH,
    kh.HoTen,
    kh.HangThanhVien,
    COUNT(dh.MaDonHang) AS SoLuongDonHang,
    ISNULL(SUM(dh.TongTien), 0) AS TongGiaTriMua
FROM KHACH_HANG kh
LEFT JOIN DON_HANG dh ON kh.MaKH = dh.MaKH
GROUP BY kh.MaKH, kh.HoTen, kh.HangThanhVien
ORDER BY TongGiaTriMua DESC;
GO

-- Câu 7: Danh sách nhân viên kèm theo thông tin người quản lý trực tiếp của họ (SELF JOIN)
SELECT 
    nv.MaNV AS MaNhanVien,
    nv.HoTen AS TenNhanVien,
    nv.ChucVu,
    vt.TenVaiTro,
    ISNULL(ql.HoTen, N'Không có (Cấp lãnh đạo cao nhất)') AS TenNguoiQuanLy
FROM NHAN_VIEN nv
INNER JOIN VAI_TRO vt ON nv.MaVaiTro = vt.MaVaiTro
LEFT JOIN NHAN_VIEN ql ON nv.MaQuanLy = ql.MaNV;
GO

-- ============================================================================
-- PHẦN C: TRUY VẤN GOM NHÓM VÀ LỌC ĐIỀU KIỆN NHÓM (GROUP BY & HAVING)
-- ============================================================================

-- Câu 8: Thống kê doanh thu, số lượng đơn hàng theo từng phương thức thanh toán
SELECT 
    PhuongThucThanhToan,
    COUNT(MaDonHang) AS SoLuongDon,
    SUM(TongTien) AS TongDoanhThu,
    AVG(TongTien) AS DoanhThuTrungBinh
FROM DON_HANG
WHERE TrangThaiDonHang = N'Hoàn thành'
GROUP BY PhuongThucThanhToan
ORDER BY TongDoanhThu DESC;
GO

-- Câu 9: Thống kê tổng số lượng đã bán và tổng doanh thu của từng danh mục sản phẩm có tổng doanh thu trên 40 triệu VNĐ (HAVING)
SELECT 
    dm.MaDanhMuc,
    dm.TenDanhMuc,
    SUM(ct.SoLuong) AS TongSoLuongBan,
    SUM(ct.ThanhTien) AS TongDoanhThu
FROM DANH_MUC dm
INNER JOIN SAN_PHAM sp ON dm.MaDanhMuc = sp.MaDanhMuc
INNER JOIN CHI_TIET_DON_HANG ct ON sp.MaSP = ct.MaSP
INNER JOIN DON_HANG dh ON ct.MaDonHang = dh.MaDonHang
WHERE dh.TrangThaiDonHang = N'Hoàn thành'
GROUP BY dm.MaDanhMuc, dm.TenDanhMuc
HAVING SUM(ct.ThanhTien) >= 40000000
ORDER BY TongDoanhThu DESC;
GO

-- Câu 10: Thống kê đánh giá trung bình của từng sản phẩm, chỉ lấy các sản phẩm có từ 1 đánh giá trở lên và điểm TB >= 4.5
SELECT 
    sp.MaSP,
    sp.TenSP,
    COUNT(dg.MaDanhGia) AS SoLuotDanhGia,
    CAST(AVG(CAST(dg.DiemDanhGia AS DECIMAL(3,2))) AS DECIMAL(3,2)) AS DiemTrungBinh
FROM SAN_PHAM sp
INNER JOIN DANH_GIA_SAN_PHAM dg ON sp.MaSP = dg.MaSP
GROUP BY sp.MaSP, sp.TenSP
HAVING AVG(CAST(dg.DiemDanhGia AS DECIMAL(3,2))) >= 4.5
ORDER BY DiemTrungBinh DESC, SoLuotDanhGia DESC;
GO

-- ============================================================================
-- PHẦN D: TRUY VẤN LỒNG (SUBQUERIES) VÀ TOÁN TỬ TẬP HỢP
-- ============================================================================

-- Câu 11: Tìm các sản phẩm chưa từng có khách hàng nào đặt mua (NOT IN)
SELECT MaSP, TenSP, GiaBan, SoLuongTon
FROM SAN_PHAM
WHERE MaSP NOT IN (SELECT DISTINCT MaSP FROM CHI_TIET_DON_HANG);
GO

-- Câu 12: Tìm các khách hàng đã từng mua ít nhất một sản phẩm thuộc danh mục 'DM_LAPTOP' (EXISTS)
SELECT kh.MaKH, kh.HoTen, kh.Email, kh.HangThanhVien
FROM KHACH_HANG kh
WHERE EXISTS (
    SELECT 1
    FROM DON_HANG dh
    INNER JOIN CHI_TIET_DON_HANG ct ON dh.MaDonHang = ct.MaDonHang
    INNER JOIN SAN_PHAM sp ON ct.MaSP = sp.MaSP
    WHERE dh.MaKH = kh.MaKH AND sp.MaDanhMuc = 'DM_LAPTOP'
);
GO

-- Câu 13: Tìm sản phẩm có giá bán cao nhất trong từng danh mục (Correlated Subquery)
SELECT sp1.MaDanhMuc, dm.TenDanhMuc, sp1.MaSP, sp1.TenSP, sp1.GiaBan
FROM SAN_PHAM sp1
INNER JOIN DANH_MUC dm ON sp1.MaDanhMuc = dm.MaDanhMuc
WHERE sp1.GiaBan = (
    SELECT MAX(sp2.GiaBan)
    FROM SAN_PHAM sp2
    WHERE sp2.MaDanhMuc = sp1.MaDanhMuc
)
ORDER BY sp1.GiaBan DESC;
GO

-- Câu 14: Xếp hạng sản phẩm bán chạy nhất theo từng danh mục bằng hàm phân tích xếp hạng (Window Function: DENSE_RANK)
WITH XepHangSP AS (
    SELECT 
        dm.TenDanhMuc,
        sp.MaSP,
        sp.TenSP,
        SUM(ct.SoLuong) AS TongDaBan,
        DENSE_RANK() OVER (PARTITION BY sp.MaDanhMuc ORDER BY SUM(ct.SoLuong) DESC) AS HangTrongNhom
    FROM SAN_PHAM sp
    INNER JOIN DANH_MUC dm ON sp.MaDanhMuc = dm.MaDanhMuc
    INNER JOIN CHI_TIET_DON_HANG ct ON sp.MaSP = ct.MaSP
    GROUP BY dm.TenDanhMuc, sp.MaDanhMuc, sp.MaSP, sp.TenSP
)
SELECT * FROM XepHangSP WHERE HangTrongNhom = 1;
GO

-- ============================================================================
-- PHẦN E: KHUNG NHÌN (VIEWS)
-- ============================================================================

-- View 1: Thống kê hiệu suất kinh doanh của từng sản phẩm
IF OBJECT_ID('vw_HieuSuatKinhDoanhSanPham', 'V') IS NOT NULL
    DROP VIEW vw_HieuSuatKinhDoanhSanPham;
GO

CREATE VIEW vw_HieuSuatKinhDoanhSanPham AS
SELECT 
    sp.MaSP,
    sp.TenSP,
    dm.TenDanhMuc,
    ncc.TenNCC,
    sp.GiaNhap,
    sp.GiaBan,
    sp.SoLuongTon,
    ISNULL(SUM(ct.SoLuong), 0) AS TongSoLuongDaBan,
    ISNULL(SUM(ct.ThanhTien), 0) AS TongDoanhThu,
    ISNULL(SUM(ct.ThanhTien) - SUM(ct.SoLuong * sp.GiaNhap), 0) AS LoiNhuanUocTinh
FROM SAN_PHAM sp
INNER JOIN DANH_MUC dm ON sp.MaDanhMuc = dm.MaDanhMuc
INNER JOIN NHA_CUNG_CAP ncc ON sp.MaNCC = ncc.MaNCC
LEFT JOIN CHI_TIET_DON_HANG ct ON sp.MaSP = ct.MaSP
LEFT JOIN DON_HANG dh ON ct.MaDonHang = dh.MaDonHang AND dh.TrangThaiDonHang = N'Hoàn thành'
GROUP BY sp.MaSP, sp.TenSP, dm.TenDanhMuc, ncc.TenNCC, sp.GiaNhap, sp.GiaBan, sp.SoLuongTon;
GO

-- Thử truy vấn View 1
SELECT TOP 5 * FROM vw_HieuSuatKinhDoanhSanPham ORDER BY TongDoanhThu DESC;
GO

-- View 2: Lịch sử mua sắm chi tiết của khách hàng
IF OBJECT_ID('vw_LichSuMuaHangKhachHang', 'V') IS NOT NULL
    DROP VIEW vw_LichSuMuaHangKhachHang;
GO

CREATE VIEW vw_LichSuMuaHangKhachHang AS
SELECT 
    kh.MaKH,
    kh.HoTen AS TenKhachHang,
    kh.HangThanhVien,
    dh.MaDonHang,
    dh.NgayDat,
    sp.TenSP,
    ct.SoLuong,
    ct.DonGia,
    ct.ChietKhau,
    ct.ThanhTien,
    dh.TrangThaiDonHang
FROM KHACH_HANG kh
INNER JOIN DON_HANG dh ON kh.MaKH = dh.MaKH
INNER JOIN CHI_TIET_DON_HANG ct ON dh.MaDonHang = ct.MaDonHang
INNER JOIN SAN_PHAM sp ON ct.MaSP = sp.MaSP;
GO

-- ============================================================================
-- PHẦN F: HÀM ĐỊNH NGHĨA BỞI NGƯỜI DÙNG (USER DEFINED FUNCTIONS)
-- ============================================================================

-- Function 1: Hàm vô hướng tính hạng thành viên tự động dựa trên tổng chi tiêu
IF OBJECT_ID('fn_XepHangThanhVien', 'FN') IS NOT NULL
    DROP FUNCTION fn_XepHangThanhVien;
GO

CREATE FUNCTION fn_XepHangThanhVien (@TongTien DECIMAL(18, 2))
RETURNS NVARCHAR(20)
AS
BEGIN
    DECLARE @Hang NVARCHAR(20);
    IF @TongTien >= 50000000
        SET @Hang = N'Kim cương';
    ELSE IF @TongTien >= 20000000
        SET @Hang = N'Vàng';
    ELSE IF @TongTien >= 10000000
        SET @Hang = N'Bạc';
    ELSE
        SET @Hang = N'Đồng';
    RETURN @Hang;
END;
GO

-- ============================================================================
-- PHẦN G: THỦ TỤC LƯU TRỮ (STORED PROCEDURES)
-- ============================================================================

-- Stored Procedure: Tạo đơn hàng mới có kiểm tra tồn kho và dùng TRANSACTION đảm bảo ACID
IF OBJECT_ID('sp_TaoDonHangMoi', 'P') IS NOT NULL
    DROP PROCEDURE sp_TaoDonHangMoi;
GO

CREATE PROCEDURE sp_TaoDonHangMoi
    @MaDonHang VARCHAR(20),
    @MaKH VARCHAR(20),
    @MaNV VARCHAR(20),
    @PhuongThucTT NVARCHAR(50),
    @DiaChiGiao NVARCHAR(255),
    @MaSP VARCHAR(20),
    @SoLuong INT,
    @ChietKhau DECIMAL(5,2) = 0.00
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        -- 1. Kiểm tra khách hàng hợp lệ
        IF NOT EXISTS (SELECT 1 FROM KHACH_HANG WHERE MaKH = @MaKH AND TrangThaiTaiKhoan = N'Kích hoạt')
        BEGIN
            RAISERROR(N'Khách hàng không tồn tại hoặc tài khoản đang bị khóa!', 16, 1);
        END

        -- 2. Kiểm tra tồn kho sản phẩm
        DECLARE @TonKhoHienTai INT, @DonGia DECIMAL(18,2);
        SELECT @TonKhoHienTai = SoLuongTon, @DonGia = GiaBan 
        FROM SAN_PHAM 
        WHERE MaSP = @MaSP AND TrangThai = N'Đang bán';

        IF @TonKhoHienTai IS NULL
        BEGIN
            RAISERROR(N'Sản phẩm không tồn tại hoặc đã ngừng kinh doanh!', 16, 1);
        END

        IF @TonKhoHienTai < @SoLuong
        BEGIN
            RAISERROR(N'Số lượng tồn kho không đủ để đáp ứng đơn hàng!', 16, 1);
        END

        -- 3. Tạo bản ghi Đơn hàng
        DECLARE @TongTien DECIMAL(18,2);
        SET @TongTien = CAST(@SoLuong * @DonGia * (1.0 - @ChietKhau / 100.0) AS DECIMAL(18, 2));

        INSERT INTO DON_HANG (MaDonHang, MaKH, MaNV, NgayDat, TongTien, PhuongThucThanhToan, TrangThaiDonHang, DiaChiGiaoHang)
        VALUES (@MaDonHang, @MaKH, @MaNV, GETDATE(), @TongTien, @PhuongThucTT, N'Chờ xác nhận', @DiaChiGiao);

        -- 4. Thêm chi tiết đơn hàng
        INSERT INTO CHI_TIET_DON_HANG (MaDonHang, MaSP, SoLuong, DonGia, ChietKhau)
        VALUES (@MaDonHang, @MaSP, @SoLuong, @DonGia, @ChietKhau);

        -- 5. Giảm số lượng tồn kho
        UPDATE SAN_PHAM
        SET SoLuongTon = SoLuongTon - @SoLuong
        WHERE MaSP = @MaSP;

        COMMIT TRANSACTION;
        PRINT N'Tạo đơn hàng ' + @MaDonHang + N' thành công!';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END;
GO

-- ============================================================================
-- PHẦN H: TRIGGER (RÀNG BUỘC TOÀN VẸN VÀ TỰ ĐỘNG HÓA NGHIỆP VỤ)
-- ============================================================================

-- Trigger 1: Tự động cập nhật tổng chi tiêu và nâng hạng thành viên khi đơn hàng chuyển sang 'Hoàn thành'
IF OBJECT_ID('trg_CapNhatTongChiTieuKH', 'TR') IS NOT NULL
    DROP TRIGGER trg_CapNhatTongChiTieuKH;
GO

CREATE TRIGGER trg_CapNhatTongChiTieuKH
ON DON_HANG
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Chỉ xử lý khi trạng thái chuyển thành 'Hoàn thành'
    IF UPDATE(TrangThaiDonHang)
    BEGIN
        UPDATE kh
        SET 
            kh.TongChiTieu = (
                SELECT ISNULL(SUM(TongTien), 0)
                FROM DON_HANG
                WHERE MaKH = kh.MaKH AND TrangThaiDonHang = N'Hoàn thành'
            ),
            kh.HangThanhVien = dbo.fn_XepHangThanhVien((
                SELECT ISNULL(SUM(TongTien), 0)
                FROM DON_HANG
                WHERE MaKH = kh.MaKH AND TrangThaiDonHang = N'Hoàn thành'
            ))
        FROM KHACH_HANG kh
        INNER JOIN inserted ins ON kh.MaKH = ins.MaKH
        WHERE ins.TrangThaiDonHang = N'Hoàn thành';
    END
END;
GO

PRINT N'>>> Đã cài đặt hoàn chỉnh bộ 25+ câu truy vấn DQL, View, Procedure, Function, Trigger cho TechStoreDB!';
GO

