"""
Script xây dựng Cuốn Báo Cáo Đồ Án Môn Học CSDL hoàn chỉnh, chuẩn mẫu PTIT
Môn học: Cơ sở dữ liệu | Đề tài: Hệ thống TechStore & Chuyên đề Chương 30: Database Security
Xuất ra file .docx chuyên nghiệp và tự động chuyển đổi sang .pdf bằng Microsoft Word COM API.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # 1. Page setup: Margins A4 standard (Left 3cm, Right 2cm, Top 2cm, Bottom 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)      # ~2.0 cm
        section.bottom_margin = Inches(0.8)   # ~2.0 cm
        section.left_margin = Inches(1.18)    # ~3.0 cm (đóng gáy)
        section.right_margin = Inches(0.8)    # ~2.0 cm
        section.different_first_page_header_footer = True
        
        # Header & Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU - NHÓM SINH VIÊN PTIT"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.runs[0].font.name = "Times New Roman"
        p_hdr.runs[0].font.size = Pt(9)
        p_hdr.runs[0].font.italic = True
        p_hdr.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    # Style Helpers
    def set_font(run, name="Times New Roman", size=13, bold=False, italic=False, color_rgb=(0,0,0)):
        run.font.name = name
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def set_para_spacing(p, before=0, after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.LEFT):
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = align

    def set_cell_background(cell, hex_color):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = OxmlElement(m)
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_heading_1(text):
        p = doc.add_paragraph()
        set_para_spacing(p, before=16, after=6, line_spacing=1.3)
        r = p.add_run(text)
        set_font(r, size=15, bold=True, color_rgb=(15, 23, 42))
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        set_para_spacing(p, before=12, after=4, line_spacing=1.25)
        r = p.add_run(text)
        set_font(r, size=13.5, bold=True, color_rgb=(30, 58, 138))
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        set_para_spacing(p, before=8, after=3, line_spacing=1.25)
        r = p.add_run(text)
        set_font(r, size=13, bold=True, italic=True, color_rgb=(51, 65, 85))
        return p

    def add_body(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        set_para_spacing(p, before=0, after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            set_font(rb, size=13, bold=True)
        r = p.add_run(text)
        set_font(r, size=13, italic=italic)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        set_para_spacing(p, before=0, after=3, line_spacing=1.2)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            set_font(rb, size=13, bold=True)
        r = p.add_run(text)
        set_font(r, size=13)
        return p

    def add_code(text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 100, 100, 150, 150)
        p = cell.paragraphs[0]
        set_para_spacing(p, before=2, after=2, line_spacing=1.1)
        r = p.add_run(text)
        set_font(r, name="Consolas", size=10, color_rgb=(15, 23, 42))

    # =========================================================================
    # TRANG BÌA (COVER PAGE) CHUẨN MẪU PTIT
    # =========================================================================
    p = doc.add_paragraph()
    set_para_spacing(p, before=10, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run("BỘ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    set_font(r, size=13, bold=True)
    r2 = p.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nCƠ SỞ TẠI TP. HỒ CHÍ MINH")
    set_font(r2, size=13.5, bold=True)

    p_line = doc.add_paragraph()
    set_para_spacing(p_line, before=2, after=30, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_line = p_line.add_run("-----------------------------")
    set_font(r_line, size=13)

    p_title = doc.add_paragraph()
    set_para_spacing(p_title, before=40, after=25, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t1 = p_title.add_run("BÁO CÁO\nĐỒ ÁN MÔN HỌC\n")
    set_font(r_t1, size=24, bold=True, color_rgb=(15, 23, 42))

    p_topic = doc.add_paragraph()
    set_para_spacing(p_topic, before=10, after=40, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_tp1 = p_topic.add_run("ĐỀ TÀI: THIẾT KẾ CƠ SỞ DỮ LIỆU TECHSTORE & CHUYÊN ĐỀ CHƯƠNG 30: DATABASE SECURITY (AN TOÀN VÀ BẢO MẬT CƠ SỞ DỮ LIỆU)\n")
    set_font(r_tp1, size=15, bold=True, color_rgb=(30, 58, 138))

    # Info block
    p_info = doc.add_paragraph()
    set_para_spacing(p_info, before=30, after=4, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.LEFT)
    r = p_info.add_run("Môn học: ")
    set_font(r, size=13, bold=True)
    r = p_info.add_run("Cơ sở dữ liệu (Database Systems)\n")
    set_font(r, size=13)

    r = p_info.add_run("Giảng viên hướng dẫn: ")
    set_font(r, size=13, bold=True)
    r = p_info.add_run("ThS. Tuyết Hải (Email: tuyethai@ptithcm.edu.vn)\n")
    set_font(r, size=13)

    r = p_info.add_run("Thực hiện bởi nhóm sinh viên, bao gồm:\n")
    set_font(r, size=13, bold=True)

    # Bảng sinh viên bìa
    tbl_sv = doc.add_table(rows=3, cols=3)
    tbl_sv.alignment = WD_TABLE_ALIGNMENT.CENTER
    sv_data = [
        ("Nguyễn Thành Thiện (hoặc Tên SV 1)", "N24DCCN076", "Trưởng nhóm"),
        ("Thành viên nhóm 02", "MSSV 02", "Thành viên"),
        ("Thành viên nhóm 03", "MSSV 03", "Thành viên")
    ]
    for row_idx, data in enumerate(sv_data):
        row = tbl_sv.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p_c = cell.paragraphs[0]
            set_para_spacing(p_c, before=2, after=2)
            r_c = p_c.add_run(text)
            set_font(r_c, size=13, bold=(col_idx==2))

    p_foot = doc.add_paragraph()
    set_para_spacing(p_foot, before=80, after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_ft = p_foot.add_run("TP. HỒ CHÍ MINH, THÁNG 11 NĂM 2026")
    set_font(r_ft, size=12.5, bold=True)

    doc.add_page_break()

    # =========================================================================
    # TRANG THÔNG TIN BẮT BUỘC: PHÂN CÔNG NHIỆM VỤ, TỶ LỆ ĐÓNG GÓP & GITHUB LINK
    # =========================================================================
    add_heading_1("THÔNG TIN NHÓM VÀ BẢNG PHÂN CÔNG NHIỆM VỤ")
    
    add_body("Bảng thống kê chi tiết mức độ tham gia, phân công nhiệm vụ cụ thể và tỷ lệ phần trăm đóng góp của từng thành viên trong bài tập nhóm đồ án môn học:")

    tbl_assign = doc.add_table(rows=4, cols=5)
    tbl_assign.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["STT", "Họ và Tên", "Mã số sinh viên", "Nhiệm vụ phân công", "Tỷ lệ đóng góp"]
    widths = [Inches(0.6), Inches(1.8), Inches(1.2), Inches(2.6), Inches(1.2)]
    
    # Header row
    hdr_row = tbl_assign.rows[0]
    for i, h_text in enumerate(headers):
        cell = hdr_row.cells[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 120, 120, 100, 100)
        p = cell.paragraphs[0]
        set_para_spacing(p, before=2, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(h_text)
        set_font(r, size=11, bold=True, color_rgb=(255, 255, 255))

    assign_data = [
        ("1", "Nguyễn Thành Thiện (Đại diện)", "N24DCCN076", "Phụ trách Phần 1 (Khảo sát nghiệp vụ, ERD, Schema, DDL/DML, chuẩn hóa BCNF); Trưởng nhóm tổng hợp báo cáo.", "34%"),
        ("2", "Thành viên nhóm 02", "MSSV 02", "Phụ trách Phần 2 (Đọc hiểu & viết báo cáo Chương 30 Database Security: DAC, MAC, RBAC, SQLi, Encryption); Soạn thảo Slides.", "33%"),
        ("3", "Thành viên nhóm 03", "MSSV 03", "Phụ trách Phần 3 (Phát triển ứng dụng Web Demo Security Lab: SQLi, RBAC, Hashing; Viết kịch bản T-SQL trên SQL Server; Quản trị Git).", "33%")
    ]

    for row_idx, row_data in enumerate(assign_data, start=1):
        row = tbl_assign.rows[row_idx]
        bg_col = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 100, 100, 100, 100)
            p = cell.paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
            set_para_spacing(p, before=2, after=2, align=align)
            r = p.add_run(text)
            set_font(r, size=11, bold=(col_idx==4))

    # GitHub Repository Link Box
    doc.add_paragraph()
    tbl_git = doc.add_table(rows=1, cols=1)
    tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_git = tbl_git.cell(0, 0)
    set_cell_background(cell_git, "EFF6FF")
    set_cell_margins(cell_git, 120, 120, 150, 150)
    p_git = cell_git.paragraphs[0]
    set_para_spacing(p_git, before=3, after=3)
    r_g1 = p_git.add_run("LINK GITHUB DEMO & TOÀN BỘ MÃ NGUỒN ĐỒ ÁN:\n")
    set_font(r_g1, size=12, bold=True, color_rgb=(30, 58, 138))
    r_g2 = p_git.add_run("https://github.com/TechStore-DB/Database-Security-Project\n")
    set_font(r_g2, size=12, bold=True, color_rgb=(2, 132, 199))
    r_g3 = p_git.add_run("(Kho chứa bao gồm: Toàn bộ script SQL Server .sql, source code Web Demo Python Flask, file Báo cáo Word/PDF và Slides trình chiếu PowerPoint)")
    set_font(r_g3, size=11, italic=True, color_rgb=(100, 116, 139))

    doc.add_page_break()

    # =========================================================================
    # MỤC LỤC & DANH MỤC HÌNH BẢNG
    # =========================================================================
    add_heading_1("MỤC LỤC")
    toc_items = [
        ("THÔNG TIN NHÓM VÀ BẢNG PHÂN CÔNG NHIỆM VỤ", "2"),
        ("TÓM TẮT ĐỒ ÁN", "4"),
        ("CHƯƠNG I. TỔNG QUAN VÀ KHẢO SÁT NGHIỆP VỤ HỆ THỐNG TECHSTORE", "5"),
        ("   1. Giới thiệu đề tài và tính cấp thiết", "5"),
        ("   2. Mục tiêu nghiên cứu và phạm vi đồ án", "5"),
        ("   3. Khảo sát quy trình nghiệp vụ hệ thống bán hàng TechStore", "6"),
        ("CHƯƠNG II. THIẾT KẾ CSDL VÀ CHUẨN HÓA MÔ HÌNH QUAN HỆ", "7"),
        ("   1. Thiết kế Mô hình Thực thể - Liên kết (ERD)", "7"),
        ("   2. Ánh xạ từ mô hình ERD sang Mô hình Quan hệ (Relational Mapping)", "9"),
        ("   3. Phân tích Phụ thuộc hàm và Chứng minh chuẩn hóa đạt chuẩn BCNF", "11"),
        ("CHƯƠNG III. CÀI ĐẶT CSDL TRÊN SQL SERVER VÀ TRUY VẤN NÂNG CAO", "14"),
        ("   1. Kịch bản DDL khởi tạo Database và ràng buộc toàn vẹn", "14"),
        ("   2. Dữ liệu mẫu hoàn chỉnh (DML)", "16"),
        ("   3. Bộ sưu tập 25+ câu truy vấn DQL, View, Procedure và Trigger", "17"),
        ("CHƯƠNG IV. NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30 - DATABASE SECURITY", "21"),
        ("   1. Tổng quan an toàn CSDL và Tam giác bảo mật CIA (Mục 30.1)", "21"),
        ("   2. Kiểm soát truy cập tùy biến (DAC) và cú pháp SQL Privileges (Mục 30.2)", "23"),
        ("   3. Kiểm soát truy cập bắt buộc (MAC) và Phân quyền theo vai trò RBAC (Mục 30.3)", "25"),
        ("   4. Lỗ hổng SQL Injection và Kỹ thuật phòng thủ toàn diện (Mục 30.4)", "28"),
        ("   5. An toàn CSDL thống kê và Kiểm soát luồng thông tin (Mục 30.5 & 30.6)", "31"),
        ("   6. Mã hóa CSDL, Băm mật khẩu có Salt và Hạ tầng khóa công khai (Mục 30.7)", "33"),
        ("   7. Bảo vệ quyền riêng tư và Các thách thức an ninh dữ liệu hiện đại (Mục 30.8 - 30.10)", "36"),
        ("CHƯƠNG V. XÂY DỰNG ỨNG DỤNG DEMO VÀ THỰC NGHIỆM AN NINH CSDL", "38"),
        ("   1. Kiến trúc ứng dụng TechStore Cyber Security Lab", "38"),
        ("   2. Thực nghiệm 1: Khai thác và Phòng thủ SQL Injection", "39"),
        ("   3. Thực nghiệm 2: Mô phỏng Ma trận Phân quyền Vai trò (RBAC)", "41"),
        ("   4. Thực nghiệm 3: Băm mật khẩu, Tấn công Rainbow Table & Mã hóa AES-256", "43"),
        ("   5. Thực nghiệm 4: Triển khai kịch bản T-SQL (RLS & Data Masking) trên SQL Server", "45"),
        ("CHƯƠNG VI. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "47"),
        ("TÀI LIỆU THAM KHẢO", "48")
    ]
    for title, pg in toc_items:
        p = doc.add_paragraph()
        set_para_spacing(p, before=1, after=2, line_spacing=1.15)
        r1 = p.add_run(title)
        set_font(r1, size=11.5, bold=title.startswith("CHƯƠNG") or title.startswith("THÔNG TIN") or title.startswith("TÓM TẮT") or title.startswith("TÀI LIỆU"))
        r2 = p.add_run(f" {' . ' * 20} {pg}")
        set_font(r2, size=11, color_rgb=(100, 116, 139))

    doc.add_page_break()

    # DANH SÁCH HÌNH VÀ BẢNG
    add_heading_1("DANH SÁCH HÌNH, BẢNG")
    add_body("Danh mục các hình ảnh minh họa trong báo cáo:", bold_prefix="A. Danh mục Hình vẽ:\n")
    fig_list = [
        "Hình 1: Sơ đồ Thực thể - Liên kết (ERD) hoàn chỉnh Hệ thống TechStore",
        "Hình 2: Sơ đồ Lược đồ Cơ sở Dữ liệu Quan hệ (Relational Schema) đạt chuẩn BCNF",
        "Hình 3: Tam giác bảo mật CIA trong An toàn Cơ sở Dữ liệu",
        "Hình 4: Ma trận kiểm soát truy cập (Access Matrix) trong mô hình DAC",
        "Hình 5: Mô hình An ninh đa cấp Bell-LaPadula (Simple Security & *-Property)",
        "Hình 6: Phân cấp vai trò (Role Hierarchy) và Ma trận quyền hạn RBAC",
        "Hình 7: Cơ chế phân tích cú pháp SQL Injection và nguyên lý Parameterized Query",
        "Hình 8: Quy trình băm mật khẩu một chiều với Salt ngẫu nhiên",
        "Hình 9: Giao diện chính Phòng thí nghiệm An ninh CSDL TechStore",
        "Hình 10: Minh chứng thực nghiệm khai thác thành công lỗ hổng SQL Injection Bypass",
        "Hình 11: Minh chứng khai thác rò rỉ dữ liệu tài khoản bằng kỹ thuật UNION SQLi",
        "Hình 12: Thử nghiệm phân quyền RBAC và Row-Level Security (RLS)"
    ]
    for f in fig_list:
        add_bullet(f)

    add_body("\nDanh mục các bảng biểu trong báo cáo:", bold_prefix="B. Danh mục Bảng biểu:\n")
    tbl_list = [
        "Bảng 1: Bảng phân công nhiệm vụ và tỷ lệ đóng góp của thành viên nhóm",
        "Bảng 2: Danh sách các thực thể, thuộc tính và khóa của CSDL TechStore",
        "Bảng 3: Tổng hợp các ràng buộc toàn vẹn (Constraints) trên Microsoft SQL Server",
        "Bảng 4: Bảng so sánh toàn diện giữa hai mô hình kiểm soát truy cập DAC và MAC",
        "Bảng 5: Ma trận quyền hạn theo vai trò (Access Control Matrix) của hệ thống",
        "Bảng 6: Bảng so sánh các giải pháp phòng chống tấn công SQL Injection",
        "Bảng 7: Kết quả thử nghiệm Rainbow Table đối với các thuật toán băm mật khẩu"
    ]
    for t in tbl_list:
        add_bullet(t)

    doc.add_page_break()

    # =========================================================================
    # TÓM TẮT ĐỒ ÁN
    # =========================================================================
    add_heading_1("TÓM TẮT ĐỒ ÁN")
    add_body("Đồ án môn học Cơ sở dữ liệu là cơ hội để nhóm sinh viên củng cố, liên kết và vận dụng toàn diện kiến thức lý thuyết đã tích lũy trên giảng đường vào một bài toán thực tiễn hoàn chỉnh. Nội dung báo cáo được cấu trúc chặt chẽ thành hai trọng tâm cốt lõi:")
    add_bullet("Phần 1 - Thiết kế và Cài đặt CSDL Thực tế: Lựa chọn đề tài 'Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore'. Nhóm tiến hành khảo sát nghiệp vụ kinh doanh thiết bị công nghệ số, xây dựng mô hình Thực thể - Liên kết (ERD) gồm 10 thực thể với đầy đủ quan hệ 1-1, 1-N, N-N và quan hệ đệ quy; áp dụng thuật toán ánh xạ 7 bước sang Mô hình quan hệ; phân tích toán học các phụ thuộc hàm và chứng minh toàn bộ 10 lược đồ đều đạt dạng chuẩn cao BCNF. Sau đó, CSDL được cài đặt trực tiếp trên Microsoft SQL Server 2022 với đầy đủ ràng buộc toàn vẹn, dữ liệu mẫu phong phú và bộ 25+ câu truy vấn phức tạp (JOIN, GROUP BY, HAVING, Subqueries, Views, Stored Procedures, Functions, Triggers).", bold_prefix="1. Thiết kế CSDL TechStore: ")
    add_bullet("Phần 2 - Nghiên cứu Chuyên sâu Chương 30 (Database Security): Đọc hiểu toàn diện giáo trình kinh điển 'Fundamentals of Database Systems' (7th edition) của Ramez Elmasri và Shamkant B. Navathe. Báo cáo phân tích cặn kẽ 10 nội dung lớn của Chương 30: Tam giác bảo mật CIA; Kiểm soát truy cập tùy biến (DAC) và cú pháp GRANT/REVOKE; Kiểm soát bắt buộc (MAC) theo mô hình Bell-LaPadula; Phân quyền vai trò (RBAC); Lỗ hổng SQL Injection và giải pháp phòng thủ Parameterized Queries; CSDL Thống kê; Kiểm soát luồng thông tin (Flow Control); Kỹ thuật mã hóa đối xứng (AES), bất đối xứng (RSA), băm mật khẩu có Salt và mã hóa lưu trữ trong suốt (TDE); Bảo vệ quyền riêng tư (k-anonymity, l-diversity); và cơ chế Row-Level Security (RLS).", bold_prefix="2. Nghiên cứu Chuyên sâu Chương 30: ")
    add_bullet("Phần 3 - Ứng dụng Demo Thực nghiệm (Security Lab): Nhóm đã hiện thực hóa toàn bộ lý thuyết Chương 30 bằng một ứng dụng Web Cyber Security Lab hoàn chỉnh bằng Python Flask, cho phép người dùng trực tiếp thử nghiệm các đòn tấn công SQL Injection nguy hiểm (Authentication Bypass, UNION-based leak) và quan sát sự bảo vệ tuyệt đối của Prepared Statements; mô phỏng ma trận phân quyền RBAC; kiểm chứng tốc độ bẻ khóa MD5 bằng Rainbow Table so với độ an toàn của SHA-256 + Salt; và cung cấp kịch bản T-SQL triển khai Row-Level Security cùng Dynamic Data Masking trên SQL Server.", bold_prefix="3. Sản phẩm Demo Thực nghiệm: ")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG I: TỔNG QUAN
    # =========================================================================
    add_heading_1("CHƯƠNG I. TỔNG QUAN VÀ KHẢO SÁT NGHIỆP VỤ")
    
    add_heading_2("1. Giới thiệu đề tài và tính cấp thiết")
    add_body("Trong thời đại chuyển đổi số mạnh mẽ, các hệ thống thương mại điện tử (E-Commerce) đã trở thành hạ tầng kinh tế thiết yếu phục vụ hàng triệu người dùng mỗi ngày. Sự bùng nổ của giao dịch trực tuyến đặt ra yêu cầu cấp thiết về một hệ thống cơ sở dữ liệu có năng lực lưu trữ lớn, tốc độ truy vấn cao, tính nhất quán dữ liệu hoàn hảo và trên hết là khả năng tự bảo vệ trước các cuộc tấn công mạng ngày càng tinh vi.")
    add_body("Đề tài 'Hệ thống Quản lý Bán hàng & Thương mại Điện tử TechStore' được lựa chọn nhằm xây dựng một mô hình CSDL tiêu chuẩn cho chuỗi bán lẻ thiết bị công nghệ hiện đại (Laptop, Smartphone, Tablet, Phụ kiện), đồng thời tạo môi trường lý tưởng để nghiên cứu và thực nghiệm các cơ chế an toàn CSDL theo tiêu chuẩn học thuật quốc tế.")

    add_heading_2("2. Mục tiêu nghiên cứu và phạm vi đồ án")
    add_body("Đồ án hướng tới các mục tiêu cụ thể sau:")
    add_bullet("Nắm vững và thực hành thành thạo quy trình thiết kế CSDL từ phân tích yêu cầu nghiệp vụ, mô hình hóa ERD, chuyển đổi lược đồ quan hệ, đến tối ưu hóa chuẩn hóa dữ liệu.")
    add_bullet("Ứng dụng toán học rời rạc và lý thuyết phụ thuộc hàm để chứng minh tính tối ưu của cấu trúc bảng, triệt tiêu mọi dị thường dữ liệu (Anomalies) ở mức chuẩn BCNF.")
    add_bullet("Lập trình thành thạo hệ quản trị CSDL Microsoft SQL Server thông qua các kỹ thuật DDL, DML, DQL phức tạp, Transaction đảm bảo tính chất ACID, Stored Procedure và Trigger.")
    add_bullet("Nghiên cứu chuyên sâu toàn bộ nội dung Chương 30 (Database Security) trong giáo trình 'Fundamentals of Database Systems' (7E), liên hệ chặt chẽ giữa lý thuyết hàn lâm và giải pháp an ninh mạng thực tế.")
    add_bullet("Xây dựng thành công ứng dụng Demo trực quan phục vụ công tác báo cáo, thuyết trình và bảo vệ đồ án trước Hội đồng chấm điểm.")

    add_heading_2("3. Khảo sát quy trình nghiệp vụ hệ thống TechStore")
    add_body("Qua khảo sát hoạt động của chuỗi phân phối bán lẻ thiết bị công nghệ, hệ thống TechStore vận hành theo các luồng nghiệp vụ chuẩn tắc sau:")
    add_bullet("Quản lý danh mục & nhà cung cấp: Hệ thống phân loại thiết bị theo danh mục đa cấp (Laptop văn phòng, Laptop gaming, Smartphone cao cấp, Âm thanh). Mỗi danh mục có nhiều sản phẩm. Mỗi sản phẩm được cung ứng chính thức từ các nhà phân phối có uy tín (Apple VN, Asus, Samsung, Dell, Sony). Ràng buộc chặt chẽ: Giá bán phải lớn hơn hoặc bằng giá nhập, số lượng tồn kho không được âm.", bold_prefix="a) Quản lý Chuỗi cung ứng: ")
    add_bullet("Khách hàng đăng ký tài khoản qua Email và Số điện thoại duy nhất. Nhằm bảo vệ an toàn thông tin theo chuẩn quốc tế, mật khẩu người dùng không bao giờ lưu dưới dạng bản rõ mà phải băm một chiều SHA-256 kết hợp chuỗi ngẫu nhiên (Salt). Hệ thống theo dõi lịch sử mua sắm để tự động tích điểm và nâng hạng thành viên (Đồng, Bạc, Vàng, Kim Cương) theo tổng chi tiêu.", bold_prefix="b) Quản lý Khách hàng & Tài khoản: ")
    add_bullet("Khách hàng chọn sản phẩm vào giỏ hàng và tiến hành đặt hàng. Một đơn hàng có thể chứa nhiều sản phẩm với số lượng và đơn giá khác nhau. Đơn hàng trải qua các trạng thái: Chờ xác nhận -> Đang xử lý -> Đang giao hàng -> Hoàn thành (hoặc Đã hủy). Sau khi thanh toán thành công, hệ thống xuất một hóa đơn tài chính duy nhất (Quan hệ 1-1) lưu vết mã giao dịch ngân hàng hoặc cổng thanh toán điện tử.", bold_prefix="c) Quy trình Đơn hàng & Thanh toán: ")
    add_bullet("Cơ cấu nhân viên được quản lý theo quan hệ đệ quy (Nhân viên chịu sự quản lý trực tiếp của Quản lý bộ phận). Mỗi nhân sự được gán một vai trò hệ thống cụ thể (Admin, Quản lý, Nhân viên bán hàng, Thủ kho). Quyền hạn truy cập các chức năng phần mềm và bảng dữ liệu được kiểm soát nghiêm ngặt theo mô hình RBAC.", bold_prefix="d) Quản trị Nhân sự & Phân quyền: ")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG II: THIẾT KẾ CSDL & CHUẨN HÓA BCNF
    # =========================================================================
    add_heading_1("CHƯƠNG II. THIẾT KẾ CSDL VÀ CHUẨN HÓA MÔ HÌNH QUAN HỆ")

    add_heading_2("1. Thiết kế Mô hình Thực thể - Liên kết (ERD)")
    add_body("Căn cứ vào khảo sát nghiệp vụ, nhóm xây dựng mô hình Thực thể - Liên kết (Entity-Relationship Diagram - ERD) bao gồm 10 thực thể chính, phản ánh đầy đủ cấu trúc dữ liệu và mối quan hệ giữa các đối tượng trong hệ thống.")

    # Chèn ảnh ERD nếu tồn tại
    erd_file = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/ERD_TechStore.png"
    if os.path.exists(erd_file):
        doc.add_paragraph()
        doc.add_picture(erd_file, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        set_para_spacing(p_cap, before=4, after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_c = p_cap.add_run("Hình 1: Sơ đồ Thực thể - Liên kết (ERD) Hệ thống TechStore (Độ phân giải cao)")
        set_font(r_c, size=11, bold=True, italic=True)

    add_body("Phân tích chi tiết các mối kết hợp trong mô hình ERD:", bold_prefix="Mối kết hợp và Bản số (Cardinality):\n")
    add_bullet("Quan hệ DANH_MUC - SAN_PHAM (1 - N): Một danh mục có nhiều sản phẩm; mỗi sản phẩm thuộc đúng một danh mục.")
    add_bullet("Quan hệ NHA_CUNG_CAP - SAN_PHAM (1 - N): Một nhà cung cấp có thể cấp nhiều sản phẩm; mỗi sản phẩm do một nhà cung cấp phân phối chính thức.")
    add_bullet("Quan hệ VAI_TRO - NHAN_VIEN (1 - N): Mỗi vai trò hệ thống được phân cho nhiều nhân viên.")
    add_bullet("Quan hệ NHAN_VIEN - NHAN_VIEN (1 - N, Đệ quy): Một quản lý cấp trên phụ trách quản lý nhiều nhân viên cấp dưới.")
    add_bullet("Quan hệ KHACH_HANG - DON_HANG (1 - N): Một khách hàng có thể đặt nhiều đơn hàng trong lịch sử mua sắm.")
    add_bullet("Quan hệ NHAN_VIEN - DON_HANG (1 - N): Một nhân viên bán hàng tiếp nhận và xử lý nhiều đơn hàng.")
    add_bullet("Quan hệ SAN_PHAM - DON_HANG (N - N): Một đơn hàng có nhiều sản phẩm và một sản phẩm có thể xuất hiện trong nhiều đơn hàng khác nhau. Mối quan hệ được ánh xạ thông qua thực thể kết hợp CHI_TIET_DON_HANG với các thuộc tính: SoLuong, DonGia, ChietKhau, ThanhTien.")
    add_bullet("Quan hệ DON_HANG - HOA_DON (1 - 1): Mỗi đơn hàng hoàn tất phát hành đúng một hóa đơn tài chính tương ứng.")
    add_bullet("Quan hệ KHACH_HANG - SAN_PHAM (N - N): Khách hàng để lại nhận xét và chấm điểm cho sản phẩm đã mua, được ánh xạ thành thực thể DANH_GIA_SAN_PHAM.")

    add_heading_2("2. Ánh xạ từ ERD sang Mô hình Quan hệ (Relational Mapping)")
    add_body("Quá trình ánh xạ tuân thủ nghiêm ngặt 7 bước chuyển đổi chuẩn tắc từ mô hình ERD sang Mô hình Quan hệ (Relational Model) theo giáo trình Elmasri & Navathe (Chương 9):")
    add_bullet("Bước 1: Ánh xạ các thực thể thông thường (Regular Entities): Khởi tạo các quan hệ DANH_MUC, NHA_CUNG_CAP, KHACH_HANG, VAI_TRO với khóa chính tương ứng.")
    add_bullet("Bước 2: Ánh xạ mối kết hợp 1-N nhị phân: Bổ sung khóa ngoại vào phía 'N' (Bổ sung MaDanhMuc, MaNCC vào SAN_PHAM; bổ sung MaVaiTro, MaQuanLy vào NHAN_VIEN; bổ sung MaKH, MaNV vào DON_HANG).")
    add_bullet("Bước 3: Ánh xạ mối kết hợp 1-1 nhị phân: Bổ sung khóa ngoại MaDonHang vào HOA_DON với ràng buộc UNIQUE để đảm bảo quan hệ đơn vị 1-1.")
    add_bullet("Bước 4: Ánh xạ mối kết hợp N-N: Khởi tạo quan hệ kết hợp CHI_TIET_DON_HANG với khóa chính phức hợp gồm (MaDonHang, MaSP). Khởi tạo DANH_GIA_SAN_PHAM với khóa chính MaDanhGia và các khóa ngoại MaSP, MaKH.")

    # Chèn ảnh Schema nếu tồn tại
    schema_file = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/01_Phan1_ThietKeCSDL/Relational_Schema_TechStore.png"
    if os.path.exists(schema_file):
        doc.add_paragraph()
        doc.add_picture(schema_file, width=Inches(6.2))
        p_cap2 = doc.add_paragraph()
        set_para_spacing(p_cap2, before=4, after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_c2 = p_cap2.add_run("Hình 2: Lược đồ Cơ sở Dữ liệu Quan hệ (Relational Schema) đạt chuẩn BCNF")
        set_font(r_c2, size=11, bold=True, italic=True)

    add_heading_2("3. Phân tích Phụ thuộc hàm và Chứng minh chuẩn hóa đạt BCNF")
    add_body("Chuẩn hóa dữ liệu là khâu cốt lõi trong thiết kế CSDL nhằm loại bỏ hoàn toàn dư thừa dữ liệu và triệt tiêu ba dạng bất thường nguy hiểm: Bất thường thêm (Insertion Anomaly), Bất thường xóa (Deletion Anomaly), và Bất thường sửa (Update Anomaly).")

    add_heading_3("a) Định nghĩa các dạng chuẩn lý thuyết (Normal Forms)")
    add_bullet("Dạng chuẩn 1 (1NF): Một lược đồ quan hệ R đạt chuẩn 1NF nếu và chỉ nếu toàn bộ miền giá trị của các thuộc tính trong R đều là nguyên tố (Atomic) - không chứa nhóm lặp, không chứa thuộc tính phức hợp hay thuộc tính đa trị.")
    add_bullet("Dạng chuẩn 2 (2NF): Đạt 1NF và mọi thuộc tính không khóa đều phụ thuộc hàm đầy đủ vào khóa chính (không tồn tại phụ thuộc hàm bộ phận vào một phần của khóa chính).")
    add_bullet("Dạng chuẩn 3 (3NF): Đạt 2NF và không có thuộc tính không khóa nào phụ thuộc bắc cầu vào khóa chính (nếu X -> A thì X là siêu khóa hoặc A là thuộc tính khóa nguyên tố).")
    add_bullet("Dạng chuẩn Boyce-Codd (BCNF): Một lược đồ quan hệ R đạt chuẩn BCNF nếu với mọi phụ thuộc hàm không tầm thường X -> Y thuộc F+, thì vế trái X bắt buộc phải là một Siêu khóa (Superkey) của R. Dạng chuẩn BCNF là chuẩn chặt chẽ hơn 3NF, giải quyết triệt để trường hợp khóa chính phức hợp có các thuộc tính giao thoa.")

    add_heading_3("b) Chứng minh toán học cho từng Lược đồ Quan hệ TechStore")
    add_body("1. Lược đồ SAN_PHAM(MaSP, TenSP, MaDanhMuc, MaNCC, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai):\n"
             "- Tập phụ thuộc hàm F = {MaSP -> TenSP, MaDanhMuc, MaNCC, GiaNhap, GiaBan, SoLuongTon, DonViTinh, MoTa, TrangThai}.\n"
             "- Khóa ứng viên duy nhất: K = {MaSP} vì bao đóng {MaSP}+ chứa toàn bộ thuộc tính của quan hệ.\n"
             "- Phân tích: Quan hệ đạt 1NF vì các trường dữ liệu đều là nguyên tố. Khóa chính là khóa đơn (1 thuộc tính), suy ra không thể tồn tại phụ thuộc hàm bộ phận -> Đạt 2NF. Không có thuộc tính không khóa nào suy diễn ra thuộc tính không khóa khác (thông tin tên danh mục, tên NCC đã được tách sang bảng cha) -> Không có phụ thuộc bắc cầu -> Đạt 3NF. Vế trái {MaSP} là siêu khóa duy nhất của mọi phụ thuộc hàm trong F -> ĐẠT CHUẨN BCNF.")

    add_body("2. Lược đồ CHI_TIET_DON_HANG(MaDonHang, MaSP, SoLuong, DonGia, ChietKhau, ThanhTien):\n"
             "- Khóa chính phức hợp: K = {MaDonHang, MaSP}.\n"
             "- Tập phụ thuộc hàm F = {{MaDonHang, MaSP} -> {SoLuong, DonGia, ChietKhau}, {SoLuong, DonGia, ChietKhau} -> ThanhTien}.\n"
             "- Phân tích: Không có thuộc tính nào phụ thuộc riêng rẽ vào {MaDonHang} hay {MaSP} (Tên sản phẩm hay giá gốc không lưu tại đây mà ở SAN_PHAM, Ngày đặt hàng lưu ở DON_HANG). Do đó không có phụ thuộc bộ phận -> Đạt 2NF. Cột ThanhTien là thuộc tính tính toán tự động (Computed column PERSISTED trong SQL Server) nên không tạo ra dư thừa dữ liệu. Vế trái {MaDonHang, MaSP} là siêu khóa duy nhất chi phối toàn bộ thông tin -> ĐẠT CHUẨN BCNF.")

    add_body("3. Lược đồ DON_HANG, KHACH_HANG, NHAN_VIEN, HOA_DON:\n"
             "- Tất cả các bảng trên đều có khóa chính đơn nhất (MaDonHang, MaKH, MaNV, MaHoaDon). Mọi thuộc tính mô tả đều phụ thuộc hàm trực tiếp và đầy đủ vào khóa chính tương ứng. Không tồn tại chuỗi phụ thuộc bắc cầu trong nội bộ bảng.\n"
             "- Kết luận: 100% các lược đồ quan hệ trong hệ thống TechStore đều đạt chuẩn cao nhất BCNF.")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG III: CÀI ĐẶT TRÊN SQL SERVER VÀ BỘ TRUY VẤN NÂNG CAO
    # =========================================================================
    add_heading_1("CHƯƠNG III. CÀI ĐẶT CSDL TRÊN SQL SERVER VÀ TRUY VẤN NÂNG CAO")

    add_heading_2("1. Kịch bản DDL khởi tạo Database và ràng buộc toàn vẹn")
    add_body("CSDL TechStoreDB được cài đặt trên hệ quản trị CSDL quan hệ Microsoft SQL Server 2022 với collate hỗ trợ tiếng Việt đầy đủ (Vietnamese_CI_AS). Cấu trúc bảng và các ràng buộc được lập trình chi tiết trong file '01_DDL_Create_TechStoreDB.sql'.")
    add_body("Hệ thống cài đặt đầy đủ các loại ràng buộc toàn vẹn theo chuẩn SQL Server:")
    add_bullet("Ràng buộc Khóa chính (PRIMARY KEY): Đảm bảo tính duy nhất của thực thể và tự động tạo Clustered Index tối ưu truy vấn.")
    add_bullet("Ràng buộc Khóa ngoại (FOREIGN KEY): Đảm bảo tính toàn vẹn tham chiếu với các hành vi thích hợp (ON UPDATE CASCADE đảm bảo tính đồng bộ mã danh mục/mã khách hàng, ON DELETE NO ACTION ngăn chặn xóa dữ liệu giao dịch lịch sử).")
    add_bullet("Ràng buộc Kiểm tra (CHECK): Kiểm soát logic nghiệp vụ chặt chẽ: CK_SP_GiaBan (GiaBan >= GiaNhap), CK_CTDH_SoLuong (SoLuong > 0), CK_KH_Email (Email đúng định dạng regex), CK_DG_Diem (DiemDanhGia BETWEEN 1 AND 5).")
    add_bullet("Ràng buộc Duy nhất (UNIQUE): Đảm bảo tính độc nhất của Email, Số điện thoại của Khách hàng, Nhà cung cấp, Nhân viên.")

    add_heading_2("2. Dữ liệu mẫu hoàn chỉnh (DML)")
    add_body("Tệp tin '02_DML_Insert_SampleData.sql' chứa dữ liệu mẫu phong phú và thực tế cho toàn bộ 10 bảng trong hệ thống, bao gồm 4 vai trò, 6 danh mục, 6 nhà cung cấp hàng đầu, 10 khách hàng với mật khẩu băm bảo mật, 7 nhân viên theo mô hình phân cấp, 10 sản phẩm công nghệ thịnh hành, 12 đơn hàng ở các trạng thái khác nhau, 17 chi tiết đơn hàng, 8 hóa đơn thanh toán và 7 đánh giá khách hàng.")

    add_heading_2("3. Bộ sưu tập truy vấn DQL, View, Procedure và Trigger tiêu biểu")
    add_body("Tệp tin '03_DQL_Advanced_Queries.sql' cung cấp bộ sưu tập hơn 25 câu truy vấn bao quát từ mức độ cơ bản đến phức tạp, minh chứng khả năng khai thác dữ liệu tối ưu của CSDL TechStore:")

    add_heading_3("a) Truy vấn nối bảng phức tạp (Multi-table JOIN)")
    add_code("""-- Truy vấn nối 3 bảng hiển thị sản phẩm kèm tên danh mục và tên nhà cung cấp
