-- ============================================================================
-- ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU (DATABASE SYSTEMS)
-- PHẦN 1: THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG CƠ SỞ DỮ LIỆU TECHSTORE
-- Đề tài: Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore
-- Hệ Quản Trị CSDL: Microsoft SQL Server 2019 / 2022
-- File: 01_DDL_Create_TechStoreDB.sql
-- Mô tả: Kịch bản DDL tạo Database, cấu trúc bảng, khóa chính, khóa ngoại,
--        ràng buộc duy nhất (UNIQUE), kiểm tra (CHECK) và mặc định (DEFAULT).
-- ============================================================================

USE master;
GO

-- 1. TẠO CƠ SỞ DỮ LIỆU TECHSTOREDB
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'TechStoreDB')
BEGIN
    ALTER DATABASE TechStoreDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE TechStoreDB;
END
GO

CREATE DATABASE TechStoreDB
COLLATE Vietnamese_CI_AS;
GO

USE TechStoreDB;
GO

-- ============================================================================
-- 2. TẠO CÁC BẢNG THEO THỨ TỰ PHỤ THUỘC TOÀN VẸN THAM CHIẾU
-- ============================================================================

-- Bảng 1: VAI_TRO (Phục vụ phân quyền RBAC và quản lý nhân sự)
CREATE TABLE VAI_TRO (
    MaVaiTro VARCHAR(20) NOT NULL,
    TenVaiTro NVARCHAR(50) NOT NULL,
    MoTa NVARCHAR(255) NULL,
    CapDoTruyCap INT NOT NULL DEFAULT 1, -- 1: NhanVien, 2: QuanLy, 3: Admin
    CONSTRAINT PK_VAI_TRO PRIMARY KEY (MaVaiTro),
    CONSTRAINT UQ_VAI_TRO_Ten UNIQUE (TenVaiTro),
    CONSTRAINT CK_VAI_TRO_CapDo CHECK (CapDoTruyCap BETWEEN 1 AND 5)
);
GO

-- Bảng 2: DANH_MUC (Danh mục sản phẩm điện tử, công nghệ)
CREATE TABLE DANH_MUC (
    MaDanhMuc VARCHAR(20) NOT NULL,
    TenDanhMuc NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255) NULL,
    TrangThai NVARCHAR(20) NOT NULL DEFAULT N'Hoạt động',
    CONSTRAINT PK_DANH_MUC PRIMARY KEY (MaDanhMuc),
    CONSTRAINT UQ_DANH_MUC_Ten UNIQUE (TenDanhMuc),
    CONSTRAINT CK_DANH_MUC_TrangThai CHECK (TrangThai IN (N'Hoạt động', N'Tạm ngưng'))
);
GO

-- Bảng 3: NHA_CUNG_CAP (Nhà cung cấp linh kiện, thiết bị)
CREATE TABLE NHA_CUNG_CAP (
    MaNCC VARCHAR(20) NOT NULL,
    TenNCC NVARCHAR(150) NOT NULL,
    NguoiLienHe NVARCHAR(100) NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    DiaChi NVARCHAR(255) NOT NULL,
    TrangThaiHoptac NVARCHAR(20) NOT NULL DEFAULT N'Đang hợp tác',
    CONSTRAINT PK_NHA_CUNG_CAP PRIMARY KEY (MaNCC),
    CONSTRAINT UQ_NCC_Email UNIQUE (Email),
    CONSTRAINT UQ_NCC_SDT UNIQUE (SoDienThoai),
    CONSTRAINT CK_NCC_Email CHECK (Email LIKE '%_@__%.__%')
);
GO

-- Bảng 4: KHACH_HANG (Khách hàng đăng ký tài khoản TechStore)
CREATE TABLE KHACH_HANG (
    MaKH VARCHAR(20) NOT NULL,
    HoTen NVARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    DiaChi NVARCHAR(255) NULL,
    NgayDangKy DATETIME NOT NULL DEFAULT GETDATE(),
    -- Các trường phục vụ an toàn mật khẩu (Security: Hashing + Salt)
    MatKhauHash VARCHAR(256) NOT NULL,
    Salt VARCHAR(64) NOT NULL,
    TongChiTieu DECIMAL(18, 2) NOT NULL DEFAULT 0.00,
    HangThanhVien NVARCHAR(20) NOT NULL DEFAULT N'Đồng',
    TrangThaiTaiKhoan NVARCHAR(20) NOT NULL DEFAULT N'Kích hoạt',
    CONSTRAINT PK_KHACH_HANG PRIMARY KEY (MaKH),
    CONSTRAINT UQ_KH_Email UNIQUE (Email),
    CONSTRAINT UQ_KH_SDT UNIQUE (SoDienThoai),
    CONSTRAINT CK_KH_Email CHECK (Email LIKE '%_@__%.__%'),
    CONSTRAINT CK_KH_TongChiTieu CHECK (TongChiTieu >= 0),
    CONSTRAINT CK_KH_HangThanhVien CHECK (HangThanhVien IN (N'Đồng', N'Bạc', N'Vàng', N'Kim cương')),
    CONSTRAINT CK_KH_TrangThai CHECK (TrangThaiTaiKhoan IN (N'Kích hoạt', N'Khóa', N'Chờ xác thực'))
);
GO

