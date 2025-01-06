
# 📘 Microsoft Teams Member Adder

Một ứng dụng GUI đơn giản giúp bạn thêm thành viên vào nhóm Microsoft Teams từ danh sách mã sinh viên. Ứng dụng hỗ trợ dán mã sinh viên, chuyển đổi thành email, và thêm vào nhóm chỉ trong vài bước.

---

## 🛠️ **Tính Năng**

1. **Nhập URL Nhóm Teams:**
   - Cho phép dán URL từ clipboard.
   - Tự động trích xuất `groupId` và `tenantId` từ URL.

2. **Nhập Mã Sinh Viên:**
   - Dán danh sách mã sinh viên trực tiếp.
   - Tự động chuyển đổi thành email dạng `xxx@student.humg.edu.vn`.
   - Hỗ trợ **Ctrl+A** và nút **Xóa Dữ Liệu**.

3. **Thêm Thành Viên:**
   - Gửi danh sách email đến nhóm Microsoft Teams.
   - Hiển thị thông báo trạng thái thêm thành viên thành công.

4. **Giao Diện Thân Thiện:**
   - Giao diện hiện đại với **ttkbootstrap**.
   - Hiển thị logo ở cuối giao diện.

---

## 📋 **Yêu Cầu**

1. **Hệ Điều Hành:** Windows.  
2. **Quyền Hạn:** Tài khoản Microsoft Teams có quyền Admin nhóm.  
3. **Môi Trường:** Không cần cài đặt Python, chỉ cần chạy file `.exe`.

---

## 🚀 **Hướng Dẫn Sử Dụng**

### **1️⃣ Tải Về Ứng Dụng**

- Tải file `TeamsBulkUserAdder-2.0.0.zip`.
- Giải nén file vào một thư mục.

### **2️⃣ Chạy Ứng Dụng**

- Mở file `Tool-add-Teams.exe`.

### **3️⃣ Sử Dụng**

1. **Dán URL Nhóm Teams:**
   - Sao chép URL nhóm từ Microsoft Teams.
   - Dán vào ô "URL Nhóm Teams".

   Ví dụ URL:
   ```
   https://teams.microsoft.com/l/team/19%3ApMEo98y41F1jZ1J1V8AElvzr-IztEwmiYnRdGCK6-Lg1%40thread.tacv2/conversations?groupId=abc123-def456&tenantId=xyz789
   ```

2. **Nhập Mã Sinh Viên:**
   - Sao chép danh sách mã sinh viên từ Excel hoặc tài liệu.
   - Dán vào bảng nhập liệu. Mỗi dòng chứa một mã sinh viên.

   Ví dụ:
   ```
   2121051xxx
   2121051xxx
   2121051xxx
   ```

3. **Thêm Thành Viên:**
   - Nhấn nút "🚀 Thêm Thành Viên".
   - Ứng dụng sẽ tự động chuyển mã sinh viên thành email và thêm vào nhóm.

4. **Xóa Dữ Liệu:**
   - Sử dụng nút "🗑️ Xóa" để xóa URL.
   - Sử dụng nút "🗑️ Xóa Dữ Liệu" để xóa bảng mã sinh viên.

---

## 🛠️ **Cách Hoạt Động**

1. **Trích Xuất `groupId` và `tenantId`:**
   - Ứng dụng sử dụng regex để lấy thông tin từ URL nhóm.

2. **Xác Thực Device Code:**
   - Yêu cầu đăng nhập qua [Device Login](https://microsoft.com/devicelogin).

3. **Thêm Thành Viên Qua API:**
   - Gửi danh sách email đến Microsoft Teams qua Microsoft Graph API.

---

## 📦 **Phân Phối**

1. **File Phân Phối:** `Tool-add-Teams.exe` (đóng gói với PyInstaller).  
2. **Tệp Đính Kèm:** `logo.png` (nếu có).  
3. **Tài Liệu Hướng Dẫn:** `README.md`.

---

## 🛡️ **Hỗ Trợ**

Nếu gặp lỗi hoặc cần hỗ trợ, vui lòng liên hệ:

- **Email:** phamhonghiep.humg@gmail.com  
- **GitHub:** [GitHub Repository](#)

---

## 🛑 **Cảnh Báo**

- Đảm bảo bạn có quyền Admin nhóm trước khi sử dụng ứng dụng.  
- Không chia sẻ token hoặc thông tin xác thực với bất kỳ ai.  

---

**✨ Chúc bạn sử dụng ứng dụng hiệu quả! ✨**
