import streamlit as st
from openai import OpenAI

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
        st.write(msg["content"])

# ช่องพิมพ์ข้อความ
prompt = st.chat_input("พิมพ์ข้อความ...")

if prompt:
    # แสดงข้อความผู้ใช้
    with st.chat_message("user"):
        st.write(prompt)
    
    # เรียก API
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        # ดึงข้อมูลจาก response
        model_name = response.model
        reply = response.choices[0].message.content
        
        # แสดงในแชท
        with st.chat_message("assistant"):
            st.write(f"**[Model: {model_name}]**")
            st.write(reply)
        
        # บันทึกประวัติ
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # ไม่ต้อง st.rerun()
        
    except Exception as e:
        st.error(f"ผิดพลาด: {str(e)}")
