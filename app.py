import ttkbootstrap as tb  # Giao diện hiện đại
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox, scrolledtext, PhotoImage
import msal
import requests
import os
import json
import re
import webbrowser
import pyperclip  # pip install pyperclip
import time
# ----------------- CẤU HÌNH -----------------
TOKEN_CACHE_FILE = 'token_cache.json'
EMAIL_DOMAIN = "@student.humg.edu.vn"
LOGO_PATH = 'logo.png'  # Đường dẫn logo

# ----------------- LƯU/LOAD TOKEN -----------------
def load_token_cache():
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_token_cache(cache):
    with open(TOKEN_CACHE_FILE, 'w') as f:
        json.dump(cache, f)

# ----------------- TRÍCH XUẤT TENANT_ID & GROUP_ID -----------------
def extract_ids_from_url(url):
    pattern = r"groupId=([a-fA-F0-9\-]+)&tenantId=([a-fA-F0-9\-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    else:
        raise ValueError("❌ URL không hợp lệ. Vui lòng kiểm tra lại!")

# ----------------- XÁC THỰC VÀ LẤY TOKEN -----------------
def get_access_token(tenant_id):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.PublicClientApplication(
        client_id="d3590ed6-52b3-4102-aeff-aad2292ab01c",
        authority=authority
    )
    
    scopes = ["https://graph.microsoft.com/.default"]
    token_cache = load_token_cache()
    
    if token_cache:
        result = app.acquire_token_silent(scopes, account=None)
        if not result or 'access_token' not in result:
            result = app.acquire_token_by_refresh_token(
                refresh_token=token_cache.get('refresh_token'),
                scopes=scopes
            )
    
    if not token_cache or 'access_token' not in result:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise Exception("❌ Failed to initiate Device Code Flow.")
        
        pyperclip.copy(flow['user_code'])
        message = (
            f"🔑 Mở liên kết: {flow['verification_uri']}\n"
            f"Nhập mã xác thực: {flow['user_code']} (đã sao chép vào clipboard)."
        )
        messagebox.showinfo("Xác Thực Device Login", message)
        webbrowser.open(flow['verification_uri'])
        
        result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        save_token_cache(result)
        return result["access_token"]
    else:
        raise Exception(f"❌ Authentication failed: {result.get('error_description')}")

# ----------------- THÊM THÀNH VIÊN VÀO NHÓM -----------------
def add_member_to_group(email, access_token, group_id, delay=0.5, retry_delay=60, max_retries=3):
    """
    Thêm thành viên vào nhóm Microsoft Teams với xử lý lỗi TooManyRequests.
    
    Args:
        email (str): Địa chỉ email của thành viên.
        access_token (str): Token xác thực.
        group_id (str): ID của nhóm Teams.
        delay (float): Thời gian chờ giữa mỗi lần thêm (đơn vị: giây).
        retry_delay (int): Thời gian chờ khi gặp lỗi TooManyRequests (đơn vị: giây).
        max_retries (int): Số lần thử lại tối đa khi gặp lỗi TooManyRequests.
    
    Returns:
        str: 'added' nếu thêm thành công, 'exists' nếu người dùng đã tồn tại, 'failed' nếu lỗi khác.
    """
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/users/{email}"
    }
    
    retries = 0
    while retries <= max_retries:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 204, 201]:
            print(f"[SUCCESS] Đã thêm {email} vào nhóm.")
            time.sleep(delay)  # Nghỉ giữa các lần thêm
            return 'added'
        
        elif response.status_code == 400 and "already exist" in response.text:
            print(f"[INFO] Người dùng {email} đã tồn tại trong nhóm, bỏ qua.")
            time.sleep(delay)
            return 'exists'
        
        elif response.status_code == 429:  # TooManyRequests
            print(f"[WARNING] Quá nhiều yêu cầu. Chờ {retry_delay} giây trước khi thử lại.")
            time.sleep(retry_delay)
            retries += 1
        
        else:
            print(f"[ERROR] Không thể thêm {email}. Chi tiết: {response.text}")
            time.sleep(delay)
            return 'failed'
    
    print(f"[ERROR] Quá nhiều lần thử lại không thành công cho {email}.")
    return 'failed'