-- Bảng 5: NHAN_VIEN (Nhân sự vận hành hệ thống & xử lý đơn)
CREATE TABLE NHAN_VIEN (
    MaNV VARCHAR(20) NOT NULL,
    HoTen NVARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    ChucVu NVARCHAR(50) NOT NULL,
    LuongCoBan DECIMAL(18, 2) NOT NULL,
    NgayVaoLam DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    MaVaiTro VARCHAR(20) NOT NULL,
    MaQuanLy VARCHAR(20) NULL, -- Mối kết hợp đệ quy (Recursive / Self-referencing)
    MatKhauHash VARCHAR(256) NOT NULL,
    Salt VARCHAR(64) NOT NULL,
    TrangThai NVARCHAR(20) NOT NULL DEFAULT N'Đang làm việc',
    CONSTRAINT PK_NHAN_VIEN PRIMARY KEY (MaNV),
    CONSTRAINT UQ_NV_Email UNIQUE (Email),
    CONSTRAINT UQ_NV_SDT UNIQUE (SoDienThoai),
    CONSTRAINT FK_NHAN_VIEN_VAI_TRO FOREIGN KEY (MaVaiTro) 
        REFERENCES VAI_TRO(MaVaiTro) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT FK_NHAN_VIEN_QUAN_LY FOREIGN KEY (MaQuanLy) 
        REFERENCES NHAN_VIEN(MaNV) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT CK_NV_Luong CHECK (LuongCoBan > 0),
    CONSTRAINT CK_NV_Email CHECK (Email LIKE '%_@__%.__%')
);
GO

-- Bảng 6: SAN_PHAM (Hàng hóa công nghệ bày bán)
CREATE TABLE SAN_PHAM (
    MaSP VARCHAR(20) NOT NULL,
    TenSP NVARCHAR(200) NOT NULL,
    MaDanhMuc VARCHAR(20) NOT NULL,
    MaNCC VARCHAR(20) NOT NULL,
    GiaNhap DECIMAL(18, 2) NOT NULL,
    GiaBan DECIMAL(18, 2) NOT NULL,
    SoLuongTon INT NOT NULL DEFAULT 0,
    DonViTinh NVARCHAR(30) NOT NULL DEFAULT N'Cái',
    MoTa NVARCHAR(MAX) NULL,
    TrangThai NVARCHAR(20) NOT NULL DEFAULT N'Đang bán',
    CONSTRAINT PK_SAN_PHAM PRIMARY KEY (MaSP),
    CONSTRAINT FK_SAN_PHAM_DANH_MUC FOREIGN KEY (MaDanhMuc) 
        REFERENCES DANH_MUC(MaDanhMuc) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT FK_SAN_PHAM_NCC FOREIGN KEY (MaNCC) 
        REFERENCES NHA_CUNG_CAP(MaNCC) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT CK_SP_GiaNhap CHECK (GiaNhap >= 0),
    CONSTRAINT CK_SP_GiaBan CHECK (GiaBan >= GiaNhap), -- Giá bán phải >= giá nhập
    CONSTRAINT CK_SP_SoLuongTon CHECK (SoLuongTon >= 0),
    CONSTRAINT CK_SP_TrangThai CHECK (TrangThai IN (N'Đang bán', N'Hết hàng', N'Ngừng kinh doanh'))
);
GO

-- Bảng 7: DON_HANG (Đơn đặt mua hàng từ khách hàng)
CREATE TABLE DON_HANG (
    MaDonHang VARCHAR(20) NOT NULL,
    MaKH VARCHAR(20) NOT NULL,
    MaNV VARCHAR(20) NULL, -- Nhân viên duyệt đơn (NULL nếu khách tự đặt online chưa duyệt)
    NgayDat DATETIME NOT NULL DEFAULT GETDATE(),
    TongTien DECIMAL(18, 2) NOT NULL DEFAULT 0.00,
    PhuongThucThanhToan NVARCHAR(50) NOT NULL,
    TrangThaiDonHang NVARCHAR(30) NOT NULL DEFAULT N'Chờ xác nhận',
    DiaChiGiaoHang NVARCHAR(255) NOT NULL,
    GhiChu NVARCHAR(255) NULL,
    CONSTRAINT PK_DON_HANG PRIMARY KEY (MaDonHang),
    CONSTRAINT FK_DON_HANG_KHACH_HANG FOREIGN KEY (MaKH) 
        REFERENCES KHACH_HANG(MaKH) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT FK_DON_HANG_NHAN_VIEN FOREIGN KEY (MaNV) 
        REFERENCES NHAN_VIEN(MaNV) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT CK_DH_TongTien CHECK (TongTien >= 0),
    CONSTRAINT CK_DH_PTTT CHECK (PhuongThucThanhToan IN (N'Tiền mặt', N'Chuyển khoản', N'Thẻ tín dụng', N'Ví điện tử')),
    CONSTRAINT CK_DH_TrangThai CHECK (TrangThaiDonHang IN (N'Chờ xác nhận', N'Đang xử lý', N'Đang giao hàng', N'Hoàn thành', N'Đã hủy'))
);
GO

