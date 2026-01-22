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