import streamlit as st
from openai import OpenAI
import base64
import io
from PIL import Image

st.set_page_config(page_title="DeepSeek V4 Chat", page_icon="🤖")
st.title("🤖 DeepSeek V4 Chat (อ่านรูปได้)")

# ตรวจสอบ API Key
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("กรุณาใส่ DEEPSEEK_API_KEY ใน Secrets ของ Streamlit")
    st.stop()

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

# เริ่มต้นประวัติแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

# เก็บรูปที่อัปโหลดชั่วคราว
if "temp_image" not in st.session_state:
    st.session_state.temp_image = None
    st.session_state.temp_image_base64 = None

# แสดงข้อความทั้งหมด
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=200)
        if "text" in msg:
            st.markdown(msg["text"])

# ส่วนอัปโหลดรูป (ใช้ sidebar หรือ放在上面)
with st.sidebar:
    st.subheader("📷 อัปโหลดรูป")
    uploaded_file = st.file_uploader("เลือกไฟล์รูป", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="รูปที่คุณจะส่ง", width=200)
        
        # แปลงเป็น base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        st.session_state.temp_image = uploaded_file
        st.session_state.temp_image_base64 = img_base64
        st.success("✅ พร้อมส่งแล้ว! พิมพ์ข้อความด้านล่าง")

# ช่องพิมพ์ข้อความ
prompt = st.chat_input("พิมพ์คำถามเกี่ยวกับรูป (ถ้ามี) หรือถามอะไรก็ได้...")

if prompt:
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        if st.session_state.temp_image_base64:
            st.image(st.session_state.temp_image, width=200)
        st.markdown(prompt)
    
    # เตรียมข้อมูลส่ง API
    content = [{"type": "text", "text": prompt}]
    
    if st.session_state.temp_image_base64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{st.session_state.temp_image_base64}"}
        })
    
    # บันทึกประวัติ
    st.session_state.messages.append({
        "role": "user",
        "text": prompt,
        "image": st.session_state.temp_image if st.session_state.temp_image_base64 else None
    })
    
    # เรียก API
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": content}]
        )
        reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(reply)
        
        st.session_state.messages.append({
            "role": "assistant",
            "text": reply,
            "image": None
        })
        
        # ล้างรูป临时
        st.session_state.temp_image = None
        st.session_state.temp_image_base64 = None
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