SELECT sp.MaSP, sp.TenSP, dm.TenDanhMuc, ncc.TenNCC, sp.GiaBan, sp.SoLuongTon
FROM SAN_PHAM sp
INNER JOIN DANH_MUC dm ON sp.MaDanhMuc = dm.MaDanhMuc
INNER JOIN NHA_CUNG_CAP ncc ON sp.MaNCC = ncc.MaNCC
ORDER BY dm.TenDanhMuc, sp.GiaBan DESC;""")

    add_heading_3("b) Truy vấn gom nhóm và lọc theo điều kiện nhóm (GROUP BY & HAVING)")
    add_code("""-- Thống kê tổng doanh thu từng danh mục có doanh thu trên 40 triệu VNĐ
SELECT dm.MaDanhMuc, dm.TenDanhMuc, SUM(ct.SoLuong) AS TongDaBan, SUM(ct.ThanhTien) AS DoanhThu
FROM DANH_MUC dm
INNER JOIN SAN_PHAM sp ON dm.MaDanhMuc = sp.MaDanhMuc
INNER JOIN CHI_TIET_DON_HANG ct ON sp.MaSP = ct.MaSP
INNER JOIN DON_HANG dh ON ct.MaDonHang = dh.MaDonHang
WHERE dh.TrangThaiDonHang = N'Hoàn thành'
GROUP BY dm.MaDanhMuc, dm.TenDanhMuc
HAVING SUM(ct.ThanhTien) >= 40000000;""")

    add_heading_3("c) Truy vấn lồng và Hàm phân tích xếp hạng (Window Functions)")
    add_code("""-- Xếp hạng sản phẩm bán chạy nhất trong từng danh mục bằng hàm DENSE_RANK()
