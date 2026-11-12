import os
import sqlite3
import hashlib
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = "techstore_secret_security_key"

DB_FILE = os.path.join(os.path.dirname(__file__), "techstore_demo.db")

def init_demo_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. Bảng USERS phục vụ Demo SQL Injection & RBAC
    c.execute("DROP TABLE IF EXISTS USERS")
    c.execute("""
    CREATE TABLE USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL DEFAULT 0
    )
    """)
    
    # Dữ liệu tài khoản mẫu
    sample_users = [
        ('admin',     hashlib.sha256(('admin123' + 'salt_admin').encode()).hexdigest(), 'salt_admin', 'Trương Công Định', 'admin@techstore.vn', 'ADMIN', 35000000),
        ('manager',   hashlib.sha256(('manager123' + 'salt_mgr').encode()).hexdigest(),   'salt_mgr',   'Nguyễn Thúy Hằng', 'hang@techstore.vn',  'MANAGER', 22000000),
        ('staff',     hashlib.sha256(('staff123' + 'salt_stf').encode()).hexdigest(),     'salt_stf',   'Lê Thị Hương',     'huong@techstore.vn', 'STAFF', 10500000),
        ('customer1', hashlib.sha256(('cust123' + 'salt_c1').encode()).hexdigest(),       'salt_c1',    'Nguyễn Văn An',    'an.nguyen@gmail.com','CUSTOMER', 0),
        ('customer2', hashlib.sha256(('cust456' + 'salt_c2').encode()).hexdigest(),       'salt_c2',    'Trần Bích Ngọc',   'ngoc@gmail.com',     'CUSTOMER', 0)
    ]
    c.executemany("INSERT INTO USERS (username, password_hash, salt, full_name, email, role, salary) VALUES (?, ?, ?, ?, ?, ?, ?)", sample_users)
    
    # 2. Bảng SAN_PHAM
    c.execute("DROP TABLE IF EXISTS SAN_PHAM")
    c.execute("""
    CREATE TABLE SAN_PHAM (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ma_sp TEXT UNIQUE NOT NULL,
        ten_sp TEXT NOT NULL,
        danh_muc TEXT NOT NULL,
        gia_ban REAL NOT NULL,
        so_luong_ton INTEGER NOT NULL
    )
    """)
    sample_products = [
        ('SP01', 'iPhone 15 Pro Max 256GB', 'Điện thoại', 31990000, 25),
        ('SP02', 'MacBook Pro 16 inch M3 Max', 'Laptop', 74990000, 10),
        ('SP03', 'Samsung Galaxy S24 Ultra', 'Điện thoại', 30490000, 18),
        ('SP04', 'Dell XPS 15 9530', 'Laptop', 48990000, 12),
        ('SP05', 'ASUS ROG Zephyrus G16', 'Laptop', 58990000, 8),
        ('SP06', 'iPad Pro 11 inch M4', 'Máy tính bảng', 27990000, 15),
        ('SP07', 'Tai nghe Sony WH-1000XM5', 'Âm thanh', 8190000, 30),
        ('SP08', 'Chuột Logitech MX Master 3S', 'Phụ kiện', 2690000, 45)
    ]
    c.executemany("INSERT INTO SAN_PHAM (ma_sp, ten_sp, danh_muc, gia_ban, so_luong_ton) VALUES (?, ?, ?, ?, ?)", sample_products)

    # 3. Bảng DON_HANG
    c.execute("DROP TABLE IF EXISTS DON_HANG")
    c.execute("""
    CREATE TABLE DON_HANG (
        ma_dh TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        tong_tien REAL NOT NULL,
        ngay_dat TEXT NOT NULL,
        trang_thai TEXT NOT NULL
    )
    """)
    sample_orders = [
        ('DH001', 'customer1', 31990000, '2024-05-10', 'Hoàn thành'),
        ('DH002', 'customer2', 30490000, '2024-05-15', 'Hoàn thành'),
        ('DH003', 'customer1', 2690000,  '2024-06-01', 'Đang giao hàng'),
        ('DH004', 'customer2', 8190000,  '2024-06-20', 'Chờ xác nhận')
    ]
    c.executemany("INSERT INTO DON_HANG (ma_dh, username, tong_tien, ngay_dat, trang_thai) VALUES (?, ?, ?, ?, ?)", sample_orders)

    conn.commit()
    conn.close()

