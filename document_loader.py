import fitz  # PyMuPDF
import docx
import os
import io

def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def load_document(file_path):
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    return ""

def load_all_documents_from_folder(folder="uploads"):
    full_text = ""
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith((".pdf", ".docx")):
            full_text += f"\n\n--- [{filename}] ---\n\n"
            full_text += load_document(path)
    return full_text
