import streamlit as st
from openai import OpenAI
import base64
import io
from PIL import Image

st.set_page_config(page_title="DeepSeek V4 Chat", page_icon="🤖")
# CSS สำหรับจัด layout ให้สวย
st.markdown("""
<style>
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    .stFileUploader > div {
        display: flex;
        justify-content: center;
    }
    button[data-testid="baseButton-secondary"] {
        background-color: transparent;
        border: 1px solid #ddd;
        border-radius: 20px;
        font-size: 20px;
        padding: 5px 12px;
    }
</style>
""", unsafe_allow_html=True)
st.title("🤖 DeepSeek V4 Chat - อ่านรูปได้")

# ตรวจ API Key
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("กรุณาใส่ DEEPSEEK_API_KEY ใน Secrets")
    st.stop()

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1/v1"
)

# เริ่มต้น session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงแชทย้อนหลัง
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"], width=200)
        st.markdown(msg["content"])

# สร้าง container สำหรับ input แบบมีปุ่ม +
with st.container():
    col1, col2 = st.columns([0.9, 0.1])
    
    with col2:
        # ปุ่ม + ไว้แนบรูป
        uploaded_file = st.file_uploader(
            "➕", 
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="uploader"
        )
    
    with col1:
        prompt = st.chat_input("พิมพ์ข้อความ...")

# ตรวจสอบว่ามีรูปที่เพิ่งอัปโหลดไหม
if uploaded_file is not None:
    # อ่านและแปลงรูป
    image = Image.open(uploaded_file)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # แจ้งว่ามีรูปแล้ว
    st.success(f"✅ แนบรูป: {uploaded_file.name}")
    
    # เก็บรูปไว้ใน session
    st.session_state.uploaded_image = uploaded_file
    st.session_state.uploaded_image_base64 = img_base64

# ส่งข้อความ
if prompt:
    # สร้าง content สำหรับ API
    content = [{"type": "text", "text": prompt}]
    
    # ถ้ามีรูปที่อัปโหลดไว้
    if "uploaded_image_base64" in st.session_state and st.session_state.uploaded_image_base64:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{st.session_state.uploaded_image_base64}"
            }
        })
    
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        if "uploaded_image" in st.session_state and st.session_state.uploaded_image:
            st.image(st.session_state.uploaded_image, width=200)
        st.markdown(prompt)
    
    # เรียก API (ใช้ DeepSeek รองรับรูป)
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # เปลี่ยนเป็น deepseek-chat เพราะรองรับ vision
            messages=[{"role": "user", "content": content}],
            max_tokens=2000
        )
        reply = response.choices[0].message.content
        
        # แสดงคำตอบ
        with st.chat_message("assistant"):
            st.markdown(reply)
        
        # บันทึกประวัติ
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "image": st.session_state.uploaded_image if "uploaded_image" in st.session_state else None
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "image": None
        })
        
        # ล้างรูปที่อัปโหลด
        if "uploaded_image" in st.session_state:
            del st.session_state.uploaded_image
            del st.session_state.uploaded_image_base64
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