# Khởi tạo CSDL khi chạy ứng dụng
init_demo_db()

@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------------------------------
# API 1: XỬ LÝ ĐĂNG NHẬP (SQL INJECTION VULNERABLE VS SECURE)
# ---------------------------------------------------------------------------
@app.route("/api/sqli-login", methods=["POST"])
def sqli_login():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    mode = data.get("mode", "vulnerable")  # 'vulnerable' hoặc 'secure'
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    raw_query = ""
    error_msg = None
    user_info = None
    
    if mode == "vulnerable":
        # Ghép chuỗi nguy hiểm (Lỗ hổng SQL Injection)
        raw_query = f"SELECT id, username, full_name, email, role, salary FROM USERS WHERE username = '{username}' AND password_hash = '{password}'"
        try:
            c.execute(raw_query)
            row = c.fetchone()
            if row:
                user_info = {
                    "id": row[0], "username": row[1], "full_name": row[2],
                    "email": row[3], "role": row[4], "salary": row[5]
                }
        except Exception as e:
            error_msg = str(e)
    else:
        # Cơ chế an toàn: Prepared Statement / Parameterized Query
        raw_query = "SELECT id, username, password_hash, salt, full_name, email, role, salary FROM USERS WHERE username = ?"
        try:
            c.execute(raw_query, (username,))
            row = c.fetchone()
            if row:
                db_hash = row[2]
                db_salt = row[3]
                # Kiểm tra băm an toàn
                input_hash = hashlib.sha256((password + db_salt).encode()).hexdigest()
                if input_hash == db_hash:
                    user_info = {
                        "id": row[0], "username": row[1], "full_name": row[4],
                        "email": row[5], "role": row[6], "salary": row[7]
                    }
        except Exception as e:
            error_msg = str(e)
            
    conn.close()
    
    return jsonify({
        "mode": mode,
        "query": raw_query,
        "success": user_info is not None,
        "user": user_info,
        "error": error_msg,
        "is_attack_success": (mode == "vulnerable" and user_info is not None and password != "admin123" and password != "manager123")
    })

# ---------------------------------------------------------------------------
# API 2: XỬ LÝ TÌM KIẾM SẢN PHẨM (UNION BASED SQL INJECTION)
# ---------------------------------------------------------------------------
@app.route("/api/sqli-search", methods=["POST"])
def sqli_search():
    data = request.get_json() or {}
    keyword = data.get("keyword", "")
    mode = data.get("mode", "vulnerable")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    raw_query = ""
    results = []
    error_msg = None
    
    if mode == "vulnerable":
        raw_query = f"SELECT id, ma_sp, ten_sp, danh_muc, gia_ban FROM SAN_PHAM WHERE ten_sp LIKE '%{keyword}%'"
        try:
            c.execute(raw_query)
            rows = c.fetchall()
            for r in rows:
                results.append({"col1": r[0], "col2": r[1], "col3": r[2], "col4": r[3], "col5": r[4]})
        except Exception as e:
            error_msg = str(e)
    else:
        raw_query = "SELECT id, ma_sp, ten_sp, danh_muc, gia_ban FROM SAN_PHAM WHERE ten_sp LIKE ?"
        try:
            c.execute(raw_query, (f"%{keyword}%",))
            rows = c.fetchall()
            for r in rows:
                results.append({"col1": r[0], "col2": r[1], "col3": r[2], "col4": r[3], "col5": r[4]})
        except Exception as e:
            error_msg = str(e)
            
    conn.close()
    return jsonify({
        "mode": mode,
        "query": raw_query,
        "results": results,
        "error": error_msg
    })

# ---------------------------------------------------------------------------
# API 3: ROLE-BASED ACCESS CONTROL (RBAC) LAB
# ---------------------------------------------------------------------------
ROLE_PERMISSIONS = {
    "ADMIN": {
        "view_products": True,
        "edit_products": True,
        "view_orders": True,
        "delete_orders": True,
        "view_salaries": True,
        "manage_users": True
    },
    "MANAGER": {
        "view_products": True,
        "edit_products": True,
        "view_orders": True,
        "delete_orders": False,
        "view_salaries": True,
        "manage_users": False
    },
    "STAFF": {
        "view_products": True,
        "edit_products": False,
        "view_orders": True,
        "delete_orders": False,
        "view_salaries": False,
        "manage_users": False
    },
    "CUSTOMER": {
        "view_products": True,
        "edit_products": False,
        "view_orders": "own_only",
        "delete_orders": False,
        "view_salaries": False,
        "manage_users": False
    }
}

