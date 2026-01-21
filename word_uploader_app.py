import streamlit as st
from publish_word import WordUploader
import os

# --- Page Config ---
st.set_page_config(
    page_title="iShare Word Uploader", 
    page_icon="📄", 
    layout="wide"
)

# --- Design System Injection ---
FLAT_DESIGN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&display=swap');

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Force Light Mode Background */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Headings */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        color: #111827 !important;
    }
    
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    /* --- UI Elements Text Color Override --- */
    /* Target specific Streamlit UI text wrappers to force dark color */
    .stMarkdown p, .stText p, .stCaption, label, .stTextInput input {
        color: #111827;
    }
    
    /* IMPORTANT: Do NOT use !important on generic 'p' or 'span' 
       as it kills inline styles from the Word HTML preview. */

    /* Buttons */
    .stButton > button {
        background-color: #3B82F6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton > button p {
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        background-color: #2563EB !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #F3F4F6 !important;
        border: 2px solid transparent !important;
        color: #111827 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        background-color: #FFFFFF !important;
        border-color: #3B82F6 !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #F9FAFB;
        border: 2px dashed #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
        color: #6B7280 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #3B82F6 !important;
        border: 2px solid #3B82F6 !important;
    }
    
    [data-testid="stFileUploader"] button p {
        color: #3B82F6 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F3F4F6 !important;
        border-radius: 8px !important;
        color: #111827 !important;
    }
    
    .streamlit-expanderHeader p {
        color: #111827 !important;
    }

    /* Code Blocks - Multiple selectors to ensure override */
    [data-testid="stCodeBlock"],
    .stCodeBlock,
    pre,
    pre code,
    [data-testid="stExpander"] pre,
    [data-testid="stExpander"] code {
        background-color: #1F2937 !important;
        color: #F9FAFB !important;
    }
    
    /* Specific targeting for code elements */
    code {
        background-color: #1F2937 !important;
        color: #F9FAFB !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace !important;
    }
    
    /* Pre blocks (code containers) */
    pre {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    pre code {
        background-color: transparent !important;
        padding: 0 !important;
    }

    /* Dividers */
    hr {
        margin: 2rem 0 !important;
        border-top: 2px solid #E5E7EB !important;
    }
    
    /* Status/Alerts */
    .stAlert {
        background-color: #EFF6FF !important;
        border-radius: 8px !important;
    }
    .stAlert p { color: #1E40AF !important; }
    .stSuccess { background-color: #ECFDF5 !important; }
    .stSuccess p { color: #065F46 !important; }
    .stError { background-color: #FEF2F2 !important; }
    .stError p { color: #991B1B !important; }

    /* Hide Streamlit Toolbar (Deploy button) & Header */
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    header { visibility: hidden !important; }

</style>
"""
st.markdown(FLAT_DESIGN_CSS, unsafe_allow_html=True)

# --- Header Section ---
col_header_L, col_header_R = st.columns([2, 1])
with col_header_L:
    st.title("iShare Word 上稿助手")
    st.markdown("""
    <div style="margin-top: -1rem; margin-bottom: 2rem; color: #6B7280; font-size: 1.2rem; font-weight: 500;">
    簡潔、自信、完美保留 Word 格式。
    </div>
    """, unsafe_allow_html=True)

# --- Settings & Input Section ---
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 01. 設定參數")
        st.caption("設定目標月刊文章 ID")
        monthly_post_id = st.text_input("月刊文章 ID (Monthly Post ID)", value="42325", help="iShare 系統中的文章 ID")
        
        # Login Check in a more subtle way
        with st.expander("檢查連線狀態"):
            if st.button("測試伺服器連線", type="secondary"):
                 try:
                    # Quick dummy check logic or init uploader earlier
                    uploader = WordUploader(monthly_post_id) 
                    with st.spinner("正在連線..."):
                        uploader.login()
                        st.success("已成功連線至 iShare ✅")
                 except Exception as e:
                    st.error(str(e))

    with col2:
        st.markdown("### 02. 來源檔案")
        st.caption("上傳排版完成的 Word 文件 (.docx)")
        uploaded_file = st.file_uploader("拖曳檔案至此或點擊上傳", type=['docx'])

# --- Logic Section ---
if uploaded_file and monthly_post_id:
    st.divider()
    
    # Initialize Uploader
    uploader = WordUploader(monthly_post_id)
    
    # Process
    try:
        sections = uploader.process_docx(uploaded_file) # Assuming this works with BytesIO based on previous edits
        
        st.markdown(f"### 03. 預覽與發布 (共 {len(sections)} 個段落)")
        
        # Preview Area
        for i, section in enumerate(sections):
            # Using columns to create a card-like layout for each section
            with st.container():
                # Streamlit containers style handling is tricky, we use the CSS injected above 
                # to style containers with borders.
                
                c_lbl, c_content = st.columns([1, 4])
                with c_lbl:
                    st.markdown(f"**段落 {i+1:02d}**")
                    type_label = "圖片" if section['type'] == 'image' else "文字"
                    st.caption(type_label)
                
                with c_content:
                    if section['type'] == 'text':
                         st.markdown(section['content'], unsafe_allow_html=True)
                    elif section['type'] == 'image':
                         st.image(section['content'], width=400)
                
                st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

        st.divider()
        
        # Action Area
        col_act_1, col_act_2 = st.columns([2, 1])
        with col_act_1:
            st.info("準備好發布了嗎？注意：若 ID 相同將會覆蓋舊有內容。")
            
        with col_act_2:
            if st.button("🚀 確認發布至 iShare", type="primary", use_container_width=True):
                 with st.status("執行發布任務中...", expanded=True) as status:
                    st.write("正在驗證身份...")
                    try:
                        uploader.login()
                        st.write("正在上傳圖文內容...")
                        success, msg = uploader.upload_sections(sections)
                        
                        if success:
                            status.update(label="發布成功！", state="complete")
                            st.balloons()
                            st.success(f"{msg}")
                        else:
                            status.update(label="發布失敗", state="error")
                            st.error(msg)
                    except Exception as e:
                        st.error(f"系統錯誤: {e}")
                        status.update(label="系統發生錯誤", state="error")
                        
    except Exception as e:
        st.error(f"解析文件失敗: {e}")
