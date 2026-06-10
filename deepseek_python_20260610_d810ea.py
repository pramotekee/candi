import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="DeepSeek V4 Chat", page_icon="🤖")
st.title("🤖 DeepSeek V4 Chat Box")

# ตั้งค่า API Key จาก Secrets (อย่าใส่ hardcode!)
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

# เก็บประวัติแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงข้อความเก่า
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# รับข้อความใหม่
if prompt := st.chat_input("พิมพ์มาเลย ถามอะไรผมก็ได้"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="deepseek-v4-flash",  # เปลี่ยนเป็น V4 แล้ว!
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})