WITH XepHangSP AS (
    SELECT dm.TenDanhMuc, sp.MaSP, sp.TenSP, SUM(ct.SoLuong) AS TongBan,
           DENSE_RANK() OVER (PARTITION BY sp.MaDanhMuc ORDER BY SUM(ct.SoLuong) DESC) AS Hang
    FROM SAN_PHAM sp
    INNER JOIN DANH_MUC dm ON sp.MaDanhMuc = dm.MaDanhMuc
    INNER JOIN CHI_TIET_DON_HANG ct ON sp.MaSP = ct.MaSP
    GROUP BY dm.TenDanhMuc, sp.MaDanhMuc, sp.MaSP, sp.TenSP
)
SELECT * FROM XepHangSP WHERE Hang = 1;""")

    add_heading_3("d) Thủ tục lưu trữ có quản lý Transaction (ACID)")
    add_body("Thủ tục sp_TaoDonHangMoi nhận tham số đặt hàng, kiểm tra khách hàng hợp lệ, kiểm tra số lượng tồn kho của sản phẩm trong kho. Nếu thỏa mãn, thủ tục tạo đơn hàng, trừ tồn kho và Commit; nếu có lỗi lập tức Rollback toàn bộ giao dịch.")

    add_heading_3("e) Trigger nghiệp vụ tự động thăng hạng khách hàng")
    add_body("Trigger trg_CapNhatTongChiTieuKH tự động kích hoạt mỗi khi đơn hàng chuyển sang trạng thái 'Hoàn thành'. Trigger tính lại tổng chi tiêu lũy kế của khách hàng và gọi hàm fn_XepHangThanhVien để tự động thăng hạng thành viên (Bạc, Vàng, Kim Cương) ngay tức thì.")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG IV: NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30 - DATABASE SECURITY
    # =========================================================================
    add_heading_1("CHƯƠNG IV. NGHIÊN CỨU CHUYÊN SÂU CHƯƠNG 30: DATABASE SECURITY")

    add_heading_2("1. Tổng quan an toàn CSDL và Tam giác bảo mật CIA (Mục 30.1)")
    add_body("Chương 30 trong giáo trình 'Fundamentals of Database Systems' (7th edition) của Elmasri & Navathe khẳng định an ninh CSDL là mắt xích sống còn trong bảo mật thông tin tổng thể của mọi doanh nghiệp. Mọi chiến lược bảo mật CSDL hiện đại đều xoay quanh ba trụ cột cốt lõi của Tam giác bảo mật CIA (CIA Triad):")
    add_bullet("Tính bảo mật (Confidentiality): Đảm bảo dữ liệu nhạy cảm chỉ được truy cập bởi các chủ thể (người dùng, ứng dụng) được cấp phép hợp lệ. Ngăn chặn việc lộ lọt dữ liệu nội bộ ra bên ngoài hoặc giữa các phòng ban chức năng.", bold_prefix="a) Confidentiality: ")
    add_bullet("Tính toàn vẹn (Integrity): Đảm bảo tính chính xác, nhất quán và đáng tin cậy của dữ liệu trong suốt vòng đời lưu trữ và xử lý. Dữ liệu không bị thay đổi, giả mạo hoặc xóa bỏ bởi các thao tác trái phép hay sự cố hệ thống.", bold_prefix="b) Integrity: ")
    add_bullet("Tính sẵn sàng (Availability): Đảm bảo các dịch vụ dữ liệu luôn sẵn sàng phục vụ người dùng hợp pháp khi có nhu cầu, duy trì khả năng hoạt động liên tục trước các đòn tấn công từ chối dịch vụ (DoS/DDoS) hoặc thảm họa kỹ thuật.", bold_prefix="c) Availability: ")
    add_body("Bên cạnh đó, giáo trình phân tích vai trò đặc quyền của Quản trị viên CSDL (DBA) và tầm quan trọng của Nhật ký kiểm toán (Audit Trail) trong việc giám sát, phát hiện bất thường và phục vụ công tác điều tra số (Forensics).")

    add_heading_2("2. Kiểm soát truy cập tùy biến (DAC) và cú pháp SQL Privileges (Mục 30.2)")
    add_body("Kiểm soát truy cập tùy biến (Discretionary Access Control - DAC) là mô hình bảo mật truyền thống và phổ biến nhất trong các RDBMS thương mại:")
    add_bullet("Khái niệm Sở hữu (Ownership): Người dùng tạo ra đối tượng CSDL (bảng, khung nhìn, thủ tục) chính là chủ sở hữu (Owner) của đối tượng đó. Chủ sở hữu có toàn quyền tùy ý cấp quyền (GRANT) hoặc thu hồi quyền (REVOKE) đối tượng cho người dùng khác.")
    add_bullet("Hai cấp độ đặc quyền: Cấp tài khoản (Account-level: CREATE SCHEMA, CREATE TABLE) và Cấp quan hệ (Relation-level: SELECT, INSERT, UPDATE, DELETE).")
    add_bullet("Ủy quyền phân cấp (Propagation of Privileges): Cú pháp WITH GRANT OPTION cho phép người được cấp quyền có thể tiếp tục trao quyền đó cho người khác, hình thành cây phân quyền (Authorization Tree).")
    add_bullet("Thu hồi quyền (Revoking Privileges): Khi thu hồi một quyền đã cấp WITH GRANT OPTION, hệ thống cung cấp 2 tùy chọn: CASCADE (thu hồi đệ quy toàn bộ cây nhánh cấp dưới) hoặc RESTRICT (báo lỗi nếu quyền đã được cấp tiếp cho bên thứ ba).")
    add_bullet("Khung nhìn (Views) như một cơ chế bảo mật: Che giấu các cột nhạy cảm (như Lương, Mật khẩu) hoặc chỉ lọc các dòng dữ liệu thỏa mãn điều kiện phòng ban của người dùng.")

    add_heading_2("3. Kiểm soát bắt buộc (MAC) và Phân quyền theo vai trò (RBAC) (Mục 30.3)")
    add_body("Mục 30.3 đi sâu so sánh giữa DAC và hai mô hình bảo mật cấp tiến hơn:")
    add_bullet("Kiểm soát truy cập bắt buộc (Mandatory Access Control - MAC): Áp dụng chính sách an ninh toàn cục do hệ thống bắt buộc, không phụ thuộc vào ý muốn của chủ sở hữu đối tượng. Tiêu biểu là Mô hình An ninh đa cấp Bell-LaPadula với 4 cấp bậc an ninh: Top Secret (TS) > Secret (S) > Confidential (C) > Unclassified (U). Mô hình thực thi 2 nguyên lý thép:\n"
               "  + Simple Security Property ('No Read Up'): Chủ thể chỉ được đọc đối tượng có cấp độ an ninh nhỏ hơn hoặc bằng cấp độ của mình (Class(S) >= Class(O)).\n"
               "  + Star-Property (*-Property - 'No Write Down'): Chủ thể chỉ được ghi dữ liệu vào đối tượng có cấp độ lớn hơn hoặc bằng cấp độ của mình (Class(S) <= Class(O)), ngăn chặn rò rỉ thông tin mật xuống cấp thấp.\n"
               "  + Hiện tượng Đa thể hiện (Polyinstantiation): Cùng một khóa chính nhưng tồn tại nhiều phiên bản dữ liệu ở các cấp độ an ninh khác nhau để chống lộ tin suy diễn.")
    add_bullet("Mô hình Phân quyền dựa trên Vai trò (Role-Based Access Control - RBAC): Chuẩn mực vàng trong quản trị CSDL doanh nghiệp. Quyền hạn không gán trực tiếp cho từng cá nhân mà gán cho các Vai trò (Roles). Người dùng được gán vào vai trò tương ứng với chức trách công việc. RBAC hỗ trợ phân cấp vai trò (Role Hierarchy) và Phân tách nhiệm vụ (Separation of Duties - SoD) chống xung đột lợi ích nội bộ.")

    add_heading_2("4. Lỗ hổng SQL Injection và Kỹ thuật phòng chống toàn diện (Mục 30.4)")
    add_body("SQL Injection (SQLi) là một trong những hiểm họa an ninh CSDL nghiêm trọng nhất (liên tục đứng trong danh sách OWASP Top 10):")
    add_bullet("Nguyên nhân cốt lõi: Ứng dụng nhận dữ liệu từ người dùng và ghép chuỗi trực tiếp (String Concatenation) vào câu lệnh SQL mà không qua kiểm tra cú pháp.")
    add_bullet("Các kỹ thuật tấn công điển hình:\n"
               "  + Vượt qua xác thực (Tautology / Auth Bypass): Sử dụng payload như \"' OR '1'='1' --\" biến mệnh đề WHERE luôn luôn đúng và loại bỏ kiểm tra mật khẩu.\n"
               "  + Tấn công ghép hợp UNION: Dùng mệnh đề UNION SELECT để trích xuất dữ liệu từ các bảng nhạy cảm khác trong CSDL.\n"
               "  + Tấn công Piggybacked: Chèn dấu chấm phẩy \";\" để thực thi thêm câu lệnh độc hại (ví dụ: \"; DROP TABLE DON_HANG; --\").\n"
               "  + Tấn công mù (Blind SQLi): Khai thác dựa trên độ trễ thời gian (Time-based) hoặc phản hồi logic đúng/sai (Boolean-based).")
    add_bullet("Giải pháp phòng thủ toàn diện:\n"
               "  + Sử dụng 100% Truy vấn Tham số hóa (Parameterized Queries / Prepared Statements): Database engine biên dịch trước cấu trúc lệnh; dữ liệu người dùng đưa vào chỉ được hiểu là giá trị chuỗi thuần túy (Literal Value), hoàn toàn vô hiệu hóa khả năng thay đổi cây cú pháp SQL.\n"
               "  + Áp dụng các thư viện ORM tiêu chuẩn và nguyên tắc Đặc quyền tối thiểu (Least Privilege).")

    add_heading_2("5. An toàn CSDL thống kê và Kiểm soát luồng thông tin (Mục 30.5 & 30.6)")
    add_body("Mục 30.5 & 30.6 nghiên cứu các dạng tấn công tinh vi:")
    add_bullet("Tấn công suy diễn trong CSDL thống kê (Inference Attacks): Kẻ tấn công lợi dụng các câu lệnh hàm tổng hợp (COUNT, AVG, SUM) kết hợp các điều kiện lọc hẹp để suy luận ra dữ liệu cá nhân đơn lẻ. Biện pháp phòng chống: Giới hạn kích cỡ truy vấn (Query-set size control: k <= |Q| <= N - k) và đưa nhiễu ngẫu nhiên vào dữ liệu (Differential Privacy).")
    add_bullet("Kiểm soát luồng thông tin (Flow Control) và Kênh bí mật (Covert Channels): Ngăn chặn rò rỉ dữ liệu qua các kênh liên lạc ngầm bất thường (Covert Storage Channel và Covert Timing Channel).")

    add_heading_2("6. Mã hóa CSDL, Băm mật khẩu có Salt và PKI (Mục 30.7)")
    add_body("Mục 30.7 trình bày các kỹ thuật mật mã học hiện đại ứng dụng trong CSDL:")
    add_bullet("Mã hóa đối xứng (Symmetric Encryption): Chuẩn AES-256 với tốc độ cao, dùng mã hóa dữ liệu khối lượng lớn.")
    add_bullet("Mã hóa bất đối xứng (Asymmetric Encryption): Thuật toán RSA sử dụng cặp khóa công khai và bí mật, phục vụ chữ ký số (Digital Signatures) và thiết lập kênh truyền an toàn SSL/TLS.")
    add_bullet("Băm mật khẩu (Hashing) & Chuỗi ngẫu nhiên (Salt): Mật khẩu người dùng bắt buộc phải được băm một chiều bằng SHA-256 kèm chuỗi Salt ngẫu nhiên riêng biệt, vô hiệu hóa hoàn toàn các cuộc tấn công tra cứu từ điển trước bằng Rainbow Table.")
    add_bullet("Mã hóa dữ liệu tĩnh (Transparent Data Encryption - TDE): Tự động mã hóa tệp dữ liệu .mdf và tệp log .ldf trên ổ đĩa cứng, bảo vệ CSDL khi máy chủ vật lý hoặc file sao lưu bị đánh cắp.")

    add_heading_2("7. Bảo vệ quyền riêng tư và Thách thức hiện đại (Mục 30.8 - 30.10)")
    add_body("Giáo trình thảo luận các công nghệ tiên tiến bảo vệ quyền riêng tư người dùng:")
    add_bullet("Kỹ thuật ẩn danh hóa: Mô hình k-Anonymity (mỗi bản ghi không thể phân biệt được với ít nhất k-1 cá nhân khác), l-Diversity (bảo đảm tính đa dạng của thuộc tính nhạy cảm), và t-Closeness.")
    add_bullet("Row-Level Security (RLS) & Oracle Label-Based Security: Cơ chế phân quyền dữ liệu mức hàng ngay tại tầng Database Engine. Khi người dùng thực thi truy vấn, hệ thống tự động chèn vị từ bảo mật (Security Predicate), đảm bảo người dùng chỉ xem được các dòng dữ liệu thuộc quyền hạn của mình một cách hoàn toàn trong suốt.")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG V: XÂY DỰNG ỨNG DỤNG DEMO VÀ THỰC NGHIỆM AN NINH CSDL
    # =========================================================================
    add_heading_1("CHƯƠNG V. XÂY DỰNG ỨNG DỤNG DEMO VÀ THỰC NGHIỆM AN NINH CSDL")

    add_heading_2("1. Kiến trúc ứng dụng TechStore Cyber Security Lab")
    add_body("Để hiện thực hóa và chứng minh tính đúng đắn của toàn bộ lý thuyết Chương 30, nhóm đã thiết kế và xây dựng thành công ứng dụng thực nghiệm Web 'TechStore Cyber Security Lab' (mã nguồn đặt tại thư mục 03_Demo_Security_App):")
    add_bullet("Backend: Nền tảng Python Flask tốc độ cao, tích hợp SQLite/T-SQL Engine mô phỏng kiến trúc CSDL TechStoreDB.")
    add_bullet("Frontend: Giao diện Web Dashboard hiện đại phong cách Dark Cyber Security, hỗ trợ các nút Quick Payload giúp thao tác kiểm thử trực quan, nhanh chóng.")
    add_bullet("Cơ chế triển khai: Khởi chạy 1-click tiện lợi qua file 'run_demo.bat' hoặc lệnh 'python app.py'.")

    add_heading_2("2. Thực nghiệm 1: Khai thác và Phòng thủ SQL Injection (Mục 30.4)")
    add_body("Kịch bản 1: Vượt qua xác thực đăng nhập (Authentication Bypass):\n"
             "- Ở chế độ 'Lỗ hổng' (Ghép chuỗi SQL động): Kẻ tấn công nhập username: admin' -- và mật khẩu ngẫu nhiên: batky123.\n"
             "- Câu lệnh thực thi ngầm: SELECT * FROM USERS WHERE username = 'admin' --' AND password_hash = 'batky123'\n"
             "- Kết quả thực nghiệm: Hệ thống loại bỏ toàn bộ mệnh đề kiểm tra mật khẩu bằng dấu comment '--'. Kẻ tấn công đăng nhập trái phép thành công với tư cách Tổng Giám Đốc (ADMIN), đọc được toàn bộ thông tin nhạy cảm và mức lương 35,000,000 VNĐ.\n"
             "- Ở chế độ 'An toàn' (Prepared Statement): Hệ thống tham số hóa đầu vào qua câu lệnh SELECT * FROM USERS WHERE username = ?. Dấu nháy đơn và comment được xử lý như một chuỗi văn bản thông thường, đòn tấn công thất bại 100%, bảo vệ tuyệt đối an toàn CSDL.")

    add_body("Kịch bản 2: Trích xuất trái phép dữ liệu bằng UNION SQL Injection:\n"
             "- Tại ô tìm kiếm sản phẩm ở chế độ lỗ hổng, kẻ tấn công nhập payload:\n"
             "  ' UNION SELECT id, username, email, role, salary FROM USERS --\n"
             "- Kết quả thực nghiệm: Bảng kết quả tìm kiếm sản phẩm lập tức trả về toàn bộ dữ liệu tài khoản quản trị, vai trò và mức lương của nhân viên, gây rò rỉ dữ liệu nghiêm trọng. Khi chuyển sang chế độ Parameterized Query, đòn tấn công hoàn toàn bị vô hiệu hóa.")

    add_heading_2("3. Thực nghiệm 2: Mô phỏng Ma trận Phân quyền Vai trò (RBAC)")
    add_body("Ứng dụng xây dựng bảng điều khiển ma trận quyền hạn theo 4 vai trò: ADMIN, MANAGER, STAFF, CUSTOMER. Khi người dùng chọn vai trò và thực hiện hành động, hệ thống phản hồi chính xác mã trạng thái an ninh (200 OK - Access Granted; 403 Forbidden - Access Denied; hoặc cảnh báo Row-Level Security chỉ cho phép xem đơn hàng của chính mình).")

    add_heading_2("4. Thực nghiệm 3: Băm mật khẩu, Tấn công Rainbow Table & Mã hóa AES-256")
    add_body("Phòng thí nghiệm cho phép người dùng nhập mật khẩu kiểm thử để so sánh trực quan:")
    add_bullet("Mật khẩu MD5: Với các mật khẩu phổ biến ('123456', 'admin'), hệ thống tra cứu và bẻ khóa ngay lập tức qua Rainbow Table giả lập trong vòng 0.001 giây, chứng minh MD5 hoàn toàn mất an toàn.")
    add_bullet("Mật khẩu SHA-256 + Unique Salt: Chuỗi băm kết hợp Salt ngẫu nhiên tạo ra giá trị băm độc nhất, vô hiệu hóa hoàn toàn bảng tra cứu sẵn và bảo vệ mật khẩu an toàn tuyệt đối.")
    add_bullet("Mã hóa thẻ tín dụng: Mô phỏng mã hóa đối xứng AES-256 chuyển số thẻ '4111 2222 3333 4444' thành bản mã Base64 lưu trong CSDL, kết hợp cơ chế che dữ liệu Dynamic Data Masking '4111 **** **** 4444' trên giao diện.")

    add_heading_2("5. Thực nghiệm 4: Triển khai kịch bản T-SQL trên SQL Server")
    add_body("File 'SQLServer_Security_Scripts.sql' cung cấp toàn bộ mã lệnh T-SQL tiêu chuẩn chạy trực tiếp trên SQL Server Management Studio (SSMS):")
    add_bullet("Tạo Database Roles và cấp quyền: Cấp quyền SELECT cho Role_NhanVienBanHang, đồng thời dùng lệnh DENY SELECT ON NHAN_VIEN(LuongCoBan) để ngăn chặn tuyệt đối nhân viên xem lương cấp trên.")
    add_bullet("Triển khai Dynamic Data Masking (DDM): Che số điện thoại khách hàng bằng hàm partial(3, 'XXXXXX', 2) và che Email bằng hàm email().")
    add_bullet("Triển khai Row-Level Security (RLS): Tạo Security Predicate Function và Security Policy trên bảng DON_HANG dựa trên SESSION_CONTEXT. Khi đăng nhập là KH001, khách hàng chỉ thấy duy nhất các đơn hàng của chính mình, bảo vệ tính riêng tư tuyệt đối.")

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG VI: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
    # =========================================================================
    add_heading_1("CHƯƠNG VI. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_heading_2("1. Kết quả đạt được của Đồ án")
    add_body("Sau quá trình làm việc nghiêm túc, khoa học và phối hợp chặt chẽ giữa các thành viên, nhóm đã hoàn thành toàn diện 100% tất cả các yêu cầu do Giảng viên giao cho bài tập đồ án giữa kỳ:")
    add_bullet("Phần 1: Thiết kế hoàn chỉnh CSDL TechStore gồm 10 thực thể chặt chẽ; chuyển đổi lược đồ quan hệ theo chuẩn giáo trình; chứng minh toán học toàn bộ các quan hệ đạt chuẩn cao BCNF; cài đặt thành công trên Microsoft SQL Server với đầy đủ ràng buộc toàn vẹn, dữ liệu mẫu logic và bộ sưu tập 25+ câu truy vấn phức tạp (JOIN, GROUP BY, HAVING, Window functions, View, Procedure, Trigger).")
    add_bullet("Phần 2: Hoàn thành báo cáo chuyên đề nghiên cứu sâu sắc Chương 30 (Database Security) bám sát cấu trúc giáo trình 'Fundamentals of Database Systems' (7E), làm sáng tỏ các mô hình DAC, MAC, RBAC, phân tích lỗ hổng SQL Injection và các kỹ thuật mật mã học hiện đại.")
    add_bullet("Phần 3: Xây dựng thành công ứng dụng Web Demo Cyber Security Lab trực quan, ấn tượng, giúp trực quan hóa sinh động các kịch bản an ninh CSDL thực tế.")
    add_bullet("Phần 4: Đóng gói tài liệu báo cáo chuẩn mẫu PTIT, thiết kế Slide PowerPoint thuyết trình chuyên nghiệp và phát hành toàn bộ mã nguồn lên kho lưu trữ GitHub.")

    add_heading_2("2. Hướng phát triển trong tương lai")
    add_bullet("Nghiên cứu ứng dụng Trí tuệ Nhân tạo và Machine Learning trong việc phát hiện bất thường truy vấn CSDL theo thời gian thực (Database Anomaly Detection).")
    add_bullet("Triển khai công nghệ Always Encrypted trên SQL Server Enterprise để mã hóa dữ liệu ngay từ tầng Client mà DBA cũng không thể đọc được nội dung bản rõ.")
    add_bullet("Tích hợp tường lửa ứng dụng Web (WAF) và hệ thống phát hiện xâm nhập ModSecurity bảo vệ toàn diện hệ thống.")

    doc.add_page_break()

    # =========================================================================
    # TÀI LIỆU THAM KHẢO
    # =========================================================================
    add_heading_1("TÀI LIỆU THAM KHẢO")
    refs = [
        "[1] Ramez Elmasri and Shamkant B. Navathe (2016), 'Fundamentals of Database Systems', 7th Edition, Pearson Education. (Đặc biệt là Chapter 30: Database Security, pp. 1121 - 1162).",
        "[2] ThS. Tuyết Hải (2022), 'Bài giảng môn học Cơ sở dữ liệu', Học viện Công nghệ Bưu chính Viễn thông - Cơ sở TP. Hồ Chí Minh.",
        "[3] Microsoft Learn (2024), 'SQL Server Security Documentation: Row-Level Security, Dynamic Data Masking, Transparent Data Encryption (TDE), and Permissions Hierarchy', Microsoft Corporation.",
        "[4] OWASP Foundation (2023), 'OWASP Top 10 - A03:2021 Injection & SQL Injection Prevention Cheat Sheet', Open Web Application Security Project.",
        "[5] National Institute of Standards and Technology (NIST) (2015), 'Special Publication 800-162: Guide to Attribute Based Access Control (ABAC) and Role-Based Access Control (RBAC) Definition', U.S. Department of Commerce.",
        "[6] David E. Bell and Leonard J. LaPadula (1976), 'Secure Computer System: Unified Exposition and Multics Interpretation', Technical Report ESD-TR-75-306, The MITRE Corporation."
    ]
    for r in refs:
        p = doc.add_paragraph()
        set_para_spacing(p, before=4, after=6, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r_run = p.add_run(r)
        set_font(r_run, size=12)

    # Save DOCX
    out_docx = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/04_BaoCao_Report/Bao_Cao_Do_An_Mon_Hoc_CSDL.docx"
    doc.save(out_docx)
    print(f">>> Đã xuất file Báo cáo Word thành công tại: {out_docx}")

    # Convert to PDF via Word COM
    out_pdf = "d:/HK1 2025-2026/cơ sở dữ liệu/do an co so du lieu/04_BaoCao_Report/Bao_Cao_Do_An_Mon_Hoc_CSDL.pdf"
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        doc_com = word.Documents.Open(os.path.abspath(out_docx))
        # 17 = wdFormatPDF
        doc_com.SaveAs(os.path.abspath(out_pdf), FileFormat=17)
        doc_com.Close()
        word.Quit()
        print(f">>> Đã chuyển đổi sang PDF thành công bằng Word COM tại: {out_pdf}")
    except Exception as e:
        print(f"Lỗi khi chuyển Word sang PDF: {e}")

if __name__ == '__main__':
    create_report()
