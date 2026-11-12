"""
Script vẽ sơ đồ Mô hình Quan hệ (Relational Schema Diagram) cho Hệ thống TechStore
Hiển thị rõ ràng các bảng, danh sách thuộc tính, khóa chính (gạch chân đỏ) và mũi tên khóa ngoại (FK).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_relational_schema():
    fig, ax = plt.subplots(figsize=(20, 13), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#F1F5F9')
    ax.set_facecolor('#F1F5F9')
    
    # Title
    ax.text(50, 97, "LƯỢC ĐỒ CƠ SỞ DỮ LIỆU QUAN HỆ (RELATIONAL SCHEMA) - TECHSTORE", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A', fontname='Arial')
    ax.text(50, 94.5, "Mô hình quan hệ sau khi chuẩn hóa đạt chuẩn BCNF (Boyce-Codd Normal Form)", 
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#475569', fontname='Arial')

    header_color = '#1E293B'
    table_bg = '#FFFFFF'
    border_color = '#94A3B8'
    
    def draw_table(x, y, w, name, columns):
        h_header = 3.0
        h_row = 1.6
        total_h = h_header + len(columns) * h_row
        
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.3, y - total_h - 0.3), w, total_h, 
                                        boxstyle="round,pad=0.2", facecolor='#CBD5E1', edgecolor='none', zorder=1)
        ax.add_patch(shadow)
        
        # Body
        body = patches.FancyBboxPatch((x, y - total_h), w, total_h, 
                                      boxstyle="round,pad=0.2", facecolor=table_bg, edgecolor=border_color, linewidth=1.2, zorder=2)
        ax.add_patch(body)
        
        # Header box
        header = patches.FancyBboxPatch((x, y - h_header), w, h_header, 
                                        boxstyle="round,pad=0.2", facecolor=header_color, edgecolor=border_color, linewidth=1, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y - h_header/2, name, color='#FFFFFF', fontsize=9.5, fontweight='bold', 
                ha='center', va='center', zorder=4, fontname='Arial')
        
        # Rows
        for i, col in enumerate(columns):
            row_y = y - h_header - (i + 0.5) * h_row
            is_pk = '(PK)' in col
            is_fk = '(FK)' in col
            col_name = col.replace('(PK)', '').replace('(FK)', '').strip()
            
            # Key indicator
            if is_pk and is_fk:
                key_txt = 'PK,FK'
                key_color = '#DC2626'
            elif is_pk:
                key_txt = 'PK'
                key_color = '#DC2626'
            elif is_fk:
                key_txt = 'FK'
                key_color = '#0284C7'
            else:
                key_txt = ''
                key_color = '#64748B'
                
            if key_txt:
                ax.text(x + 1.2, row_y, key_txt, color=key_color, fontsize=7, fontweight='bold', ha='left', va='center', zorder=4)
            
            # Column text
            fw = 'bold' if is_pk else 'normal'
            txt_color = '#0F172A' if is_pk else '#334155'
            ax.text(x + 4.5, row_y, col_name, color=txt_color, fontsize=7.5, fontweight=fw, ha='left', va='center', zorder=4)
            
            # Underline for PK
            if is_pk:
                ax.plot([x + 4.5, x + 4.5 + len(col_name)*0.55], [row_y - 0.55, row_y - 0.55], color='#DC2626', linewidth=1, zorder=4)
                
            # Divider line between rows
            if i < len(columns) - 1:
                ax.plot([x + 0.5, x + w - 0.5], [row_y - h_row/2, row_y - h_row/2], color='#E2E8F0', linewidth=0.6, zorder=3)
                
        return {'top': y, 'bottom': y - total_h, 'left': x, 'right': x + w, 'center_x': x + w/2, 'center_y': y - total_h/2}

    # Draw 10 Tables
    # Col 1: DANH_MUC, NHA_CUNG_CAP, KHACH_HANG
    t_dm = draw_table(4, 90, 16, "DANH_MUC", ["(PK) MaDanhMuc", "TenDanhMuc", "MoTa", "TrangThai"])
    t_ncc = draw_table(4, 70, 16, "NHA_CUNG_CAP", ["(PK) MaNCC", "TenNCC", "NguoiLienHe", "SoDienThoai", "Email", "DiaChi", "TrangThaiHoptac"])
    t_kh = draw_table(4, 43, 17, "KHACH_HANG", ["(PK) MaKH", "HoTen", "Email", "SoDienThoai", "DiaChi", "NgayDangKy", "MatKhauHash", "Salt", "TongChiTieu", "HangThanhVien", "TrangThaiTaiKhoan"])

    # Col 2: SAN_PHAM, DANH_GIA_SAN_PHAM
    t_sp = draw_table(26, 90, 18, "SAN_PHAM", ["(PK) MaSP", "TenSP", "(FK) MaDanhMuc", "(FK) MaNCC", "GiaNhap", "GiaBan", "SoLuongTon", "DonViTinh", "MoTa", "TrangThai"])
    t_dg = draw_table(26, 45, 18, "DANH_GIA_SAN_PHAM", ["(PK) MaDanhGia", "(FK) MaSP", "(FK) MaKH", "DiemDanhGia", "BinhLuan", "NgayDanhGia"])

    # Col 3: CHI_TIET_DON_HANG, DON_HANG, HOA_DON
    t_ctdh = draw_table(50, 90, 18, "CHI_TIET_DON_HANG", ["(PK)(FK) MaDonHang", "(PK)(FK) MaSP", "SoLuong", "DonGia", "ChietKhau", "ThanhTien"])
    t_dh = draw_table(50, 62, 18, "DON_HANG", ["(PK) MaDonHang", "(FK) MaKH", "(FK) MaNV", "NgayDat", "TongTien", "PhuongThucTT", "TrangThaiDonHang", "DiaChiGiaoHang", "GhiChu"])
    t_hd = draw_table(50, 26, 18, "HOA_DON", ["(PK) MaHoaDon", "(FK) MaDonHang", "NgayLap", "SoTienThanhToan", "HinhThucThanhToan", "TrangThaiThanhToan", "MaGiaoDichNganHang"])

    # Col 4: VAI_TRO, NHAN_VIEN
    t_vt = draw_table(76, 90, 18, "VAI_TRO", ["(PK) MaVaiTro", "TenVaiTro", "MoTa", "CapDoTruyCap"])
    t_nv = draw_table(76, 68, 19, "NHAN_VIEN", ["(PK) MaNV", "HoTen", "Email", "SoDienThoai", "ChucVu", "LuongCoBan", "NgayVaoLam", "(FK) MaVaiTro", "(FK) MaQuanLy", "MatKhauHash", "Salt", "TrangThai"])

    # Draw FK Connecting Arrows
    def draw_fk_arrow(start_pt, end_pt, label=""):
        ax.annotate("", xy=end_pt, xytext=start_pt,
                    arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=10), zorder=5)

    # DANH_MUC -> SAN_PHAM
    draw_fk_arrow((t_dm['right'], t_dm['top'] - 4.5), (t_sp['left'], t_sp['top'] - 6.5))
    # NHA_CUNG_CAP -> SAN_PHAM
    draw_fk_arrow((t_ncc['right'], t_ncc['top'] - 4.5), (t_sp['left'], t_sp['top'] - 8.0))
    # SAN_PHAM -> CHI_TIET_DON_HANG
    draw_fk_arrow((t_sp['right'], t_sp['top'] - 4.5), (t_ctdh['left'], t_ctdh['top'] - 6.5))
    # DON_HANG -> CHI_TIET_DON_HANG
    draw_fk_arrow((t_dh['center_x'], t_dh['top']), (t_ctdh['center_x'], t_ctdh['bottom']))
    # KHACH_HANG -> DON_HANG
    draw_fk_arrow((t_kh['right'], t_kh['top'] - 4.5), (t_dh['left'], t_dh['top'] - 5.0))
    # DON_HANG -> HOA_DON
    draw_fk_arrow((t_dh['center_x'], t_dh['bottom']), (t_hd['center_x'], t_hd['top']))
    # VAI_TRO -> NHAN_VIEN
    draw_fk_arrow((t_vt['center_x'], t_vt['bottom']), (t_nv['center_x'], t_nv['top']))
    # NHAN_VIEN -> DON_HANG
    draw_fk_arrow((t_nv['left'], t_nv['top'] - 12.0), (t_dh['right'], t_dh['top'] - 6.5))
    # SAN_PHAM -> DANH_GIA
    draw_fk_arrow((t_sp['center_x'], t_sp['bottom']), (t_dg['center_x'], t_dg['top']))
    # KHACH_HANG -> DANH_GIA
    draw_fk_arrow((t_kh['right'], t_kh['top'] - 14.0), (t_dg['left'], t_dg['top'] - 6.5))

    plt.tight_layout()
    plt.savefig('d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/Relational_Schema_TechStore.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    print(">>> Đã xuất file Relational_Schema_TechStore.png chất lượng 300 DPI thành công!")

if __name__ == '__main__':
    draw_relational_schema()
