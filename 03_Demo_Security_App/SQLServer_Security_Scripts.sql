-- ============================================================================
-- ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU (DATABASE SYSTEMS)
-- PHẦN 2: CHƯƠNG 30 - DATABASE SECURITY
-- KỊCH BẢN T-SQL THỰC NGHIỆM TRÊN MICROSOFT SQL SERVER 2019 / 2022
-- Nội dung: DAC (GRANT, REVOKE, DENY), Role-Based Access Control,
--          Dynamic Data Masking (DDM), và Row-Level Security (RLS)
-- ============================================================================

USE TechStoreDB;
GO

-- ============================================================================
-- 1. TẠO CÁC VAI TRÒ CSDL (DATABASE ROLES) VÀ PHÂN QUYỀN TRUY CẬP (DAC / RBAC)
-- ============================================================================

-- Tạo role cho nhân viên bán hàng
IF DATABASE_PRINCIPAL_ID('Role_NhanVienBanHang') IS NULL
    CREATE ROLE Role_NhanVienBanHang;
GO

-- Tạo role cho quản lý cửa hàng
IF DATABASE_PRINCIPAL_ID('Role_QuanLyCuaHang') IS NULL
    CREATE ROLE Role_QuanLyCuaHang;
GO

-- Cấp quyền cho Role_NhanVienBanHang
GRANT SELECT ON SAN_PHAM TO Role_NhanVienBanHang;
GRANT SELECT ON DANH_MUC TO Role_NhanVienBanHang;
GRANT SELECT, INSERT ON DON_HANG TO Role_NhanVienBanHang;
GRANT SELECT, INSERT ON CHI_TIET_DON_HANG TO Role_NhanVienBanHang;
GRANT SELECT (MaKH, HoTen, SoDienThoai, DiaChi, HangThanhVien) ON KHACH_HANG TO Role_NhanVienBanHang;

-- CẤM tuyệt đối nhân viên bán hàng xem thông tin lương của nhân viên
DENY SELECT ON NHAN_VIEN(LuongCoBan) TO Role_NhanVienBanHang;
DENY SELECT ON NHAN_VIEN(MatKhauHash) TO Role_NhanVienBanHang;
DENY DELETE ON DON_HANG TO Role_NhanVienBanHang;
GO

-- Cấp quyền cho Role_QuanLyCuaHang
GRANT SELECT, UPDATE(GiaBan, SoLuongTon) ON SAN_PHAM TO Role_QuanLyCuaHang;
GRANT SELECT, UPDATE(TrangThaiDonHang) ON DON_HANG TO Role_QuanLyCuaHang;
GRANT SELECT ON NHAN_VIEN TO Role_QuanLyCuaHang;
GRANT SELECT ON HOA_DON TO Role_QuanLyCuaHang;
GO

-- ============================================================================
-- 2. TRIỂN KHAI DYNAMIC DATA MASKING (DDM) BẢO VỆ DỮ LIỆU NHẠY CẢM
-- ============================================================================

-- Mặt nạ số điện thoại khách hàng: Hiển thị 3 số đầu, ẩn giữa bằng X, hiển thị 2 số cuối
ALTER TABLE KHACH_HANG
ALTER COLUMN SoDienThoai ADD MASKED WITH (FUNCTION = 'partial(3, "XXXXXX", 2)');
GO

-- Mặt nạ Email khách hàng: tự động chuyển thành aXXX@gmail.com
ALTER TABLE KHACH_HANG
ALTER COLUMN Email ADD MASKED WITH (FUNCTION = 'email()');
GO

-- Mặt nạ mã giao dịch ngân hàng
ALTER TABLE HOA_DON
ALTER COLUMN MaGiaoDichNganHang ADD MASKED WITH (FUNCTION = 'default()');
GO

-- ============================================================================
-- 3. TRIỂN KHAI ROW-LEVEL SECURITY (RLS) - BẢO MẬT MỨC HÀNG
-- Khách hàng chỉ xem được đơn hàng của chính mình
-- ============================================================================

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Security')
    EXEC('CREATE SCHEMA Security');
GO

-- Tạo vị từ bảo mật (Predicate function)
IF OBJECT_ID('Security.fn_DonHangSecurityPredicate', 'IF') IS NOT NULL
    DROP FUNCTION Security.fn_DonHangSecurityPredicate;
GO

CREATE FUNCTION Security.fn_DonHangSecurityPredicate(@MaKH VARCHAR(20))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_access_result
WHERE 
    -- Quản trị viên và Quản lý được xem toàn bộ đơn
    IS_MEMBER('Role_QuanLyCuaHang') = 1 
    OR IS_MEMBER('db_owner') = 1
    -- Khách hàng chỉ xem đơn trùng khớp với MaKH đã đăng nhập trong SESSION_CONTEXT
    OR @MaKH = CAST(SESSION_CONTEXT(N'CurrentLogin_MaKH') AS VARCHAR(20));
GO

-- Kích hoạt chính sách bảo mật Security Policy
IF EXISTS (SELECT * FROM sys.security_policies WHERE name = 'DonHangSecurityPolicy')
    DROP SECURITY POLICY Security.DonHangSecurityPolicy;
GO

CREATE SECURITY POLICY Security.DonHangSecurityPolicy
ADD FILTER PREDICATE Security.fn_DonHangSecurityPredicate(MaKH) ON dbo.DON_HANG
WITH (STATE = ON);
GO

-- ============================================================================
-- 4. KỊCH BẢN THỬ NGHIỆM ROW-LEVEL SECURITY
-- ============================================================================

-- Thử nghiệm 1: Thiết lập phiên đăng nhập là khách hàng KH001
EXEC sp_set_session_context 'CurrentLogin_MaKH', 'KH001';
SELECT MaDonHang, MaKH, NgayDat, TongTien, TrangThaiDonHang FROM DON_HANG;
-- Kết quả: Chỉ thấy các đơn hàng của KH001!

-- Thử nghiệm 2: Đổi sang khách hàng KH002
EXEC sp_set_session_context 'CurrentLogin_MaKH', 'KH002';
SELECT MaDonHang, MaKH, NgayDat, TongTien, TrangThaiDonHang FROM DON_HANG;
-- Kết quả: Lập tức chỉ thấy các đơn hàng của KH002!

-- Thử nghiệm 3: Đặt lại phiên làm việc (Admin)
EXEC sp_set_session_context 'CurrentLogin_MaKH', NULL;
GO

PRINT N'>>> Đã cài đặt hoàn chỉnh kịch bản DAC, RBAC, Data Masking và Row-Level Security trên SQL Server!';
GO

