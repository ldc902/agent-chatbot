import os
import requests
import hashlib

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st

from utils.constants import PROVIDERS, API_URL

def apply_customCSS(path="./css/styles.css"):
    with open(path, "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
apply_customCSS()

def get_file_hash(file):
    return hashlib.sha256(file.getvalue()).hexdigest()

def check_files():
    result = requests.get(
        f"{API_URL}/api/chat/files/check"
    ).json()
    
    is_exist_files = result["status"]
    
    return is_exist_files

is_exist_files = check_files()

if __name__ == "__main__":  # nghĩa là mã bên dưới chỉ thực thi khi dùng file này làm main
    # quản lý trạng thái
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "uploaded_file_hash" not in st.session_state:
        st.session_state.uploaded_file_hash = None

    st.set_page_config(page_title="AI Chatbot", page_icon="🧠", layout="centered")
    st.title("🧠 AI Chatbot")
    st.caption("Ask any question based on your uploaded knowledge documents.")

    # SIDEBAR SETTINGS
    with st.sidebar:
        st.header("🧠 Chatbot Settings")
        chat_mode = st.radio("🧠 Select Chatbot Mode:", ["Normal Chatbot", "PDF Chatbot"])

        # Normal Chatbot settings
        if chat_mode == "Normal Chatbot":
            provider = st.radio("🔌 Choose LLM Provider:", list(PROVIDERS.keys()), index=0)
            model = st.selectbox("🧠 Select Model:", PROVIDERS[provider])
            use_web = st.checkbox("🌐 Allow web search", value=False)
            
            st.subheader("⚙️ Custom Prompt Template")
            
            custom_prompt = st.text_area(
                "Define your own prompt template:",
                height=150,
                placeholder="e.g. You are a helpful medical assistant. Only use the context provided..."
            )
            
        elif chat_mode == "PDF Chatbot":
            model = st.selectbox("🧠 Select Model:", PROVIDERS["Groq"])
            # file = st.file_uploader("📄 Upload your PDF file", type=["pdf"])
        
        st.markdown(f"**Mode:** `{chat_mode}`")
        
        if chat_mode == "Normal Chatbot":
            st.markdown(f"""
            **Provider:** `{provider}`  
            **Model:** `{model}`  
            **Web Search Enabled:** `{use_web}`  
            """)
            if use_web:
                st.markdown("**🌐 Web Search Enabled**")
        
        st.markdown("---")
        st.markdown("✉️ [cuongld.ai@gmail.com](mailto:cuongld.ai@gmail.com)")
        
    # PDF UPLOAD    
    if chat_mode == "PDF Chatbot":
        file = st.file_uploader("📄 Upload your PDF file", type=["pdf"])
        
        if file is not None:
            file_hash = get_file_hash(file)
             
            # Kiểm tra file đã upload chưa
            if file_hash != st.session_state.uploaded_file_hash:
                with st.spinner("Uploading PDF..."):
                    result = requests.post(f"{API_URL}/api/upload", files={"file": file})
                
                if result.status_code == 200:
                    if result.headers.get("content-type", "").startswith("application/json"):
                        result = result.json()
                        
                    if result["status"]:
                        # vì streamlit rerun toàn bộ script khi có tương tác với widget
                        st.session_state.uploaded_file_hash = file_hash
                        
                        is_exist_files = check_files()
                        
                        st.success("PDF uploaded successfully!")
                        st.write("Filename:", result["data"]["filename"])
                    
                    else:
                        st.error(f"Upload failed: {result["message"]}")
                
                else:
                    st.error(f"Upload failed: {result.text}")
                        
    # CHAT INPUT
    with st.form("chat_input", clear_on_submit = True):
        query = st.text_input("💬 Ask your medical question:", placeholder="E.g. What are the symptoms of hypertension?", disabled = not is_exist_files)
        
        submitted = st.form_submit_button("Send message", disabled = not is_exist_files)

        if submitted:
            if not query.strip():
                st.warning("❗Please enter a valid question.")
            else:
                with st.spinner("🤖 Thinking..."):
                    try:
                        if chat_mode == "Normal Chatbot":
                            payload = {
                                "model_name": model,
                                "provider": provider.lower(),
                                "allow_search": use_web,
                                "query": query,
                            }
                            
                            result = requests.post(f"{API_URL}/api/chat/normal-chat", json = payload)
                            
                            if result.headers.get("content-type", "").startswith("application/json"):
                                result = result.json()
                                
                                if result["status"]:
                                    response = result["data"].strip()
                                    if response:
                                        st.session_state.chat_history.append({"user": query, "bot": response})
                                else:
                                    st.error("❌ No response from model.")
                        
                        # PDF Chatbot mode        
                        elif chat_mode == "PDF Chatbot":  
                            payload = {
                                "model_name": model,
                                "query": query,
                            }
                            
                            result = requests.post(f"{API_URL}/api/chat/pdf-chat", json = payload)
                            
                            if result.headers.get("content-type", "").startswith("application/json"):
                                result = result.json()
                            
                                if result["status"]:
                                    response = result["data"]["response"].strip()
                                    sources = result["data"]["sources"]
                                    
                                    if response:
                                        st.session_state.chat_history.append({"user": query, "bot": response})
                                        
                                        if sources:
                                            with st.expander("📚 Source Chunks"):
                                                for i, chunk in enumerate(sources, 1):
                                                    st.markdown(f"**Chunk {i}:** `{chunk['metadata'].get('source', 'Unknown')}`")
                                                    st.code(chunk["page_content"].strip())       
                    except Exception as e:
                        st.error(f"🚨 An error occurred: {e}")
                            
    # Display chat history
    for pair in st.session_state.chat_history[::-1]:
        for role, msg in pair.items():
            css_class = "user-msg" if role == "user" else "bot-msg"
            st.markdown(f"<div class='{css_class}'>{msg}</div>", unsafe_allow_html=True)
    
