import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import quote
import json

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- 基礎環境變數設定 (預設值) ---
DEFAULT_CONFIG = {
    "BASE_URL": os.getenv("BASE_URL", "http://10.180.161.48/isharebackend"),
    "ADMIN_ID": os.getenv("ADMIN_ID", "service@amway.com"),
    "ADMIN_PW": os.getenv("ADMIN_PW", "system"),
}

class IShareUploader:
    def __init__(self, config=None, dry_run=False):
        self.config = config or DEFAULT_CONFIG
        self.dry_run = dry_run
        self.session = requests.Session()
        self.token = "MOCK_TOKEN" if dry_run else ""
        
        if self.dry_run:
            print("⚠️ 啟動 Dry Run 模式：不會真的連接伺服器或上傳檔案。")

    def login(self):
        """執行身分驗證"""
        if self.dry_run:
            print("[Mock] 模擬登入成功")
            return
            
        print("[Auth] 正在執行管理者登入...")
        try:
            res = self.session.get(f"{self.config['BASE_URL']}/Admin.aspx")
            soup = BeautifulSoup(res.text, 'html.parser')
            
            data = {
                "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"})['value'],
                "__VIEWSTATEGENERATOR": soup.find("input", {"name": "__VIEWSTATEGENERATOR"})['value'],
                "__EVENTVALIDATION": soup.find("input", {"name": "__EVENTVALIDATION"})['value'],
                "AdminID": self.config['ADMIN_ID'],
                "AdminPassword": self.config['ADMIN_PW'],
                "ButtonSubmit": "登入"
            }
            self.session.post(f"{self.config['BASE_URL']}/Admin.aspx", data=data)
            print("✅ 登入程序完成")
        except Exception as e:
            print(f"❌ 登入失敗: {e}")
            raise

    def refresh_token(self):
        """獲取 RequestVerificationToken"""
        if self.dry_run:
            self.token = "MOCK_VERIFICATION_TOKEN_12345"
            return

        url = f"{self.config['BASE_URL']}/Article/MonthlyPostSection/{self.config['MONTHLY_POST_ID']}"
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.token = soup.find("input", {"name": "__RequestVerificationToken"})['value']

    def upload_image_bytes(self, image_data, filename, content_type="image/jpeg"):
        """直接上傳二進位圖片數據 (記憶體內)"""
        if self.dry_run:
            print(f"[Mock] 模擬上傳記憶體圖片: {filename}")
            return f"http://mock-server/uploads/{filename}"

        files = {"files[]": (filename, image_data, content_type)}
        try:
            res = self.session.post(f"{self.config['BASE_URL']}/Page/PhotoUpload", files=files, timeout=30)
            if res.status_code == 200:
                return res.json().get("url")
            else:
                print(f"❌ 上傳失敗: {res.status_code} - {res.text}")
                return ""
        except Exception as e:
            print(f"❌ 上傳異常: {e}")
            return ""

    def upload_binary_image(self, file_path):
        """上傳圖片 (檔案路徑)"""
        if self.dry_run:
            print(f"[Mock] 模擬上傳圖片: {file_path}")
            return f"http://mock-server/uploads/{os.path.basename(file_path)}"

        with open(file_path, "rb") as f:
            files = {"files[]": (os.path.basename(file_path), f, "image/jpeg")}
            res = self.session.post(f"{self.config['BASE_URL']}/Page/PhotoUpload", files=files)
            print(f"[Debug] Response Text: {res.text}")
            return res.json().get("url")

    def build_section_payload(self, section_type, title, content, photo_url="", alt="", section_order=0):
        """通用 Payload 建構函數"""
        payload = [
            f"MonthlyPostID={self.config['MONTHLY_POST_ID']}",
            "SectionId=0",
            "PostSectionId=0",
            f"SectionOrder={section_order}",
            f"SectionType={section_type}",
            f"Template={section_type}"
        ]

        if section_type == 8:  # 純文字
            payload.extend([
                f"Title={quote(title)}",
                f"Content={quote(content)}"
            ])
        elif section_type == 1:  # 圖片
            payload.extend([
                f"Photo={photo_url}",
                "Url=",
                f"Alt={quote(alt)}",
                "Target=_blank"
            ])
        
        return "&".join(payload)

    def submit_data(self, data_items):
        """提交組合好的 data 陣列"""
        if self.dry_run:
            print("\n[Mock] 準備提交 Payload:")
            print(json.dumps(data_items, indent=2, ensure_ascii=False))
            print("✅ [Mock] 模擬提交成功")
            return

        self.refresh_token()
        
        payload = {
            "__RequestVerificationToken": self.token,
            "isPost": "true",
            "Id": self.config['MONTHLY_POST_ID'],
            "data": data_items
        }

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive"
        }
        # Reset headers to avoid accumulation
        self.session.headers.clear()
        self.session.headers.update(headers)
        api_url = f"{self.config['BASE_URL']}/Article/MonthlyPostSection/{self.config['MONTHLY_POST_ID']}"
        # Disable redirects to prevent loops
        response = self.session.post(api_url, data=payload, headers=headers, allow_redirects=False)

        if '"code":200' in response.text:
            print("✅ 批次組合上傳成功")
        else:
            print(f"❌ 上傳失敗，伺服器回應: {response.text}")
