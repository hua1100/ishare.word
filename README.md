# iShare Word Uploader (Word 上稿助手)

這是一個專為 iShare 平台設計的自動化上稿工具。它可以讓使用者上傳排版完成的 Word 文件 (`.docx`)，自動解析其中的文字、圖片與格式（如粗體、列表），並透過 API 發布至 iShare 系統。

## ✨ 功能特色

- **直覺介面**：使用 Streamlit 建構，操作簡單，支援拖放上傳。
- **精準解析**：保留 Word 中的段落、圖片、粗體、字體顏色與列表格式。
- **即時預覽**：上傳前可預覽解析後的圖文排版效果。
- **自動發布**：一鍵將內容同步至 iShare 月刊文章系統。

## 🛠️ 環境需求

- Python 3.10 或更高版本
- iShare 內網連線權限 (若需實際發布)

## 🚀 快速開始 (開發者模式)

### 1. 取得專案
```bash
git clone https://github.com/hua1100/ishare.word.git
cd ishare.word
```

### 2. 建立虛擬環境 (推薦使用 uv 或 venv)
```bash
# 使用 Python 原生 venv
python -m venv venv

# Mac/Linux 啟動虛擬環境
source venv/bin/activate

# Windows 啟動虛擬環境
.\venv\Scripts\activate
```

### 3. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 4. 設定環境變數 (.env)
請在專案根目錄建立 `.env` 檔案，填入以下資訊（可參考 `.env.example`）：
```ini
BASE_URL=http://Your-iShare-Backend-URL
ADMIN_ID=your_admin_account
ADMIN_PW=your_admin_password
```

### 5. 啟動應用程式
```bash
streamlit run word_uploader_app.py
```
啟動後，瀏覽器將自動開啟 `http://localhost:8501`。

## 📦 打包給同事使用 (Windows)

若需將程式打包成無需安裝 Python 的 `.exe` 執行檔，請參考 [iShare Word Uploader - Windows 打包教學.md](./iShare%20Word%20Uploader%20-%20Windows%20打包教學.md)。

簡單指令（需先安裝 pyinstaller）：
```bash
pyinstaller --onefile --additional-hooks-dir=. --hidden-import=streamlit --collect-all streamlit --copy-metadata streamlit --collect-all word_uploader_app --add-data "word_uploader_app.py;." --add-data ".env;." run_app.py
```

## 📁 專案結構

- `word_uploader_app.py`: 前端介面 (Streamlit)
- `publish_word.py`: Word 解析與上傳核心邏輯
- `backend_api.py`: 底層 API 連線處理
- `run_app.py`: PyInstaller 打包用的啟動腳本