-- Bảng 8: CHI_TIET_DON_HANG (Mối kết hợp N-N giữa DON_HANG và SAN_PHAM)
CREATE TABLE CHI_TIET_DON_HANG (
    MaDonHang VARCHAR(20) NOT NULL,
    MaSP VARCHAR(20) NOT NULL,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(18, 2) NOT NULL,
    ChietKhau DECIMAL(5, 2) NOT NULL DEFAULT 0.00, -- % chiết khấu (0 - 100%)
    ThanhTien AS (CAST(SoLuong * DonGia * (1.0 - ChietKhau / 100.0) AS DECIMAL(18, 2))) PERSISTED,
    CONSTRAINT PK_CHI_TIET_DON_HANG PRIMARY KEY (MaDonHang, MaSP),
    CONSTRAINT FK_CTDH_DON_HANG FOREIGN KEY (MaDonHang) 
        REFERENCES DON_HANG(MaDonHang) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_CTDH_SAN_PHAM FOREIGN KEY (MaSP) 
        REFERENCES SAN_PHAM(MaSP) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT CK_CTDH_SoLuong CHECK (SoLuong > 0),
    CONSTRAINT CK_CTDH_DonGia CHECK (DonGia >= 0),
    CONSTRAINT CK_CTDH_ChietKhau CHECK (ChietKhau >= 0 AND ChietKhau <= 100)
);
GO

-- Bảng 9: HOA_DON (Mối kết hợp 1-1 với DON_HANG xác nhận thanh toán tài chính)
CREATE TABLE HOA_DON (
    MaHoaDon VARCHAR(20) NOT NULL,
    MaDonHang VARCHAR(20) NOT NULL,
    NgayLap DATETIME NOT NULL DEFAULT GETDATE(),
    SoTienThanhToan DECIMAL(18, 2) NOT NULL,
    HinhThucThanhToan NVARCHAR(50) NOT NULL,
    TrangThaiThanhToan NVARCHAR(30) NOT NULL DEFAULT N'Đã thanh toán',
    MaGiaoDichNganHang VARCHAR(50) NULL,
    CONSTRAINT PK_HOA_DON PRIMARY KEY (MaHoaDon),
    CONSTRAINT UQ_HOA_DON_MaDonHang UNIQUE (MaDonHang), -- Đảm bảo quan hệ 1 - 1
    CONSTRAINT FK_HOA_DON_DON_HANG FOREIGN KEY (MaDonHang) 
        REFERENCES DON_HANG(MaDonHang) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT CK_HD_SoTien CHECK (SoTienThanhToan >= 0),
    CONSTRAINT CK_HD_TrangThai CHECK (TrangThaiThanhToan IN (N'Đã thanh toán', N'Chưa thanh toán', N'Đã hoàn tiền'))
);
GO

-- Bảng 10: DANH_GIA_SAN_PHAM (Đánh giá và nhận xét sản phẩm từ khách hàng)
CREATE TABLE DANH_GIA_SAN_PHAM (
    MaDanhGia VARCHAR(20) NOT NULL,
    MaSP VARCHAR(20) NOT NULL,
    MaKH VARCHAR(20) NOT NULL,
    DiemDanhGia INT NOT NULL,
    BinhLuan NVARCHAR(500) NULL,
    NgayDanhGia DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_DANH_GIA PRIMARY KEY (MaDanhGia),
    CONSTRAINT FK_DANH_GIA_SAN_PHAM FOREIGN KEY (MaSP) 
        REFERENCES SAN_PHAM(MaSP) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_DANH_GIA_KHACH_HANG FOREIGN KEY (MaKH) 
        REFERENCES KHACH_HANG(MaKH) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT CK_DG_Diem CHECK (DiemDanhGia BETWEEN 1 AND 5)
);
GO

-- ============================================================================
-- 3. TẠO INDEXES TỐI ƯU HÓA TRUY VẤN
-- ============================================================================
CREATE NONCLUSTERED INDEX IX_SAN_PHAM_DanhMuc ON SAN_PHAM(MaDanhMuc);
CREATE NONCLUSTERED INDEX IX_SAN_PHAM_NCC ON SAN_PHAM(MaNCC);
CREATE NONCLUSTERED INDEX IX_DON_HANG_KhachHang ON DON_HANG(MaKH);
CREATE NONCLUSTERED INDEX IX_DON_HANG_NgayDat ON DON_HANG(NgayDat);
CREATE NONCLUSTERED INDEX IX_CHI_TIET_DON_HANG_SP ON CHI_TIET_DON_HANG(MaSP);
CREATE NONCLUSTERED INDEX IX_DANH_GIA_SP ON DANH_GIA_SAN_PHAM(MaSP);
GO

PRINT N'>>> Đã khởi tạo hoàn tất cấu trúc Cơ sở dữ liệu TechStoreDB với đầy đủ các bảng và ràng buộc toàn vẹn!';
GO

