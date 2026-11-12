/* ==========================================================================
   TECHSTORE CYBER SECURITY LAB - INTERACTIVE JAVASCRIPT
   ========================================================================== */

// 1. CHUYỂN ĐỔI TAB GIAO DIỆN
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.add('active');
    }

    event.currentTarget.classList.add('active');
}

// 2. CẬP NHẬT GIAO DIỆN CHẾ ĐỘ ĐĂNG NHẬP
function updateModeUI() {
    const mode = document.querySelector('input[name="loginMode"]:checked').value;
    const queryBox = document.getElementById('loginQueryBox');
    if (mode === 'vulnerable') {
        queryBox.style.borderColor = '#EF4444';
    } else {
        queryBox.style.borderColor = '#10B981';
    }
}

// 3. SET PAYLOAD CHO FORM ĐĂNG NHẬP
function setLoginPayload(username, password) {
    document.getElementById('loginUsername').value = username;
    document.getElementById('loginPassword').value = password;
}

// 4. XỬ LÝ SUBMIT ĐĂNG NHẬP (SQL INJECTION DEMO)
async function submitLoginDemo() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const mode = document.querySelector('input[name="loginMode"]:checked').value;

    const queryCode = document.getElementById('loginQueryCode');
    const resultBox = document.getElementById('loginResultBox');

    resultBox.innerHTML = '<div class="alert alert-warning"><i class="fa-solid fa-spinner fa-spin"></i> Đang phân tích cú pháp SQL...</div>';

    try {
        const response = await fetch('/api/sqli-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, mode })
        });
        const data = await response.json();

        // Hiển thị câu lệnh SQL
        queryCode.innerText = data.query;
        if (mode === 'vulnerable') {
            queryCode.style.color = '#F87171';
        } else {
            queryCode.style.color = '#34D399';
        }

        // Hiển thị kết quả
        if (data.is_attack_success) {
            resultBox.innerHTML = `
                <div class="alert alert-danger">
                    <h4><i class="fa-solid fa-triangle-exclamation"></i> TẤN CÔNG THÀNH CÔNG! (SQL INJECTION EXPLOITED)</h4>
                    <p>Kẻ tấn công đã vượt qua xác thực bằng mệnh đề logic luôn đúng và bỏ qua mật khẩu bằng ký tự comment <code>--</code>.</p>
                    <div style="margin-top: 8px;">
                        <strong>Đăng nhập trái phép thành công với tài khoản:</strong>
                        <ul style="margin-left: 20px; margin-top: 4px;">
                            <li>Họ tên: <strong>${data.user.full_name}</strong></li>
                            <li>Vai trò: <span class="role-badge role-admin">${data.user.role}</span></li>
                            <li>Email: ${data.user.email}</li>
                            <li>Lương cơ bản bí mật: <strong>${data.user.salary.toLocaleString()} VNĐ</strong></li>
                        </ul>
                    </div>
                </div>
            `;
        } else if (data.success) {
            resultBox.innerHTML = `
                <div class="alert alert-success">
                    <h4><i class="fa-solid fa-circle-check"></i> ĐĂNG NHẬP HỢP LỆ</h4>
                    <p>Chào mừng <strong>${data.user.full_name}</strong> (Vai trò: ${data.user.role}).</p>
                </div>
            `;
        } else {
            const extra = mode === 'secure' ? ' (Prepared Statement đã ngăn chặn triệt để payload tấn công - tham số được cô lập)' : '';
            resultBox.innerHTML = `
                <div class="alert alert-warning">
                    <h4><i class="fa-solid fa-circle-xmark"></i> ĐĂNG NHẬP THẤT BẠI${extra}</h4>
                    <p>Tài khoản hoặc mật khẩu không chính xác.</p>
                </div>
            `;
        }
    } catch (e) {
        resultBox.innerHTML = `<div class="alert alert-danger">Lỗi kết nối máy chủ: ${e}</div>`;
    }
}

// 5. SET PAYLOAD CHO FORM TÌM KIẾM
function setSearchPayload(keyword) {
    document.getElementById('searchKeyword').value = keyword;
}

