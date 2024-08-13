# 🚀 Công Cụ Thêm Thành Viên Hàng Loạt Cho Microsoft Teams

Repo này chứa một script PowerShell giúp bạn thêm nhiều thành viên vào một nhóm Microsoft Teams bằng cách đọc địa chỉ email từ một tệp văn bản.

## 📋 Yêu Cầu

Trước khi bắt đầu, hãy đảm bảo bạn đã đáp ứng các yêu cầu sau:

- 🖥️ Bạn đã cài đặt **PowerShell** trên máy tính Windows của mình.
- 👤 Bạn có quyền cần thiết (Owner hoặc Admin) để thêm thành viên vào một nhóm Microsoft Teams.
- 🔑 Bạn có một tài khoản Microsoft Teams đang hoạt động.
- 📦 Bạn đã cài đặt **Microsoft Teams PowerShell module**. Bạn có thể cài đặt bằng cách chạy lệnh sau trong PowerShell:

  ```powershell
  Install-Module -Name PowerShellGet -Force -AllowClobber
  Install-Module -Name MicrosoftTeams -Force -AllowClobber
  ```

## 🛠️ Hướng Dẫn Sử Dụng

### 1. 📑 Chuẩn Bị Danh Sách Email

1. Tạo một tệp văn bản (`emails.txt`) chứa các địa chỉ email của người dùng mà bạn muốn thêm vào nhóm Microsoft Teams.
2. Mỗi địa chỉ email nên được đặt trên một dòng riêng biệt. Ví dụ:

   ```
   user1@example.com
   user2@example.com
   user3@example.com
   ```

3. Lưu tệp ở một thư mục dễ truy cập, ví dụ: `C:\Users\Administrator\Downloads\`.

### 2. 🔍 Cách Lấy ID Nhóm (Group ID)

1. Truy cập Microsoft Teams và mở nhóm mà bạn muốn thêm thành viên.
2. Nhìn vào thanh địa chỉ URL của trình duyệt, bạn sẽ thấy một phần chứa `groupId`. Ví dụ:
   ```
   https://teams.microsoft.com/l/team/19%3Aexample%40thread.tacv2/conversations?groupId=abc123-def456-gh789&tenantId=xyz
   ```
3. Phần `groupId` trong URL chính là ID của nhóm. Sao chép đoạn ID này.

### 3. 🖥️ Sử Dụng PowerShell

1. Mở PowerShell trên máy tính của bạn.

2. Kết nối với tài khoản Microsoft Teams bằng lệnh sau:
   ```powershell
   Connect-MicrosoftTeams
   ```
   Một cửa sổ đăng nhập sẽ xuất hiện. Đăng nhập bằng tài khoản Microsoft Teams có quyền cần thiết để thêm thành viên vào nhóm.

### 4. ✍️ Viết Script Để Thêm Thành Viên

1. Tạo một script trên trình Editor (dùng Notepad cho nhanh) với nội dung như sau:

   ```powershell
   $emails = Get-Content "duong_dan_file_emails"
   $groupId = "id_group_ban_can_them"
   # Vai trò của thành viên (Member hoặc Owner)
   $role = "Member"  # Hoặc "Owner"
   foreach ($email in $emails) {
       Add-TeamUser -GroupId $groupId -User $email -Role $role
   }
   ```

2. Thay thế `"duong_dan_file_emails"` bằng đường dẫn đến tệp `emails.txt` của bạn. Ví dụ:
   ```powershell
   $emails = Get-Content "C:\Users\Administrator\Downloads\emails.txt"
   ```

3. Thay thế `"id_group_ban_can_them"` bằng `groupId` mà bạn đã sao chép ở bước trước. Ví dụ:
   ```powershell
   $groupId = "b2781ca1-60ba-4b7d-9a2e-5d1840621718"
   ```

4. Nếu cần, thay đổi `$role` thành `"Owner"` nếu bạn muốn thêm thành viên với quyền Owner.

### 5. ▶️ Chạy Script

Chạy script bằng cách dán nội dung bạn vừa soạn vào PowerShell và chạy chương trình bằng phím Enter. Chờ đến khi PowerShell chạy xong thì thoát chương trình.

### 6. ✅ Kiểm Tra

Sau khi script hoàn tất, bạn có thể kiểm tra lại trong Microsoft Teams để đảm bảo rằng các thành viên đã được thêm vào nhóm.

## 🛠️ Khắc Phục Sự Cố

Nếu bạn gặp phải vấn đề:

- 🔍 Đảm bảo rằng các địa chỉ email trong `emails.txt` là chính xác.
- 🔍 Kiểm tra lại `groupId` có đúng không.
- 🔍 Đảm bảo rằng bạn có quyền cần thiết để thêm thành viên vào nhóm.

Nếu gặp phải các vấn đề khác, bạn có thể mở một issue trong repo này để được hỗ trợ.

## 📄 Giấy Phép

Dự án này được cấp phép dưới giấy phép MIT - xem tệp [LICENSE](LICENSE) để biết thêm chi tiết.
