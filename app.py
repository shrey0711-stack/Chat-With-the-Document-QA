import streamlit as st
import os
import shutil

from document_loader import load_all_documents_from_folder
from gemini_api import query_gemini_with_history

# Constants
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Page config
st.set_page_config(page_title="📚 Gemini Chatbot", layout="wide")
st.title("📚 Chat with Your Documents (Gemini)")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# Upload section
uploaded_files = st.file_uploader(
    "Upload PDF or DOCX", type=["pdf", "docx"], accept_multiple_files=True
)

# Save uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
    st.success("📥 Files uploaded successfully.")
    st.session_state.document_text = load_all_documents_from_folder(UPLOAD_FOLDER)

# Auto-load documents if folder has files but no text loaded
if not st.session_state.document_text.strip() and os.listdir(UPLOAD_FOLDER):
    st.session_state.document_text = load_all_documents_from_folder(UPLOAD_FOLDER)
    st.info("📄 Loaded previously uploaded documents.")

# Sidebar controls
st.sidebar.title("🛠 Options")
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.success("💬 Chat history cleared.")

if st.sidebar.button("🧹 Delete Uploaded Files"):
    shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    st.session_state.document_text = ""
    st.success("🗂 All uploaded files deleted.")

if st.sidebar.button("🔄 Reload Documents"):
    if os.listdir(UPLOAD_FOLDER):
        st.session_state.document_text = load_all_documents_from_folder(UPLOAD_FOLDER)
        st.success("🔄 Documents reloaded from folder.")
    else:
        st.warning("⚠️ No documents found in the folder.")

# Chat section
st.markdown("### 💬 Chat")
for msg in st.session_state.chat_history:
    st.chat_message("user").markdown(msg["user"])
    st.chat_message("assistant").markdown(msg["gemini"])

# Chat input
prompt = st.chat_input("Ask something about the uploaded documents...")

if prompt:
    if st.session_state.document_text.strip():
        intro = f"The following documents were uploaded:\n\n{st.session_state.document_text}"
    else:
        intro = "No documents have been uploaded yet."

    # Prepare chat history for Gemini
    history = [{"role": "user", "parts": [{"text": intro}]}]
    for msg in st.session_state.chat_history:
        history.append({"role": "user", "parts": [{"text": msg['user']}]} )
        history.append({"role": "model", "parts": [{"text": msg['gemini']}]} )
    history.append({"role": "user", "parts": [{"text": prompt}]})

    with st.spinner("💡 Gemini is thinking..."):
        answer = query_gemini_with_history(history)

    st.session_state.chat_history.append({"user": prompt, "gemini": answer})
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown(answer)