// 6. XỬ LÝ TÌM KIẾM (UNION SQL INJECTION DEMO)
async function submitSearchDemo() {
    const keyword = document.getElementById('searchKeyword').value;
    const mode = document.querySelector('input[name="searchMode"]:checked').value;

    const queryCode = document.getElementById('searchQueryCode');
    const tableBox = document.getElementById('searchResultsBox');

    tableBox.innerHTML = '<div class="alert alert-warning"><i class="fa-solid fa-spinner fa-spin"></i> Đang thực thi...</div>';

    try {
        const response = await fetch('/api/sqli-search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword, mode })
        });
        const data = await response.json();

        queryCode.innerText = data.query;

        if (data.error) {
            tableBox.innerHTML = `<div class="alert alert-danger"><i class="fa-solid fa-triangle-exclamation"></i> Lỗi cú pháp SQL: ${data.error}</div>`;
            return;
        }

        if (data.results.length === 0) {
            tableBox.innerHTML = `<div class="alert alert-warning">Không tìm thấy bản ghi nào phù hợp.</div>`;
            return;
        }

        let html = `
            <table class="rbac-table" style="margin-top: 10px;">
                <thead>
                    <tr>
                        <th>Cột 1 (ID)</th>
                        <th>Cột 2 (Mã / Username)</th>
                        <th>Cột 3 (Tên SP / Email)</th>
                        <th>Cột 4 (Danh mục / Role)</th>
                        <th>Cột 5 (Giá bán / Lương)</th>
                    </tr>
                </thead>
                <tbody>
        `;

        data.results.forEach(r => {
            const isLeaked = (typeof r.col4 === 'string' && (r.col4 === 'ADMIN' || r.col4 === 'MANAGER' || r.col4 === 'STAFF'));
            const highlightClass = isLeaked ? 'style="background: rgba(239, 68, 68, 0.15); font-weight: bold;"' : '';
            html += `
                <tr ${highlightClass}>
                    <td>${r.col1}</td>
                    <td>${r.col2}</td>
                    <td>${r.col3}</td>
                    <td>${r.col4}</td>
                    <td>${r.col5.toLocaleString()}</td>
                </tr>
            `;
        });

        html += `</tbody></table>`;

        if (mode === 'vulnerable' && data.results.some(r => r.col4 === 'ADMIN' || r.col4 === 'MANAGER')) {
            html = `<div class="alert alert-danger" style="margin-bottom: 10px;">
                <i class="fa-solid fa-skull"></i> <strong>CẢNH BÁO RÒ RỈ DỮ LIỆU:</strong> Kẻ tấn công đã dùng kỹ thuật <code>UNION SELECT</code> để đọc trộm toàn bộ danh sách tài khoản, vai trò và mức lương nhân sự từ bảng USERS!
            </div>` + html;
        }

        tableBox.innerHTML = html;
    } catch (e) {
        tableBox.innerHTML = `<div class="alert alert-danger">Lỗi kết nối: ${e}</div>`;
    }
}

// 7. KIỂM THỬ PHÂN QUYỀN RBAC
async function testRBACPermission() {
    const role = document.getElementById('rbacRoleSelect').value;
    const action = document.getElementById('rbacActionSelect').value;
    const box = document.getElementById('rbacFeedbackBox');

    try {
        const response = await fetch('/api/rbac-check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role, action })
        });
        const data = await response.json();

        let alertClass = 'alert-danger';
        let icon = 'fa-ban';
        let title = 'TỪ CHỐI TRUY CẬP (ACCESS DENIED)';

        if (data.allowed === true) {
            alertClass = 'alert-success';
            icon = 'fa-circle-check';
            title = 'CHO PHÉP TRUY CẬP (ACCESS GRANTED)';
        } else if (data.allowed === 'own_only') {
            alertClass = 'alert-warning';
            icon = 'fa-filter';
            title = 'QUYỀN TRUY CẬP CÓ ĐIỀU KIỆN (ROW-LEVEL SECURITY)';
        }

        box.innerHTML = `
            <div class="alert ${alertClass}">
                <h4><i class="fa-solid ${icon}"></i> ${title}</h4>
                <p style="margin-top: 6px;">${data.message}</p>
                <div style="margin-top: 12px; font-size: 0.82rem; color: #E2E8F0;">
                    <strong>Chi tiết chính sách cho vai trò [${data.role}]:</strong>
                    <pre style="margin-top: 6px;"><code>${JSON.stringify(data.all_permissions, null, 2)}</code></pre>
                </div>
            </div>
        `;
    } catch (e) {
        box.innerHTML = `<div class="alert alert-danger">Lỗi kết nối: ${e}</div>`;
    }
}

// 8. PHÒNG THÍ NGHIỆM BĂM MẬT KHẨU
async function runHashLab() {
    const password = document.getElementById('hashInputPwd').value;
    const salt = document.getElementById('hashInputSalt').value;

    try {
        const response = await fetch('/api/hash-lab', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password, salt })
        });
        const data = await response.json();

        document.getElementById('md5Output').innerText = data.md5;
        document.getElementById('sha256Output').innerText = data.sha256;
        document.getElementById('saltedSha256Output').innerText = data.salted_sha256;

        const md5Status = document.getElementById('md5Status');
        if (data.md5_cracked) {
            md5Status.className = 'status-tag status-danger';
            md5Status.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Tìm thấy trong Rainbow Table: "${data.md5_cracked}"`;
        } else {
            md5Status.className = 'status-tag status-safe';
            md5Status.innerText = 'Chưa có trong từ điển mẫu';
        }
    } catch (e) {
        console.error(e);
    }
}

// 9. MÃ HÓA THẺ TÍN DỤNG & MASKING
async function runEncryptCard() {
    const cardNumber = document.getElementById('cardInput').value;
    const key = document.getElementById('keyInput').value;

    try {
        const response = await fetch('/api/encrypt-card', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_number: cardNumber, key: key })
        });
        const data = await response.json();

        document.getElementById('maskedCardOutput').innerText = data.masked_card;
        document.getElementById('cipherOutput').innerText = data.ciphertext;
        document.getElementById('decryptedOutput').innerText = data.decrypted;
    } catch (e) {
        console.error(e);
    }
}

// Khởi chạy ngầm các tính toán khi tải trang
document.addEventListener('DOMContentLoaded', () => {
    updateModeUI();
    runHashLab();
    runEncryptCard();
});
