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
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
    st.session_state.uploaded_image_data = None

# แสดงข้อความทั้งหมด
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user" and "image" in msg:
            st.image(msg["image"], caption="รูปที่คุณส่ง", width=200)
        st.markdown(msg["content"])

# ส่วนของ input แบบมีปุ่ม + (ใช้ columns เพื่อให้ดูเหมือนแชท)
col1, col2 = st.columns([6, 1])

with col1:
    prompt = st.chat_input("พิมพ์ข้อความ หรือ กด + เพื่อแนบรูป")

with col2:
    # ปุ่ม + สำหรับอัปโหลดรูป
    uploaded_file = st.file_uploader(
        "📎", 
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="image_uploader"
    )
    
    if uploaded_file is not None:
        # แปลงรูปเป็น base64
        image = Image.open(uploaded_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        st.session_state.uploaded_image = uploaded_file
        st.session_state.uploaded_image_data = img_base64
        st.success("✅ รูปพร้อมใช้งาน พิมพ์ข้อความแล้วส่งได้เลย")

# เวลาส่งข้อความ
if prompt:
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        if st.session_state.uploaded_image_data:
            st.image(st.session_state.uploaded_image, caption="รูปที่คุณส่ง", width=200)
        st.markdown(prompt)
    
    # เตรียม content สำหรับ API
    content = [{"type": "text", "text": prompt}]
    
    if st.session_state.uploaded_image_data:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{st.session_state.uploaded_image_data}"}
        })
    
    # บันทึกประวัติผู้ใช้
    user_msg = {"role": "user", "content": prompt}
    if st.session_state.uploaded_image_data:
        user_msg["image"] = st.session_state.uploaded_image
    st.session_state.messages.append(user_msg)
    
    # เรียก API
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": content}]
        )
        reply = response.choices[0].message.content
        
        # แสดงคำตอบ
        with st.chat_message("assistant"):
            st.markdown(reply)
        
        # บันทึกประวัติ
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # ล้างรูปที่อัปโหลด (หลังส่งแล้ว)
        st.session_state.uploaded_image = None
        st.session_state.uploaded_image_data = None
        st.rerun()
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
