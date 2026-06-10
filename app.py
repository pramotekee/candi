import streamlit as st
from openai import OpenAI
import io
import tempfile
import os
import platform
from pathlib import Path

# ไลบรารีสำหรับอ่านไฟล์
import PyPDF2
from docx import Document
import pandas as pd
from PIL import Image

# ตั้งค่า OCR สำหรับ Streamlit Cloud
try:
    import pytesseract
    from pdf2image import convert_from_path
    
    # ตั้งค่า path ของ Tesseract สำหรับ Cloud (Linux)
    if platform.system() == "Linux":
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    else:
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    st.sidebar.warning("⚠️ OCR ไม่พร้อมใช้งาน (ติดตั้ง pytesseract และ pdf2image ใน requirements.txt)")

st.set_page_config(page_title="POPZILAR CHAT", page_icon="🤖")
st.title("POPZILAR TALK")

# ตรวจ API Key
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("กรุณาใส่ API Key ใน Secrets")
    st.stop()

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

# ========== ฟังก์ชันอ่านไฟล์ ==========
def read_pdf(file_bytes):
    text = ""
    try:
        pdf = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except:
        pass
    
    # ถ้าอ่านไม่ออก (PDF สแกน) และมี OCR
    if not text.strip() and OCR_AVAILABLE:
        with st.spinner("📸 OCR กำลังอ่าน PDF สแกน..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
                    f.write(file_bytes)
                    temp_path = f.name
                
                images = convert_from_path(temp_path, dpi=150)
                for img in images:
                    text += pytesseract.image_to_string(img, lang='eng+tha') + "\n"
                os.unlink(temp_path)
            except:
                text = "[ไม่สามารถอ่าน PDF สแกนได้]"
    
    return text if text.strip() else "[ไม่พบข้อความใน PDF]"

def read_docx(file_bytes):
    try:
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        return "[อ่านไฟล์ DOCX ไม่ได้]"

def read_txt(file_bytes):
    try:
        return file_bytes.decode("utf-8")
    except:
        return file_bytes.decode("latin-1", errors="ignore")

def read_csv(file_bytes):
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        return df.to_string()
    except:
        return "[อ่าน CSV ไม่ได้]"

def read_excel(file_bytes):
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))
        return df.to_string()
    except:
        return "[อ่าน Excel ไม่ได้]"

def read_image(file_bytes):
    if not OCR_AVAILABLE:
        return "[OCR ไม่พร้อมใช้งาน]"
    try:
        img = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(img, lang='eng+tha')
        return text if text.strip() else "[ไม่พบข้อความในรูป]"
    except:
        return "[อ่านรูปภาพไม่ได้]"

def extract_content(file):
    name = file.name.lower()
    data = file.read()
    
    if name.endswith('.pdf'):
        return read_pdf(data)
    elif name.endswith('.docx'):
        return read_docx(data)
    elif name.endswith('.txt') or name.endswith('.md') or name.endswith('.py'):
        return read_txt(data)
    elif name.endswith('.csv'):
        return read_csv(data)
    elif name.endswith(('.xlsx', '.xls')):
        return read_excel(data)
    elif name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return read_image(data)
    else:
        return f"[ไม่รองรับไฟล์ {name.split('.')[-1]}]"

# ========== UI ==========
st.sidebar.header("📎 อัปโหลดไฟล์")
st.sidebar.markdown("รองรับ PDF, DOCX, TXT, CSV, Excel, รูปภาพ (OCR)")

files = st.sidebar.file_uploader(
    "เลือกไฟล์ (หลายไฟล์ได้)",
    type=["pdf", "docx", "txt", "csv", "xlsx", "xls", "png", "jpg", "jpeg", "md", "py"],
    accept_multiple_files=True
)

file_contents = []
if files:
    for f in files:
        content = extract_content(f)
        file_contents.append(f"### 📄 {f.name}\n```\n{content[:5000]}\n```")
        st.sidebar.success(f"✅ {f.name} อ่านแล้ว ({len(content)} ตัวอักษร)")

# ประวัติแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ช่องพิมพ์
prompt = st.chat_input("พิมพ์ข้อความ หรือถามเกี่ยวกับไฟล์...")

if prompt:
    with st.chat_message("user"):
        if file_contents:
            st.write(f"📎 {len(files)} ไฟล์")
        st.write(prompt)
    
    # รวมไฟล์เข้า prompt
    final_prompt = prompt
    if file_contents:
        final_prompt = "📁 ไฟล์ที่อัปโหลด:\n\n" + "\n\n".join(file_contents) + f"\n\nคำถาม: {prompt}"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": final_prompt}],
            max_tokens=4000
        )
        
        reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(reply)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
    except Exception as e:
        st.error(f"ผิดพลาด: {e}")
