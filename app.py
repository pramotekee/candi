import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

st.set_page_config(page_title="DeepSeek V4 Chat", page_icon="🤖")
st.title("🤖 DeepSeek Chat (ถาม+อ่านรูป)")

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

# อัปโหลดรูป (อยู่ข้างบน แบบชัดๆ)
uploaded_file = st.file_uploader("📷 แนบรูป (ถ้ามี)", type=["jpg", "png", "jpeg"])

# ช่องพิมพ์ข้อความ
prompt = st.chat_input("พิมพ์คำถาม...")

if prompt:
    # เตรียมรูป base64
    image_base64 = None
    if uploaded_file:
        img = Image.open(uploaded_file)
        buff = io.BytesIO()
        img.save(buff, format="PNG")
        image_base64 = base64.b64encode(buff.getvalue()).decode()
    
    # แสดงข้อความ+รูปในแชท
    with st.chat_message("user"):
        if uploaded_file:
            st.image(uploaded_file, width=200)
        st.write(prompt)
    
    # เรียก API
    try:
        if image_base64:
            # มีรูป -> ใช้ vision
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ]
                }]
            )
        else:
            # ไม่มีรูป -> แชทปกติ
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
        
        reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(reply)
        
        # บันทึก
        st.session_state.messages.append({"role": "user", "content": prompt, "image": uploaded_file})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        st.rerun()
        
    except Exception as e:
        st.error(f"ข้อผิดพลาด: {e}")
