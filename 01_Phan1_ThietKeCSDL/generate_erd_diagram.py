"""
Script vẽ sơ đồ ERD và Sơ đồ Mô hình Quan hệ (Relational Schema) cho Hệ thống TechStore
Sử dụng matplotlib với chất lượng 300 DPI cực kỳ sắc nét để chèn vào Báo cáo và Slides.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_erd_diagram():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    
    # Title
    ax.text(50, 97, "SƠ ĐỒ THỰC THỂ - LIÊN KẾT (ERD) - HỆ THỐNG TECHSTORE", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#0F172A', fontname='Arial')
    ax.text(50, 94.5, "Môn học: Cơ sở dữ liệu | Đề tài: Hệ thống Quản lý Bán hàng Thương mại Điện tử", 
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#475569', fontname='Arial')

    # Color palette
    entity_color = '#1E3A8A'      # Deep Blue
    entity_text = '#FFFFFF'
    rel_color = '#0284C7'         # Light Blue
    rel_text = '#FFFFFF'
    attr_color = '#F1F5F9'        # Soft grey
    border_color = '#334155'
    
    # Helper to draw Entity (Rectangle)
    def draw_entity(x, y, w, h, name, attrs=None):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5",
                                      facecolor=entity_color, edgecolor='#0F172A', linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 2, name, color=entity_text, fontsize=11, fontweight='bold', 
                ha='center', va='center', zorder=4, fontname='Arial')
        if attrs:
            # draw attribute box below
            attr_box = patches.FancyBboxPatch((x, y - len(attrs)*1.8 - 0.5), w, len(attrs)*1.8 + 0.5, 
                                              boxstyle="round,pad=0.2", facecolor=attr_color, 
                                              edgecolor=border_color, linewidth=1, zorder=2)
            ax.add_patch(attr_box)
            for i, attr in enumerate(attrs):
                is_pk = attr.startswith('*')
                is_fk = attr.startswith('#')
                disp_attr = attr.lstrip('*#')
                fw = 'bold' if is_pk else 'normal'
                col = '#DC2626' if is_pk else ('#0284C7' if is_fk else '#1E293B')
                prefix = '(PK) ' if is_pk else ('(FK) ' if is_fk else ' - ')
                ax.text(x + 1, y - 1.2 - i*1.8, prefix + disp_attr, color=col, fontsize=7.5,
                        fontweight=fw, ha='left', va='center', zorder=4, fontname='Arial')

    # Helper to draw Relationship (Diamond)
    def draw_diamond(cx, cy, r, name):
        pts = [(cx, cy + r), (cx + r*1.3, cy), (cx, cy - r), (cx - r*1.3, cy)]
        poly = patches.Polygon(pts, facecolor=rel_color, edgecolor='#0369A1', linewidth=1.5, zorder=3)
        ax.add_patch(poly)
        ax.text(cx, cy, name, color=rel_text, fontsize=8, fontweight='bold', ha='center', va='center', zorder=4, fontname='Arial')

    # Helper to draw connector lines
    def draw_line(p1, p2, card1="", card2=""):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#334155', linewidth=1.5, zorder=1)
        if card1:
            ax.text(p1[0], p1[1], card1, fontsize=9, fontweight='bold', color='#B91C1C', zorder=5)
        if card2:
            ax.text(p2[0], p2[1], card2, fontsize=9, fontweight='bold', color='#B91C1C', zorder=5)

    # 1. DANH_MUC (Top-Left)
    draw_entity(5, 78, 16, 4, "DANH_MUC", ["*MaDanhMuc", "TenDanhMuc", "MoTa", "TrangThai"])
    
    # 2. NHA_CUNG_CAP (Top-Center)
    draw_entity(30, 78, 16, 4, "NHA_CUNG_CAP", ["*MaNCC", "TenNCC", "NguoiLienHe", "SoDienThoai", "Email", "DiaChi"])

    # 3. SAN_PHAM (Center-Top)
    draw_entity(18, 52, 17, 4, "SAN_PHAM", ["*MaSP", "TenSP", "#MaDanhMuc", "#MaNCC", "GiaNhap", "GiaBan", "SoLuongTon", "DonViTinh", "TrangThai"])

    # Relationships DANH_MUC - SAN_PHAM
    draw_diamond(13, 67, 2.5, "Phân loại")
    draw_line((13, 78), (13, 69.5), card1=" 1", card2="")
    draw_line((13, 64.5), (20, 56), card1="", card2=" N")

    # Relationships NHA_CUNG_CAP - SAN_PHAM
    draw_diamond(34, 67, 2.5, "Cung cấp")
    draw_line((36, 78), (34, 69.5), card1=" 1", card2="")
    draw_line((34, 64.5), (32, 56), card1="", card2=" N")

    # 4. KHACH_HANG (Left-Bottom)
    draw_entity(5, 20, 18, 4, "KHACH_HANG", ["*MaKH", "HoTen", "Email", "SoDienThoai", "DiaChi", "NgayDangKy", "MatKhauHash", "TongChiTieu", "HangThanhVien"])

    # 5. VAI_TRO (Right-Top)
    draw_entity(78, 78, 16, 4, "VAI_TRO", ["*MaVaiTro", "TenVaiTro", "MoTa", "CapDoTruyCap"])

    # 6. NHAN_VIEN (Right-Center)
    draw_entity(77, 48, 18, 4, "NHAN_VIEN", ["*MaNV", "HoTen", "Email", "SoDienThoai", "ChucVu", "LuongCoBan", "#MaVaiTro", "#MaQuanLy", "TrangThai"])

    # Relationship VAI_TRO - NHAN_VIEN
    draw_diamond(85, 66, 2.5, "Phân quyền")
    draw_line((85, 78), (85, 68.5), card1=" 1", card2="")
    draw_line((85, 63.5), (85, 52), card1="", card2=" N")

    # Recursive NHAN_VIEN - NHAN_VIEN
    ax.annotate("", xy=(95, 50), xytext=(97, 44),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, connectionstyle="arc3,rad=-0.7"))
    ax.text(99, 47, "Quản lý\n(1-N)", fontsize=7.5, color='#0284C7', fontweight='bold')

    # 7. DON_HANG (Center)
    draw_entity(46, 32, 18, 4, "DON_HANG", ["*MaDonHang", "#MaKH", "#MaNV", "NgayDat", "TongTien", "PhuongThucTT", "TrangThai", "DiaChiGiaoHang"])

    # Relationship KHACH_HANG - DON_HANG
    draw_diamond(30, 24, 2.5, "Đặt mua")
    draw_line((23, 22), (27.5, 24), card1=" 1", card2="")
    draw_line((32.5, 24), (46, 33), card1="", card2=" N")

    # Relationship NHAN_VIEN - DON_HANG
    draw_diamond(69, 36, 2.5, "Xử lý")
    draw_line((77, 49), (71.5, 37.5), card1=" 1", card2="")
    draw_line((66.5, 34.5), (64, 34), card1="", card2=" N")

    # 8. CHI_TIET_DON_HANG (Center-Between DON_HANG and SAN_PHAM)
    draw_entity(47, 56, 17, 3.5, "CHI_TIET_DON_HANG", ["*#MaDonHang", "*#MaSP", "SoLuong", "DonGia", "ChietKhau", "ThanhTien"])
    draw_line((35, 54), (47, 57), card1="1", card2="N")
    draw_line((55, 36), (55, 47), card1="1", card2="N")

    # 9. HOA_DON (Bottom-Center)
    draw_entity(46, 8, 18, 4, "HOA_DON", ["*MaHoaDon", "#MaDonHang", "NgayLap", "SoTienThanhToan", "HinhThucTT", "TrangThaiTT", "MaGiaoDich"])
    draw_diamond(55, 19, 2.2, "Thanh toán")
    draw_line((55, 32), (55, 21.2), card1=" 1", card2="")
    draw_line((55, 16.8), (55, 12), card1="", card2=" 1 (1-1)")

    # 10. DANH_GIA_SAN_PHAM (Bottom-Left)
    draw_entity(20, 3, 18, 3.5, "DANH_GIA_SAN_PHAM", ["*MaDanhGia", "#MaSP", "#MaKH", "DiemDanhGia", "BinhLuan", "NgayDanhGia"])
    draw_line((12, 10), (20, 5), card1="1", card2="N")
    draw_line((22, 38), (22, 6.5), card1="1", card2="N")

    # Legend
    leg_x, leg_y = 75, 5
    leg_box = patches.FancyBboxPatch((leg_x, leg_y), 22, 13, boxstyle="round,pad=0.5",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1, zorder=5)
    ax.add_patch(leg_box)
    ax.text(leg_x + 11, leg_y + 11.5, "CHÚ THÍCH KÝ HIỆU", fontsize=9, fontweight='bold', ha='center', color='#0F172A')
    
    # Legend items
    ax.add_patch(patches.Rectangle((leg_x + 1, leg_y + 8.5), 3, 1.8, facecolor=entity_color, edgecolor='#0F172A'))
    ax.text(leg_x + 5, leg_y + 9.4, "Thực thể (Entity)", fontsize=8, va='center')

    poly_leg = patches.Polygon([(leg_x + 2.5, leg_y + 7.5), (leg_x + 4, leg_y + 6.5), 
                                (leg_x + 2.5, leg_y + 5.5), (leg_x + 1, leg_y + 6.5)], facecolor=rel_color, edgecolor='#0369A1')
    ax.add_patch(poly_leg)
    ax.text(leg_x + 5, leg_y + 6.5, "Mối kết hợp (Relationship)", fontsize=8, va='center')

    ax.text(leg_x + 1.5, leg_y + 4, "(PK)", color='#DC2626', fontsize=8, fontweight='bold')
    ax.text(leg_x + 5, leg_y + 4, "Khóa chính (Primary Key)", fontsize=8, va='center')

    ax.text(leg_x + 1.5, leg_y + 1.8, "(FK)", color='#0284C7', fontsize=8, fontweight='bold')
    ax.text(leg_x + 5, leg_y + 1.8, "Khóa ngoại (Foreign Key)", fontsize=8, va='center')

    plt.tight_layout()
    plt.savefig('d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/ERD_TechStore.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    print(">>> Đã xuất file ERD_TechStore.png chất lượng 300 DPI thành công!")

if __name__ == '__main__':
    draw_erd_diagram()
