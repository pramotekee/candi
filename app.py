import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

st.set_page_config(page_title="DeepSeek V4 Chat", page_icon="🤖")
st.title("🤖 DeepSeek V4 Chat Box (อ่านรูปได้)")

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงข้อความเก่า
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for content in msg["content"]:
                if content["type"] == "text":
                    st.markdown(content["text"])
                elif content["type"] == "image_url":
                    st.image(content["image_url"]["url"])
        else:
            st.markdown(msg["content"])

# ช่องอัปโหลดรูป
uploaded_file = st.file_uploader("📷 อัปโหลดรูป (ถ้ามี)", type=["jpg", "jpeg", "png"])

# รับข้อความ
prompt = st.chat_input("พิมพ์คำถาม หรือ ถามเกี่ยวกับรูปได้เลย")

if prompt:
    # เตรียมข้อความ
    content = [{"type": "text", "text": prompt}]
    
    # ถ้ามีรูปที่อัปโหลด
    if uploaded_file is not None:
        # อ่านรูปเป็น base64
        image = Image.open(uploaded_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img_base64}"}
        })
    
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        if uploaded_file:
            st.image(uploaded_file, caption="รูปที่คุณส่ง")
        st.markdown(prompt)
    
    # บันทึกข้อความผู้ใช้
    st.session_state.messages.append({"role": "user", "content": content})
    
    # เรียก API
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": content}]
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
