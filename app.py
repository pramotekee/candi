import streamlit as st
import sqlite3
import pandas as pd
import calendar
from datetime import datetime, date
import hashlib
import os

st.set_page_config(page_title="PEOPLE DAIRY", layout="wide")

# DB Setup
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

# Helper
def get_today_str():
    return date.today().isoformat()

def get_fyi():
    fyi_list = {
        "2026-06-11": "🌍 World Population Day: Raise awareness about global population issues",
        "2026-06-12": "🎨 International Yarn Bombing Day: Yarn art in public spaces"
    }
    today = get_today_str()
    return fyi_list.get(today, "✨ Every day is special for someone. Start writing your story.")

def get_country_province_list():
    return {
        "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen"],
        "Japan": ["Tokyo", "Osaka", "Kyoto"],
        "USA": ["New York", "Los Angeles", "Chicago"],
        "UK": ["London", "Manchester", "Liverpool"],
        "France": ["Paris", "Lyon", "Marseille"],
        "Germany": ["Berlin", "Munich", "Hamburg"]
    }

day_colors = {
    0: "#FFD966",  # Mon
    1: "#FFB347",  # Tue
    2: "#F4A261",  # Wed
    3: "#E9C46A",  # Thu
    4: "#A7C7E7",  # Fri
    5: "#B5EAD7",  # Sat
    6: "#F7C6C6"   # Sun
}

# Initialize session state
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None

# Layout columns
left_col, right_col = st.columns([2, 1])

with left_col:
    st.title("📔 PEOPLE DAIRY")
    st.caption(f"🧠 FYI : {get_fyi()}")

    # Calendar
    now = datetime.now()
    year, month = now.year, now.month
    cal = calendar.monthcalendar(year, month)
    today_date = date.today()

    # Weekday headers
    headers = st.columns(7)
    for i, day_name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        headers[i].markdown(f"**{day_name}**")

    # Display calendar grid
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                current_date = date(year, month, day)
                is_future = current_date > today_date
                day_color = day_colors.get(i, "#CCCCCC")
                
                if is_future:
                    cols[i].markdown(
                        f"<div style='text-align: center; padding: 10px; background-color: #E0E0E0; border-radius: 50%; width: 50px; margin: auto; color: gray;'>{day}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    # ใช้ markdown แทน button
                    if cols[i].markdown(
                        f"<div style='text-align: center; padding: 10px; background-color: {day_color}; border-radius: 50%; width: 50px; margin: auto; cursor: pointer;'>{'✨ ' if current_date == today_date else ''}{day}</div>",
                        unsafe_allow_html=True
                    ):
                        # Streamlit markdown ไม่มี onclick แบบนี้ได้
                        pass
                    # ใช้ button จริงข้างล่างแทน
                    button_label = f"{day}"
                    if current_date == today_date:
                        button_label = f"✨ {day}"
                    if cols[i].button(button_label, key=f"day_{year}_{month}_{day}", use_container_width=True):
                        st.session_state.selected_date = current_date
                        st.rerun()

with right_col:
    st.subheader("📊 Mini Dashboard")
    df_all = pd.read_sql("SELECT country, province FROM entries", conn)
    if not df_all.empty:
        country_stats = df_all['country'].value_counts()
        province_stats = df_all['province'].value_counts()
        st.markdown("### 🌍 Countries")
        for ctry, cnt in country_stats.items():
            percent = (cnt / len(df_all)) * 100
            st.markdown(f"{ctry} : {cnt} stories ({percent:.1f}%)")
        st.markdown("### 📍 Provinces")
        for prov, cnt in province_stats.items():
            st.markdown(f"{prov} : {cnt} stories")
    else:
        st.info("No location data yet")

# Form Section
if st.session_state.selected_date:
    selected_date = st.session_state.selected_date
    with st.container():
        st.divider()
        st.subheader(f"📝 {selected_date.isoformat()}")
        c.execute("SELECT * FROM entries WHERE entry_date=?", (selected_date.isoformat(),))
        old = c.fetchone()
        if selected_date < today_date and old:
            st.info("🔒 Past date: View only mode (PRO feature coming)")
            with st.expander("📄 Read Story"):
                st.write(f"**Name :** {old[2]}")
                st.write(f"**Title :** {old[3]}")
                st.write(f"**Story :** {old[4]}")
                st.write(f"**Country :** {old[5]}")
                st.write(f"**Province :** {old[6]}")
        else:
            with st.form("entry_form"):
                name = st.text_input("1️⃣ Name")
                title = st.text_input("2️⃣ Title")
                story = st.text_area("3️⃣ Story", height=150)
                story_len = len(story)
                st.caption(f"Characters {story_len}/500")
                
                country_list = list(get_country_province_list().keys())
                selected_country = st.selectbox("4️⃣ Country", ["Select"] + country_list)
                provinces = get_country_province_list().get(selected_country, [])
                selected_province = st.selectbox("Province", ["Select"] + provinces)
                
                uploaded_img = st.file_uploader("🖼️ Add Image", type=["png", "jpg", "jpeg"])
                saved = st.form_submit_button("💾 SAVE")
                if saved:
                    if not name or not title or not story:
                        st.error("Please fill Name, Title, Story")
                    elif selected_country == "Select" or selected_province == "Select":
                        st.error("Please select Country and Province")
                    else:
                        img_path = ""
                        if uploaded_img:
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
                        st.success("✅ Saved successfully")
                        st.session_state.selected_date = None
                        st.rerun()

# Feed
st.divider()
st.subheader("📌 Latest Stories")
search_term = st.text_input("🔍 Search by Name, Title, or Story")
query = "SELECT * FROM entries ORDER BY created_at DESC"
if search_term:
    query = f'''SELECT * FROM entries 
                WHERE name LIKE '%{search_term}%' 
                OR title LIKE '%{search_term}%' 
                OR story LIKE '%{search_term}%' 
                ORDER BY created_at DESC'''
df = pd.read_sql(query, conn)

if df.empty:
    st.info("No stories yet. Start writing in the calendar ✨")
else:
    for _, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**👤 {row['name']}**  •  📍 {row['country']} / {row['province']}")
                st.markdown(f"### {row['title']}")
                st.markdown(f"{row['story'][:200]}...")
            with col2:
                if st.button(f"🔗 Share", key=f"share_{row['id']}"):
                    st.code(f"https://people-dairy.streamlit.app/?id={row['id']}", language="text")
            st.divider()
