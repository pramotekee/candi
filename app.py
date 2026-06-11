import streamlit as st
import sqlite3
import pandas as pd
import calendar
from datetime import datetime, date
import hashlib

# ------------------------------
# ตั้งค่า page
# ------------------------------
st.set_page_config(page_title="POPZILAR DAIRY", layout="wide")

# ------------------------------
# ฐานข้อมูล
# ------------------------------
conn = sqlite3.connect('diary.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT,
        name TEXT,
        title TEXT,
        story TEXT,
        country TEXT,
        province TEXT,
        image_path TEXT,
        created_at TEXT
    )
''')
conn.commit()

# ------------------------------
# helper
# ------------------------------
def get_today_str():
    return date.today().isoformat()

def get_fyi():
    # ตัวอย่าง FYI
    fyi_list = {
        "2026-06-11": "🌍 World Population Day: ตระหนักถึงปัญหาประชากรโลก",
        "2026-06-12": "🎨 International Yarn Bombing Day: ศิลปะถักไหมพรมบนพื้นที่สาธารณะ"
    }
    today = get_today_str()
    return fyi_list.get(today, "✨ ทุกวันคือวันพิเศษของใครสักคน ลองบันทึกเรื่องราวดีๆ ดู")

def get_country_province_list():
    # ตัวอย่างข้อมูล location 2 ชั้น (เอาจริงต้องขยายเยอะ)
    return {
        "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen"],
        "Japan": ["Tokyo", "Osaka", "Kyoto"],
        "USA": ["New York", "LA", "Chicago"],
        "UK": ["London", "Manchester", "Liverpool"],
        "France": ["Paris", "Lyon", "Marseille"],
        "Germany": ["Berlin", "Munich", "Hamburg"]
    }

# ------------------------------
# sidebar dashboard
# ------------------------------
st.sidebar.title("📊 Mini Dashboard")
df_all = pd.read_sql("SELECT country, province FROM entries", conn)
if not df_all.empty:
    country_stats = df_all['country'].value_counts()
    province_stats = df_all['province'].value_counts()
    st.sidebar.markdown("### 🌍 ประเทศ")
    for ctry, cnt in country_stats.items():
        percent = (cnt / len(df_all)) * 100
        st.sidebar.markdown(f"{ctry} : {cnt} เรื่อง ({percent:.1f}%)")
    st.sidebar.markdown("### 📍 จังหวัด")
    for prov, cnt in province_stats.items():
        st.sidebar.markdown(f"{prov} : {cnt} เรื่อง")
else:
    st.sidebar.info("ยังไม่มีข้อมูล location")

# ------------------------------
# ค้นหา
# ------------------------------
st.sidebar.markdown("## 🔍 ค้นหา")
search_term = st.sidebar.text_input("ชื่อ / title / story")

# ------------------------------
# หัวข้อหลัก + FYI
# ------------------------------
st.title("📔 POPZILAR DAIRY")
st.caption(f"🧠 FYI : {get_fyi()}")

# ------------------------------
# ปฏิทิน
# ------------------------------
now = datetime.now()
year, month = now.year, now.month
cal = calendar.monthcalendar(year, month)

days_in_month = calendar.monthrange(year, month)[1]
today_date = date.today()

# แสดงปฏิทิน grid
cols_header = st.columns(7)
for i, day_name in enumerate(["จ", "อ", "พ", "พฤ", "ศ", "ส", "อา"]):
    cols_header[i].markdown(f"**{day_name}**")

# เก็บวันที่ active สำหรับเลือก
selected_date = None
week_rows = []
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            current_date = date(year, month, day)
            is_future = current_date > today_date
            is_past = current_date < today_date
            is_active = current_date == today_date

            if is_future:
                cols[i].button(f"{day}", key=f"future_{day}", disabled=True, use_container_width=True)
            elif is_past:
                if cols[i].button(f"📅 {day}", key=f"past_{day}"):
                    selected_date = current_date
            else:
                if cols[i].button(f"✨ {day}", key=f"active_{day}", type="primary", use_container_width=True):
                    selected_date = current_date

# ------------------------------
# ส่วนบันทึก / แก้ไข
# ------------------------------
if selected_date:
    st.divider()
    st.subheader(f"📝 วันที่ {selected_date.isoformat()}")

    # ดึงข้อมูลเก่า (ถ้ามี)
    c.execute("SELECT * FROM entries WHERE entry_date=?", (selected_date.isoformat(),))
    old = c.fetchone()

    if selected_date < today_date and old:
        st.info("🔒 วันที่ผ่านไปแล้ว: แสดงมุมมองอ่านอย่างเดียว (ไว้ทำ PRO)")
        with st.expander("📄 ดูเนื้อหาเก่า"):
            st.write(f"**ชื่อ :** {old[2]}")
            st.write(f"**หัวข้อ :** {old[3]}")
            st.write(f"**เรื่อง :** {old[4]}")
            st.write(f"**ประเทศ :** {old[5]}")
            st.write(f"**จังหวัด :** {old[6]}")
    else:
        with st.form("entry_form"):
            name = st.text_input("1️⃣ Name")
            title = st.text_input("2️⃣ Title")
            story = st.text_area("3️⃣ Story", height=150)
            story_len = len(story)
            st.caption(f"ตัวอักษร {story_len}/500")
            if story_len > 500:
                st.warning("Story เกิน 500 (demo ปิด) เดี๋ยวทำ pro จำกัด")

            # location 2 ชั้น
            country_list = list(get_country_province_list().keys())
            selected_country = st.selectbox("4️⃣ ประเทศ", ["เลือก"] + country_list)
            provinces = get_country_province_list().get(selected_country, [])
            selected_province = st.selectbox("จังหวัด", ["เลือก"] + provinces)

            uploaded_img = st.file_uploader("🖼️ เพิ่มไฟล์ (ภาพ)", type=["png", "jpg", "jpeg"])
            saved = st.form_submit_button("💾 SAVE")

            if saved:
                if not name or not title or not story:
                    st.error("กรุณากรอก name, title, story")
                elif selected_country == "เลือก" or selected_province == "เลือก":
                    st.error("กรุณาเลือกประเทศและจังหวัด")
                else:
                    img_path = ""
                    if uploaded_img:
                        import hashlib, os
                        os.makedirs("uploads", exist_ok=True)
                        ext = uploaded_img.name.split('.')[-1]
                        fname = hashlib.md5(f"{selected_date}{name}".encode()).hexdigest() + f".{ext}"
                        img_path = os.path.join("uploads", fname)
                        with open(img_path, "wb") as f:
                            f.write(uploaded_img.getbuffer())

                    c.execute('''
                        INSERT OR REPLACE INTO entries 
                        (entry_date, name, title, story, country, province, image_path, created_at)
                        VALUES (?,?,?,?,?,?,?,?)
                    ''', (selected_date.isoformat(), name, title, story, selected_country, selected_province, img_path, datetime.now().isoformat()))
                    conn.commit()
                    st.success("✅ บันทึกสำเร็จ")
                    st.rerun()

# ------------------------------
# แสดง content card
# ------------------------------
st.divider()
st.subheader("📌 เรื่องราวล่าสุด")

query = "SELECT * FROM entries ORDER BY created_at DESC"
if search_term:
    query = f'''SELECT * FROM entries 
                WHERE name LIKE '%{search_term}%' 
                OR title LIKE '%{search_term}%' 
                OR story LIKE '%{search_term}%' 
                ORDER BY created_at DESC'''
df = pd.read_sql(query, conn)

if df.empty:
    st.info("ยังไม่มีเรื่องราว เริ่มเขียนในปฏิทินเลย ✨")
else:
    for _, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**👤 {row['name']}**  •  📍 {row['country']} / {row['province']}")
                st.markdown(f"### {row['title']}")
                st.markdown(f"{row['story'][:200]}...")
            with col2:
                share_url = f"?id={row['id']}"
                if st.button(f"🔗 Share", key=f"share_{row['id']}"):
                    st.code(f"http://localhost:8501{share_url}", language="text")
            st.divider()
