import streamlit as st
from openai import OpenAI
import base64
import io
from PIL import Image

st.set_page_config(page_title="POPZILAR CHAT", page_icon="🤖")
st.title("POPZILAR CHAT")

# ตรวจ API Key
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("กรุณาใส่ API Key ใน Secrets")
    st.stop()

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

# ประวัติแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"], width=200)
        st.write(msg["content"])

# ช่องอัปโหลดรูปและข้อความ
col1, col2 = st.columns([1, 10])

with col1:
    uploaded_file = st.file_uploader("📎", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

with col2:
    prompt = st.chat_input("พิมพ์ข้อความ...")

# ถ้ามีการส่งข้อความ
if prompt:
    # แปลงรูป
    image_base64 = None
    uploaded_img = None
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        uploaded_img = uploaded_file
        buff = io.BytesIO()
        img.save(buff, format="PNG")
        image_base64 = base64.b64encode(buff.getvalue()).decode()
    
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        if uploaded_img:
            st.image(uploaded_img, width=200)
        st.write(prompt)
    
    # เรียก API
    try:
        if image_base64:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ]
                }],
                max_tokens=2000
            )
        else:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
        
        reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(reply)
        
        # บันทึกประวัติ
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "image": uploaded_img
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "image": None
        })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"ผิดพลาด: {str(e)}")
