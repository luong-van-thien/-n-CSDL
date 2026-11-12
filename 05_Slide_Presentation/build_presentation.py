"""
Script tự động sinh Slide thuyết trình PowerPoint (.pptx) chuẩn đồ án chuyên nghiệp
Môn học: Cơ sở dữ liệu | Đề tài: Hệ thống TechStore & Chuyên đề Chương 30: Database Security
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette
    C_BG_DARK = RGBColor(11, 15, 25)        # #0B0F19
    C_CARD_BG = RGBColor(21, 28, 44)        # #151C2C
    C_CARD_BORDER = RGBColor(51, 65, 85)    # #334155
    C_PRIMARY = RGBColor(59, 130, 246)      # #3B82F6
    C_SECONDARY = RGBColor(14, 165, 233)    # #0EA5E9
    C_ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444
    C_ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981
    C_TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
    C_TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="ĐỒ ÁN MÔN HỌC CƠ SỞ DỮ LIỆU"):
        # Category small
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_PRIMARY

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_WHITE

    def add_card(slide, left, top, width, height, title="", items=None, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.name = "Arial"
            p0.font.size = Pt(16)
            p0.font.bold = True
            p0.font.color.rgb = C_SECONDARY
            p0.space_after = Pt(10)

        if items:
            for i, itm in enumerate(items):
                p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
                p.text = "• " + itm
                p.font.name = "Arial"
                p.font.size = Pt(13)
                p.font.color.rgb = C_TEXT_WHITE
                p.space_after = Pt(8)

        return card

    # =========================================================================
    # SLIDE 1: BÌA BÁO CÁO (TITLE SLIDE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # University header
    u_box = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    tf_u = u_box.text_frame
    p_u1 = tf_u.paragraphs[0]
    p_u1.text = "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG - CƠ SỞ TP.HCM"
    p_u1.font.name = "Arial"
    p_u1.font.size = Pt(14)
    p_u1.font.bold = True
    p_u1.font.color.rgb = C_TEXT_MUTED

    p_u2 = tf_u.add_paragraph()
    p_u2.text = "KHOA CÔNG NGHỆ THÔNG TIN | BỘ MÔN HỆ THỐNG THÔNG TIN"
    p_u2.font.name = "Arial"
    p_u2.font.size = Pt(12)
    p_u2.font.color.rgb = C_PRIMARY

    # Main Title Box
    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(2.2))
    tf_main = title_box.text_frame
    tf_main.word_wrap = True
    p_m1 = tf_main.paragraphs[0]
    p_m1.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU"
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(32)
    p_m1.font.bold = True
    p_m1.font.color.rgb = C_TEXT_WHITE

    p_m2 = tf_main.add_paragraph()
    p_m2.text = "Phần 1: Thiết Kế & Cài Đặt Hệ Thống CSDL TechStore (Chuẩn BCNF)"
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(18)
    p_m2.font.bold = True
    p_m2.font.color.rgb = C_SECONDARY
    p_m2.space_before = Pt(10)

    p_m3 = tf_main.add_paragraph()
    p_m3.text = "Phần 2: Nghiên Cứu Chuyên Sâu Chương 30 - Database Security & Lab Thực Nghiệm"
    p_m3.font.name = "Arial"
    p_m3.font.size = Pt(18)
    p_m3.font.bold = True
    p_m3.font.color.rgb = C_ACCENT_GREEN
    p_m3.space_before = Pt(4)

    # Info card
    add_card(s1, Inches(1.0), Inches(4.7), Inches(11.3), Inches(2.0),
             title="THÔNG TIN THỰC HIỆN",
             items=[
                 "Giảng viên hướng dẫn: ThS. Tuyết Hải (tuyethai@ptithcm.edu.vn)",
                 "Nhóm sinh viên thực hiện: N24DCCN076 & Các thành viên trong nhóm",
                 "Học kỳ: HK1 (2025 - 2026) | Ngày báo cáo: Tháng 11/2026",
                 "GitHub Demo Repository: https://github.com/TechStore-DB/Database-Security-Project"
             ])

    # =========================================================================
    # SLIDE 2: NỘI DUNG TRÌNH BÀY (AGENDA)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "NỘI DUNG TỔNG QUAN BÀI BÁO CÁO")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="PHẦN 1: THIẾT KẾ CSDL TECHSTORE",
             items=[
                 "Khảo sát nghiệp vụ & Mô tả bài toán",
                 "Mô hình Thực thể - Liên kết (ERD 10 thực thể)",
                 "Quy tắc ánh xạ 7 bước sang Mô hình quan hệ",
                 "Phân tích & Chứng minh chuẩn hóa đạt BCNF",
                 "Cài đặt CSDL trên Microsoft SQL Server",
                 "Bộ sưu tập 25+ câu truy vấn DQL, View, Stored Procedure và Trigger nghiệp vụ"
             ])

    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="PHẦN 2 & 3: CHƯƠNG 30 & DEMO BẢO MẬT",
             items=[
                 "Tổng quan An ninh CSDL & Tam giác CIA",
                 "Kiểm soát truy cập tùy biến (DAC) & SQL Privileges",
                 "Kiểm soát truy cập bắt buộc (MAC) & Bell-LaPadula",
                 "Mô hình phân quyền theo vai trò (RBAC)",
                 "Lỗ hổng SQL Injection & Kỹ thuật phòng thủ",
                 "Mã hóa CSDL, Băm mật khẩu (SHA-256 + Salt) & DDM",
                 "Demo trực quan: Phòng thí nghiệm An ninh CSDL"
             ])

    # =========================================================================
    # SLIDE 3: BỐI CẢNH & KHẢO SÁT NGHIỆP VỤ TECHSTORE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "BỐI CẢNH & QUY TẮC NGHIỆP VỤ HỆ THỐNG TECHSTORE")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Chuỗi Cung Ứng & Hàng Hóa",
             items=[
                 "Hệ thống kinh doanh thiết bị công nghệ: Laptop, Smartphone, Tablet, Phụ kiện.",
                 "Một Danh mục có nhiều Sản phẩm (1-N).",
                 "Một Nhà cung cấp cung ứng nhiều Sản phẩm (1-N).",
                 "Ràng buộc nghiệp vụ: Giá bán >= Giá nhập, Số lượng tồn >= 0."
             ])

    add_card(s3, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Khách Hàng & Giao Dịch",
             items=[
                 "Khách hàng đăng ký tài khoản với Email và SĐT duy nhất (UNIQUE).",
                 "Mật khẩu băm an toàn SHA-256 kèm chuỗi Salt ngẫu nhiên.",
                 "Một Khách hàng đặt nhiều Đơn hàng (1-N).",
                 "Một Đơn hàng gồm nhiều Sản phẩm (N-N) thông qua CHI_TIET_DON_HANG.",
                 "Hóa đơn thanh toán phát hành 1-1 với đơn hoàn tất."
             ])

    add_card(s3, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Nhân Sự & Phân Quyền",
             items=[
                 "Cơ cấu tổ chức nhân sự phân cấp đệ quy (Recursive: MaQuanLy -> MaNV).",
                 "Nhân viên được gán Vai trò (VAI_TRO) tương ứng chức vụ.",
                 "Cơ chế RBAC kiểm soát quyền: Admin, Manager, Sales Staff, Warehouse Staff.",
                 "Tự động tính chi tiêu và thăng hạng thành viên (Loyalty Tiers)."
             ])

    # =========================================================================
    # SLIDE 4: SƠ ĐỒ THỰC THỂ - LIÊN KẾT (ERD)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "MÔ HÌNH THỰC THỂ - LIÊN KẾT (ERD) HỆ THỐNG TECHSTORE")

    # Insert ERD image
    erd_img_path = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/ERD_TechStore.png"
    if os.path.exists(erd_img_path):
        s4.shapes.add_picture(erd_img_path, Inches(0.8), Inches(1.6), width=Inches(8.5))
    
    add_card(s4, Inches(9.6), Inches(1.6), Inches(3.0), Inches(5.3),
             title="Điểm Nổi Bật ERD",
             items=[
                 "10 Thực thể hoàn chỉnh bao quát toàn bộ quy trình E-Commerce.",
                 "Quan hệ 1-1: DON_HANG - HOA_DON.",
                 "Quan hệ 1-N: DANH_MUC -> SAN_PHAM, KHACH_HANG -> DON_HANG.",
                 "Quan hệ N-N: SAN_PHAM & DON_HANG qua CHI_TIET_DON_HANG.",
                 "Quan hệ đệ quy: NHAN_VIEN tự quản lý (1-N)."
             ])

    # =========================================================================
    # SLIDE 5: LƯỢC ĐỒ QUAN HỆ & CHUẨN HÓA BCNF
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "LƯỢC ĐỒ QUAN HỆ & PHÂN TÍCH CHUẨN HÓA BCNF")

    schema_img_path = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/Relational_Schema_TechStore.png"
    if os.path.exists(schema_img_path):
        s5.shapes.add_picture(schema_img_path, Inches(0.8), Inches(1.6), width=Inches(8.5))

    add_card(s5, Inches(9.6), Inches(1.6), Inches(3.0), Inches(5.3),
             title="Chứng Minh BCNF",
             items=[
                 "1NF: Tất cả thuộc tính đều chứa giá trị nguyên tố (Atomic values).",
                 "2NF: Không có phụ thuộc hàm bộ phận vào bộ phận của khóa chính.",
                 "3NF: Triệt tiêu hoàn toàn các phụ thuộc bắc cầu.",
                 "BCNF: Mọi vế trái X của phụ thuộc hàm X -> Y đều là Siêu khóa (Superkey).",
                 "Không có bất thường thêm, xóa, sửa hay dư thừa."
             ])

    # =========================================================================
    # SLIDE 6: CÀI ĐẶT CSDL SQL SERVER & TRUY VẤN TIÊU BIỂU
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "CÀI ĐẶT TRÊN SQL SERVER & TÍNH NĂNG NÂNG CAO")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Ràng Buộc Toàn Vẹn",
             items=[
                 "PRIMARY KEY & FOREIGN KEY với ON DELETE / ON UPDATE linh hoạt.",
                 "CHECK ràng buộc giá: GiaBan >= GiaNhap, SoLuongTon >= 0.",
                 "CHECK định dạng: Email LIKE '%_@__%.__%'.",
                 "UNIQUE cho Email, SĐT Khách hàng và Nhà cung cấp.",
                 "DEFAULT ngày tạo (GETDATE()), trạng thái kích hoạt."
             ])

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Bộ Truy Vấn DQL Đa Dạng",
             items=[
                 "Truy vấn nối: INNER JOIN 4 bảng, LEFT JOIN khách chưa mua hàng, SELF JOIN cây nhân sự.",
                 "Gom nhóm: GROUP BY & HAVING tính doanh thu trên 40 triệu.",
                 "Truy vấn lồng: IN, NOT IN, EXISTS, Correlated Subquery.",
                 "Window Functions: DENSE_RANK() xếp hạng sản phẩm bán chạy theo từng danh mục."
             ])

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Lập Trình Thủ Tục T-SQL",
             items=[
                 "View: vw_HieuSuatKinhDoanhSanPham, vw_LichSuMuaHangKhachHang.",
                 "Function: fn_XepHangThanhVien tự động thăng hạng khách hàng.",
                 "Stored Procedure: sp_TaoDonHangMoi kiểm tra tồn kho, dùng TRANSACTION đảm bảo ACID.",
                 "Trigger: trg_CapNhatTongChiTieuKH tự động đồng bộ khi đơn Hoàn thành."
             ])

    # =========================================================================
    # SLIDE 7: PHẦN 2 - CHƯƠNG 30: TỔNG QUAN AN NINH CSDL (CIA TRIAD)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "CHƯƠNG 30: TỔNG QUAN BẢO MẬT CƠ SỞ DỮ LIỆU & TAM GIÁC CIA", category="NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Tính Bảo Mật (Confidentiality)",
             items=[
                 "Ngăn chặn việc lộ lọt dữ liệu cho các bên không có thẩm quyền.",
                 "Bảo vệ dữ liệu bí mật: Thông tin cá nhân (PII), mật khẩu, số thẻ ngân hàng, bảng lương.",
                 "Các biện pháp kỹ thuật: Mã hóa đường truyền SSL/TLS, mã hóa dữ liệu tĩnh (TDE), che dữ liệu nhạy cảm (Data Masking)."
             ], border_color=C_PRIMARY)

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Tính Toàn Vẹn (Integrity)",
             items=[
                 "Đảm bảo dữ liệu chính xác, không bị sửa đổi, chèn ép hoặc xóa trái phép.",
                 "Ràng buộc toàn vẹn CSDL (PK, FK, CHECK, Trigger).",
                 "Cơ chế Giao dịch (ACID Transactions) chống lỗi nửa vời.",
                 "Kiểm toán CSDL (Audit Trail) lưu vết mọi hành vi thay đổi cấu trúc và dữ liệu."
             ], border_color=C_ACCENT_GREEN)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Tính Sẵn Sàng (Availability)",
             items=[
                 "Đảm bảo hệ thống CSDL luôn phục vụ người dùng hợp pháp khi cần thiết.",
                 "Phòng chống các đòn tấn công từ chối dịch vụ (DoS / DDoS) gây cạn kiệt tài nguyên máy chủ.",
                 "Giải pháp hạ tầng: Backup định kỳ, Sao chép (Replication), High Availability (Always On Clustering)."
             ], border_color=C_SECONDARY)

    # =========================================================================
    # SLIDE 8: CƠ CHẾ KIỂM SOÁT TRUY CẬP: DAC VS MAC VS RBAC
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "SO SÁNH MÔ HÌNH KIỂM SOÁT TRUY CẬP: DAC, MAC VÀ RBAC", category="NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="1. DAC (Discretionary)",
             items=[
                 "Dựa trên quyền sở hữu (Ownership).",
                 "Chủ sở hữu tự ý cấp quyền (GRANT) hoặc thu hồi (REVOKE) cho đối tượng.",
                 "Hỗ trợ WITH GRANT OPTION (ủy quyền phân cấp).",
                 "Thu hồi theo cây quyền hạn (CASCADE hoặc RESTRICT).",
                 "Rất linh hoạt, phổ biến trong thương mại nhưng dễ bị lạm quyền."
             ])

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="2. MAC (Mandatory)",
             items=[
                 "Quy định nghiêm ngặt bởi chính sách an ninh toàn hệ thống.",
                 "Mô hình Bell-LaPadula: Top Secret > Secret > Confidential > Unclassified.",
                 "Nguyên tắc 'No Read Up': Người cấp thấp không được đọc tin cấp cao.",
                 "Nguyên tắc 'No Write Down': Người cấp cao không ghi đè xuống cấp thấp.",
                 "Hiện tượng đa thể hiện (Polyinstantiation)."
             ])

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="3. RBAC (Role-Based)",
             items=[
                 "Quyền hạn được gán vào Vai trò (Role) thay vì từng người dùng.",
                 "Người dùng được cấp các vai trò phù hợp với công việc.",
                 "Phân cấp vai trò (Role Hierarchy): Quản lý kế thừa quyền nhân viên.",
                 "Phân tách nhiệm vụ (Separation of Duties - SoD) chống xung đột lợi ích.",
                 "Chuẩn mực bảo mật của các RDBMS doanh nghiệp."
             ])

    # =========================================================================
    # SLIDE 9: LỖ HỔNG SQL INJECTION & KỸ THUẬT PHÒNG THỦ
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "LỖ HỔNG SQL INJECTION: CƠ CHẾ, NGUY CƠ & PHÒNG THỦ", category="NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="Cơ Chế & Các Dạng Tấn Công SQLi",
             items=[
                 "Nguyên nhân: Ghép chuỗi SQL động trực tiếp từ dữ liệu người dùng (String Concatenation).",
                 "Tấn công đồng nhất thức (Tautology / Auth Bypass): Nhập ' OR '1'='1' -- để vượt qua đăng nhập không cần mật khẩu.",
                 "Tấn công trích xuất UNION: Ghép ' UNION SELECT ... để đánh cắp bảng tài khoản, thẻ ngân hàng, bảng lương.",
                 "Tấn công Piggybacked: Chèn dấu chấm phẩy ; DROP TABLE ... để phá hủy toàn bộ cơ sở dữ liệu.",
                 "Tấn công mù (Blind SQLi): Dựa vào thời gian phản hồi hoặc phản hồi nhị phân để suy luận mật khẩu."
             ], border_color=C_ACCENT_RED)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="Chiến Lược Phòng Thủ Toàn Diện",
             items=[
                 "Biện pháp số 1: Sử dụng Truy vấn Tham số hóa (Parameterized Queries / Prepared Statements) 100%.",
                 "Cơ chế: Phân tách rõ ràng mã lệnh và dữ liệu, ký tự nhập vào chỉ là chuỗi thuần túy (Literal Value).",
                 "Sử dụng các thư viện ORM tiêu chuẩn (Entity Framework, Hibernate, SQLAlchemy).",
                 "Nguyên tắc đặc quyền tối thiểu (Least Privilege): Web kết nối CSDL không dùng tài khoản 'sa'/'root'.",
                 "Kiểm tra và khử trùng dữ liệu đầu vào (Input Validation & Sanitization)."
             ], border_color=C_ACCENT_GREEN)

    # =========================================================================
    # SLIDE 10: BĂM MẬT KHẨU, MÃ HÓA CSDL & DATA MASKING
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "BĂM MẬT KHẨU, MÃ HÓA CSDL & ROW-LEVEL SECURITY", category="NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Băm Mật Khẩu (Hashing & Salt)",
             items=[
                 "Không bao giờ lưu mật khẩu dạng bản rõ (Plaintext).",
                 "Hàm băm MD5 / SHA-1 đã lỗi thời, dễ bị bẻ khóa bởi Rainbow Table.",
                 "Giải pháp chuẩn: SHA-256 kèm chuỗi Salt ngẫu nhiên duy nhất cho từng tài khoản.",
                 "Salt vô hiệu hóa bảng tra cứu trước, bảo vệ mật khẩu yếu."
             ])

    add_card(s10, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Mã Hóa CSDL & Masking",
             items=[
                 "Mã hóa đối xứng (AES-256): Mã hóa thông tin nhạy cảm (Số thẻ tín dụng, CCCD, Bệnh án).",
                 "Mã hóa bất đối xứng (RSA): Trao đổi khóa và chữ ký số an toàn.",
                 "Dynamic Data Masking (DDM): Tự động che thông tin riêng tư (Số điện thoại XXX, Email a***@gmail.com)."
             ])

    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Row-Level Security (RLS)",
             items=[
                 "Cơ chế lọc dữ liệu mức hàng ngay tại tầng Database Engine.",
                 "Sử dụng Security Predicate Function và Filter Policy.",
                 "Khách hàng chỉ xem được đơn hàng của chính mình (cô lập tuyệt đối).",
                 "Bảo mật trong suốt (Transparent), ứng dụng không cần viết thêm điều kiện WHERE."
             ])

    # =========================================================================
    # SLIDE 11: GIỚI THIỆU ỨNG DỤNG DEMO BẢO MẬT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "KIẾN TRÚC ỨNG DỤNG DEMO: TECHSTORE SECURITY LAB", category="SẢN PHẨM THỰC NGHIỆM")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Công Nghệ & Giao Diện",
             items=[
                 "Backend: Python Flask Server tốc độ cao, xử lý API linh hoạt.",
                 "Database: SQLite / T-SQL Engine mô phỏng trọn vẹn kiến trúc TechStoreDB.",
                 "Giao diện: Dashboard phong cách Dark Cyber Security hiện đại, responsive.",
                 "Khởi chạy 1-click tiện lợi qua file run_demo.bat."
             ])

    add_card(s11, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="4 Phân Hệ Thực Nghiệm",
             items=[
                 "Module 1: Thử nghiệm Tấn công SQL Injection (Bypass Đăng nhập & UNION Data Leak).",
                 "Module 2: Trực quan hóa Ma trận phân quyền vai trò (RBAC Simulator).",
                 "Module 3: Phòng thí nghiệm Băm Mật khẩu & Mã hóa AES-256.",
                 "Module 4: Kịch bản lệnh T-SQL triển khai thực tế trên SQL Server."
             ])

    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             title="Ý Nghĩa Thực Tiễn",
             items=[
                 "Minh chứng trực quan sự khác biệt giữa Code dễ bị tổn thương và Code chuẩn bảo mật.",
                 "Cung cấp các nút Quick-Payload giúp giảng viên và người xem kiểm thử ngay tức thì.",
                 "Kết nối chặt chẽ giữa lý thuyết hàn lâm Chương 30 và kỹ thuật lập trình an toàn."
             ])

    # =========================================================================
    # SLIDE 12: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "KẾT LUẬN, BÀI HỌC KINH NGHIỆM & HƯỚNG PHÁT TRIỂN")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="Kết Quả Đạt Được",
             items=[
                 "Hoàn thành xuất sắc thiết kế CSDL TechStore chuẩn BCNF với 10 thực thể chặt chẽ.",
                 "Cài đặt hoàn chỉnh trên SQL Server: 25+ truy vấn phức tạp, Procedure, Trigger và Transaction.",
                 "Nghiên cứu chuyên sâu toàn diện Chương 30 (Fundamentals of Database Systems 7E).",
                 "Xây dựng thành công ứng dụng Web Demo Cyber Security trực quan, sống động.",
                 "Đóng gói đầy đủ mã nguồn, tài liệu báo cáo chuẩn mẫu PTIT và xuất bản lên GitHub."
             ], border_color=C_ACCENT_GREEN)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             title="Hướng Phát Triển Tiếp Theo",
             items=[
                 "Tích hợp Web Application Firewall (WAF) và hệ thống phát hiện xâm nhập ModSecurity.",
                 "Nghiên cứu áp dụng Machine Learning trong việc phát hiện bất thường truy vấn CSDL (Anomaly Detection).",
                 "Triển khai kiến trúc Always Encrypted trên Microsoft SQL Server Enterprise.",
                 "Mở rộng mô hình vi dịch vụ (Microservices) với xác thực JWT và OAuth2 / OpenID Connect."
             ], border_color=C_PRIMARY)

    # =========================================================================
    # SLIDE 13: LỜI CẢM ƠN & Q&A
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)

    qa_box = s13.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.3), Inches(3.5))
    tf_qa = qa_box.text_frame
    tf_qa.word_wrap = True

    p_q1 = tf_qa.paragraphs[0]
    p_q1.text = "XIN CHÂN THÀNH CẢM ƠN CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE!"
    p_q1.font.name = "Arial"
    p_q1.font.size = Pt(28)
    p_q1.font.bold = True
    p_q1.font.color.rgb = C_TEXT_WHITE
    p_q1.alignment = PP_ALIGN.CENTER

    p_q2 = tf_qa.add_paragraph()
    p_q2.text = "Kính mong nhận được sự nhận xét và đóng góp quý báu từ Giảng viên!"
    p_q2.font.name = "Arial"
    p_q2.font.size = Pt(18)
    p_q2.font.color.rgb = C_SECONDARY
    p_q2.space_before = Pt(20)
    p_q2.alignment = PP_ALIGN.CENTER

    p_q3 = tf_qa.add_paragraph()
    p_q3.text = "PHIÊN HỎI ĐÁP (Q & A)"
    p_q3.font.name = "Arial"
    p_q3.font.size = Pt(24)
    p_q3.font.bold = True
    p_q3.font.color.rgb = C_ACCENT_GREEN
    p_q3.space_before = Pt(25)
    p_q3.alignment = PP_ALIGN.CENTER

    # Save presentation
    out_pptx = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/05_Slide_Presentation/Slide_Thuyet_Trinh_Do_An_CSDL.pptx"
    prs.save(out_pptx)
    print(f">>> Đã xuất file trình chiếu PowerPoint thành công tại: {out_pptx}")

if __name__ == '__main__':
    create_deck()