@app.route("/api/rbac-check", methods=["POST"])
def rbac_check():
    data = request.get_json() or {}
    role = data.get("role", "CUSTOMER")
    action = data.get("action", "view_products")
    
    perms = ROLE_PERMISSIONS.get(role, {})
    allowed = perms.get(action, False)
    
    msg = ""
    if allowed is True:
        msg = f"QUYỀN HỢP LỆ (200 OK): Vai trò [{role}] được phép thực hiện hành động [{action}]."
    elif allowed == "own_only":
        msg = f"QUYỀN CÓ ĐIỀU KIỆN (RLS): Vai trò [{role}] chỉ được xem dữ liệu do chính mình sở hữu."
    else:
        msg = f"TỪ CHỐI TRUY CẬP (403 Forbidden): Vai trò [{role}] KHÔNG có quyền thực hiện hành động [{action}]!"
        
    return jsonify({
        "role": role,
        "action": action,
        "allowed": allowed,
        "message": msg,
        "all_permissions": perms
    })

# ---------------------------------------------------------------------------
# API 4: PASSWORD HASHING & ENCRYPTION LAB
# ---------------------------------------------------------------------------
@app.route("/api/hash-lab", methods=["POST"])
def hash_lab():
    data = request.get_json() or {}
    pwd = data.get("password", "")
    salt = data.get("salt", "techstore_salt_2024")
    
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    sha256_hash = hashlib.sha256(pwd.encode()).hexdigest()
    salted_sha256 = hashlib.sha256((pwd + salt).encode()).hexdigest()
    
    # Giả lập từ điển tra cứu Rainbow Table
    rainbow_dict = {
        hashlib.md5("123456".encode()).hexdigest(): "123456",
        hashlib.md5("password".encode()).hexdigest(): "password",
        hashlib.md5("admin".encode()).hexdigest(): "admin",
        hashlib.md5("qwerty".encode()).hexdigest(): "qwerty",
        hashlib.md5("techstore".encode()).hexdigest(): "techstore"
    }
    
    md5_cracked = rainbow_dict.get(md5_hash, None)
    
    return jsonify({
        "plaintext": pwd,
        "salt": salt,
        "md5": md5_hash,
        "md5_cracked": md5_cracked,
        "sha256": sha256_hash,
        "salted_sha256": salted_sha256
    })

# ---------------------------------------------------------------------------
# API 5: AES SYMMETRIC ENCRYPTION (XOR/B64 Clean Sim)
# ---------------------------------------------------------------------------
@app.route("/api/encrypt-card", methods=["POST"])
def encrypt_card():
    data = request.get_json() or {}
    card_number = data.get("card_number", "")
    key = data.get("key", "SECRET_KEY_256")
    
    # Biến đổi giả lập AES Block cipher (XOR + Base64) minh họa trực quan
    cipher_bytes = bytearray()
    key_bytes = key.encode()
    for i, b in enumerate(card_number.encode()):
        cipher_bytes.append(b ^ key_bytes[i % len(key_bytes)])
    ciphertext = base64.b64encode(cipher_bytes).decode()
    
    # Giải mã
    decrypted_bytes = bytearray()
    raw_cipher = base64.b64decode(ciphertext)
    for i, b in enumerate(raw_cipher):
        decrypted_bytes.append(b ^ key_bytes[i % len(key_bytes)])
    decrypted = decrypted_bytes.decode(errors='ignore')
    
    # Mặt nạ hiển thị (Dynamic Data Masking)
    if len(card_number) >= 8:
        masked = card_number[:4] + " **** **** " + card_number[-4:]
    else:
        masked = "****"
        
    return jsonify({
        "raw_card": card_number,
        "masked_card": masked,
        "ciphertext": ciphertext,
        "decrypted": decrypted
    })

if __name__ == "__main__":
    print(">>> Ứng dụng Demo Bảo mật TechStore đang khởi chạy tại http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)

