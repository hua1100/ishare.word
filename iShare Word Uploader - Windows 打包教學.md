iShare Word Uploader - Windows 打包教學
這份指南將協助您在公司 Windows 電腦上，將此 Python 程式打包成一個可獨立執行的 .exe 檔案，方便分享給同事使用。

步驟 1：準備檔案
請將以下檔案複製到公司電腦的一個新資料夾中（例如命名為 ishare_tool）：

word_uploader_app.py
 (主程式)
backend_api.py
 (API 模組)
publish_word.py
 (Word 解析模組)
.env
 (設定檔 - 請確認裡面有正確的 BASE_URL)
requirements.txt
 (剛剛幫您產生的套件清單)
步驟 2：安裝 Python 與套件
在公司電腦上打開 CMD (命令提示字元) 或 PowerShell，進入該資料夾，並執行以下指令：

# 1. 確保 pip 是最新的
python -m pip install --upgrade pip
# 2. 安裝必要套件
pip install -r requirements.txt
# 3. 安裝打包工具 PyInstaller
pip install pyinstaller
步驟 3：建立啟動腳本 (關鍵！)
因為 Streamlit 的架構比較特殊，直接打包 
.py
 檔變成 EXE 執行後會無法啟動。我們需要一個「啟動器」來幫忙執行。

請在同一個資料夾新增一個檔案，命名為 run_app.py，內容如下：

import streamlit.web.cli as stcli
import os, sys
def resolve_path(path):
    basedir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    return os.path.join(basedir, path)
if __name__ == "__main__":
    import sys
    # 設定目標 app 的路徑
    app_path = resolve_path("word_uploader_app.py")
    
    # 偽裝成 streamlit run 指令
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false"
    ]
    sys.exit(stcli.main())
步驟 4：執行打包指令
在終端機執行以下指令來開始打包（這會花一點時間）：

pyinstaller --onefile --additional-hooks-dir=. --hidden-import=streamlit --collect-all streamlit --copy-metadata streamlit --collect-all word_uploader_app --add-data "word_uploader_app.py;." --add-data ".env;." run_app.py
注意： 如果指令執行失敗，可以嘗試簡化版（可能會產生較多檔案，但較容易成功）： pyinstaller --onedir --add-data "word_uploader_app.py;." --add-data ".env;." run_app.py

步驟 5：完成！
打包完成後，您會在 dist 資料夾中看到 run_app.exe。 您可以將這個檔案重新命名為 iShare上傳小工具.exe，然後傳給同事即可！

同事如何使用？

收到 .exe 檔案。
確保他們電腦可以連上公司內網。
點兩下執行，瀏覽器會自動跳出操作介面。