# ----------------- GUI TKINTER -----------------
class TeamsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔗 Công Cụ Thêm Thành Viên Teams")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # Header
        header = tb.Label(self.root, text="Công Cụ Thêm Thành Viên Teams", font=("Roboto", 16), bootstyle="primary")
        header.pack(pady=10)
        
        # URL Input + Clipboard Button + Clear Button
        url_frame = tb.Frame(self.root)
        url_frame.pack(pady=10)
        
        tb.Label(url_frame, text="🔗 URL Nhóm Teams:").pack(side=tk.LEFT, padx=5)
        self.url_entry = tb.Entry(url_frame, width=45)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        
        paste_button = tb.Button(url_frame, text="📋 Dán", bootstyle="secondary", command=self.paste_from_clipboard)
        paste_button.pack(side=tk.LEFT, padx=5)
        
        clear_url_button = tb.Button(url_frame, text="🗑️ Xóa", bootstyle="danger", command=self.clear_url)
        clear_url_button.pack(side=tk.LEFT, padx=5)
        
        # Student IDs Input + Clear Button
        tb.Label(self.root, text="📋 Dán Danh Sách Mã Sinh Viên:").pack(pady=5)
        self.student_ids_text = scrolledtext.ScrolledText(self.root, width=70, height=15)
        self.student_ids_text.pack(pady=5)
        
        # Hỗ trợ Ctrl+A
        self.student_ids_text.bind("<Control-a>", self.select_all)
        self.student_ids_text.bind("<Control-A>", self.select_all)
        
        clear_students_button = tb.Button(self.root, text="🗑️ Xóa Dữ Liệu", bootstyle="danger", command=self.clear_students)
        clear_students_button.pack(pady=5)
        
        # Run Button
        tb.Button(self.root, text="🚀 Thêm Thành Viên", command=self.start_process, bootstyle="success").pack(pady=20)
        
        # Status Label
        self.status_label = tb.Label(self.root, text="", bootstyle="info")
        self.status_label.pack(pady=5)
        
        # Logo at the bottom
        self.load_logo()
    
    def paste_from_clipboard(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, pyperclip.paste())
    
    def clear_url(self):
        self.url_entry.delete(0, tk.END)
    
    def clear_students(self):
        self.student_ids_text.delete('1.0', tk.END)
    
    def select_all(self, event):
        self.student_ids_text.tag_add(tk.SEL, "1.0", tk.END)
        self.student_ids_text.mark_set(tk.INSERT, "1.0")
        self.student_ids_text.see(tk.INSERT)
        return 'break'
    
    def start_process(self):
        """
        Hàm bắt đầu quy trình thêm thành viên với độ trễ và xử lý lỗi TooManyRequests.
        """
        try:
            url = self.url_entry.get()
            if not url:
                raise ValueError("URL không được để trống!")
            group_id, tenant_id = extract_ids_from_url(url)
            access_token = get_access_token(tenant_id)
            
            student_ids = self.student_ids_text.get("1.0", tk.END).strip().split("\n")
            emails = [f"{sid.strip()}{EMAIL_DOMAIN}" for sid in student_ids if sid.strip()]
            
            success_count = 0
            exists_count = 0
            failed_count = 0
            
            with open("already_exists.log", "w") as exists_log, open("failed_additions.log", "w") as failed_log:
                for email in emails:
                    status = add_member_to_group(email, access_token, group_id, delay=0.5, retry_delay=60, max_retries=3)
                    if status == 'added':
                        success_count += 1
                    elif status == 'exists':
                        exists_count += 1
                        exists_log.write(f"{email}\n")
                    else:
                        failed_count += 1
                        failed_log.write(f"{email}\n")
            
            self.status_label.config(
                text=f"✅ Thêm thành công: {success_count}, ⚠️ Đã tồn tại: {exists_count}, ❌ Lỗi: {failed_count}"
            )
            messagebox.showinfo(
                "Hoàn Thành", 
                f"Thêm thành công: {success_count}\nĐã tồn tại: {exists_count}\nLỗi: {failed_count}"
            )
        except Exception as e:
            self.status_label.config(text=str(e))
            messagebox.showerror("Lỗi", str(e))


    
    def load_logo(self):
        try:
            logo = PhotoImage(file=LOGO_PATH)
            logo_label = tb.Label(self.root, image=logo)
            logo_label.image = logo  # Giữ tham chiếu
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"Không thể tải logo: {e}")

# ----------------- CHẠY CHƯƠNG TRÌNH -----------------
if __name__ == "__main__":
    root = tb.Window(themename="litera")
    app = TeamsApp(root)
    root.mainloop()
