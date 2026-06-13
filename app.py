import streamlit as st

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CANDI | Find Talent</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=SF+Pro+Display:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #F5F5F7;
    --surface: #FFFFFF;
    --accent: #1D1D6E;
    --accent-mid: #3A3A8C;
    --text-primary: #1D1D1F;
    --text-secondary: #6E6E73;
    --tag-bg: #E8E8ED;
    --tag-text: #3A3A3C;
    --border: #D2D2D7;
    --card-shadow: 0 2px 12px rgba(0,0,0,0.07);
    --card-shadow-hover: 0 8px 28px rgba(0,0,0,0.12);
    --cat-system: #4A6FA5;
    --cat-conversation: #3A9E8F;
    --cat-revenue: #2E8B57;
    --cat-people: #E8734A;
    --cat-money: #B8860B;
    --cat-beauty: #C4637A;
    --cat-flow: #7B5EA7;
    --cat-trust: #4A90C4;
    --cat-pattern: #D4832A;
    --cat-maker: #8B5A2B;
    --cat-default: #8E8E93;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
  }
  .app { max-width: 1400px; margin: 0 auto; min-height: 100vh; position: relative; }
  #page-list { padding-bottom: 60px; }
  .header {
    text-align: center;
    padding: 24px 20px 32px;
    background: #1538C0;
    border-radius: 0 0 32px 32px;
    margin-bottom: 20px;
  }
  @media (max-width: 768px) {
    .header { padding: 32px 20px 40px; }
    .header .slogan { font-size: 16px; letter-spacing: 1px; }
    .header .caption { font-size: 13px; padding: 0 20px; }
  }
  .header h1 {
    font-family: 'Inter', sans-serif;
    font-size: 72px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 14px;
    line-height: 1;
    text-transform: uppercase;
  }
  .header .slogan {
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 2px;
    margin-top: 24px;
    margin-bottom: 12px;
    font-family: 'Inter', sans-serif;
  }
  .header .caption {
    font-size: 15px;
    font-weight: 400;
    color: #F9BF16;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
    font-family: 'Inter', sans-serif;
  }
  .search-container {
    display: flex;
    gap: 10px;
    padding: 0 20px 14px;
    max-width: 100%;
    margin: 0;
  }
  .search-box { flex: 1; position: relative; }
  .search-box input {
    width: 100%;
    padding: 11px 18px 11px 40px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    outline: none;
  }
  .search-box input:focus { border-color: var(--accent-mid); box-shadow: 0 0 0 3px rgba(58,58,140,0.08); }
  .search-box::before {
    content: "🔍";
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 13px;
    opacity: 0.4;
  }
  .sort-select {
    padding: 0 16px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    outline: none;
    cursor: pointer;
    min-width: 72px;
  }
  .create-btn {
    background: #F5C518;
    color: #1D1D1F;
    border: none;
    border-radius: 12px;
    padding: 0 20px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .create-btn:hover { background: #E0B010; transform: translateY(-1px); }
  .tabs-wrapper {
    padding: 0 20px 20px;
    overflow-x: auto;
    display: flex;
    gap: 8px;
    max-width: 1400px;
    margin: 0 auto;
  }
  .tabs-wrapper::-webkit-scrollbar { display: none; }
  .tab-btn {
    white-space: nowrap;
    padding: 7px 16px;
    border-radius: 20px;
    border: 2px solid transparent;
    background: var(--surface);
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .tab-btn:hover { color: var(--text-primary); }
  .tab-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .tab-btn.active[data-cat="System Architect"] { background: var(--cat-system); border-color: var(--cat-system); }
  .tab-btn.active[data-cat="Conversation Builder"] { background: var(--cat-conversation); border-color: var(--cat-conversation); }
  .tab-btn.active[data-cat="Revenue Generator"] { background: var(--cat-revenue); border-color: var(--cat-revenue); }
  .tab-btn.active[data-cat="People Connector"] { background: var(--cat-people); border-color: var(--cat-people); }
  .tab-btn.active[data-cat="Money Guardian"] { background: var(--cat-money); border-color: var(--cat-money); }
  .tab-btn.active[data-cat="Make Things Beauty"] { background: var(--cat-beauty); border-color: var(--cat-beauty); }
  .tab-btn.active[data-cat="Flow Planner"] { background: var(--cat-flow); border-color: var(--cat-flow); }
  .tab-btn.active[data-cat="Trust Keeper"] { background: var(--cat-trust); border-color: var(--cat-trust); }
  .tab-btn.active[data-cat="Pattern Hunter"] { background: var(--cat-pattern); border-color: var(--cat-pattern); }
  .tab-btn.active[data-cat="Hands-on Maker"] { background: var(--cat-maker); border-color: var(--cat-maker); }
  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    padding: 0 16px 40px;
  }
  @media (min-width: 600px) { .grid { grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 0 20px 40px; } }
  @media (min-width: 900px) { .grid { grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 0 24px 40px; } }
  @media (min-width: 1200px) { .grid { grid-template-columns: repeat(5, 1fr); gap: 22px; } }
  @media (min-width: 1400px) { .grid { grid-template-columns: repeat(6, 1fr); } }
  .thumb-card {
    cursor: pointer;
    background: var(--surface);
    border-radius: 16px;
    overflow: hidden;
    border: 2.5px solid transparent;
    box-shadow: var(--card-shadow);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }
  .thumb-card:hover { transform: translateY(-3px); box-shadow: var(--card-shadow-hover); }
  .thumb-card[data-cat="System Architect"] { border-color: var(--cat-system); }
  .thumb-card[data-cat="Conversation Builder"] { border-color: var(--cat-conversation); }
  .thumb-card[data-cat="Revenue Generator"] { border-color: var(--cat-revenue); }
  .thumb-card[data-cat="People Connector"] { border-color: var(--cat-people); }
  .thumb-card[data-cat="Money Guardian"] { border-color: var(--cat-money); }
  .thumb-card[data-cat="Make Things Beauty"] { border-color: var(--cat-beauty); }
  .thumb-card[data-cat="Flow Planner"] { border-color: var(--cat-flow); }
  .thumb-card[data-cat="Trust Keeper"] { border-color: var(--cat-trust); }
  .thumb-card[data-cat="Pattern Hunter"] { border-color: var(--cat-pattern); }
  .thumb-card[data-cat="Hands-on Maker"] { border-color: var(--cat-maker); }
  .thumb-img {
    width: 100%;
    aspect-ratio: 1;
    overflow: hidden;
    background: #E8E8ED;
    position: relative;
  }
  .thumb-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .thumb-info { padding: 12px 12px 14px; }
  .thumb-name {
    font-size: 12px;
    color: var(--text-primary);
    font-weight: 600;
    letter-spacing: 0.5px;
    line-height: 1.4;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .thumb-purpose {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 6px;
    line-height: 1.4;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
  }
  .thumb-meta { display: flex; flex-direction: column; gap: 2px; }
  .thumb-meta-row { font-size: 10.5px; color: var(--text-secondary); display: flex; align-items: center; gap: 4px; }
  .thumb-badge {
    display: inline-block;
    background: var(--tag-bg);
    color: var(--tag-text);
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 500;
    white-space: nowrap;
  }
  .thumb-badge.available { background: #E3F5EC; color: #1A7A3C; }
  .view-toggle-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
  }
  .view-toggle-btn.active { background: var(--accent); color: white; border-color: var(--accent); }
  .grid.line-view { display: block; }
  .grid.line-view .thumb-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    padding: 12px 16px;
    border-radius: 14px;
    border: 1px solid var(--border);
  }
  .grid.line-view .thumb-img { width: 52px; height: 52px; border-radius: 12px; flex-shrink: 0; }
  .grid.line-view .thumb-info { flex: 1; display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px 12px; padding: 0; }
  .grid.line-view .thumb-name { min-width: 130px; font-size: 13px; margin-bottom: 0; }
  .grid.line-view .thumb-purpose { min-width: 140px; font-size: 12px; margin-bottom: 0; }
  .line-sentence { display: none; }
  .grid.line-view .line-sentence {
    display: block;
    min-width: 200px;
    max-width: 280px;
    font-size: 11.5px;
    color: var(--text-secondary);
    line-height: 1.45;
    font-style: italic;
    padding-left: 8px;
    border-left: 2px solid var(--border);
  }
  .grid.line-view .line-workzone {
    min-width: 140px;
    font-size: 11.5px;
    color: var(--text-secondary);
    padding-left: 8px;
    border-left: 1px solid var(--border);
  }
  @media (max-width: 768px) {
    .grid.line-view .thumb-card { flex-direction: column; align-items: flex-start; }
    .grid.line-view .thumb-info { flex-direction: column; width: 100%; }
    .grid.line-view .line-workzone, .grid.line-view .line-sentence { border-left: none; padding-left: 0; margin-top: 4px; }
  }
  .modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10,10,30,0.5);
    z-index: 300;
    align-items: center;
    justify-content: center;
  }
  .modal-overlay.open { display: flex; }
  .modal {
    background: var(--surface);
    border-radius: 28px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
  }
  .modal-top {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    border-bottom: 1px solid var(--border);
  }
  .close-btn {
    width: 36px; height: 36px;
    border-radius: 50%;
    border: 1px solid var(--border);
    background: none;
    cursor: pointer;
  }
  .modal-body { padding: 20px; }
  .profile-top { display: flex; gap: 16px; margin-bottom: 18px; }
  .profile-img { width: 100px; height: 100px; border-radius: 14px; overflow: hidden; flex-shrink: 0; }
  .profile-img img { width: 100%; height: 100%; object-fit: cover; }
  .fname { font-size: 28px; font-weight: 700; text-transform: uppercase; }
  .lname { font-size: 18px; color: var(--text-secondary); text-transform: uppercase; }
  .info-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 8px;
    margin: 20px 0;
  }
  .info-label { font-weight: 600; padding-right: 20px; }
  .contact-section { border-top: 1px solid var(--border); padding-top: 16px; }
  .contact-links { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .contact-btn {
    background: var(--tag-bg);
    border: none;
    padding: 8px 16px;
    border-radius: 30px;
    cursor: pointer;
  }
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #1D1D1F;
    color: white;
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 13px;
    opacity: 0;
    transition: opacity 0.2s;
    pointer-events: none;
  }
  .toast.show { opacity: 1; }
</style>
</head>
<body>
<div class="app">
  <div id="page-list">
    <div class="header">
      <h1>CANDI</h1>
      <p class="slogan">Job titles fade. Human capabilities grow.</p>
      <p class="caption">The future of work isn't about titles. It's about what people can do.</p>
    </div>
    <div class="search-container">
      <div class="search-box"><input type="text" id="search-input" placeholder="Search talent..." oninput="handleFilterChange()"></div>
      <select id="sort-select" class="sort-select" onchange="handleFilterChange()">
        <option value="">A-Z</option>
        <option value="A">A</option><option value="B">B</option><option value="C">C</option>
        <option value="D">D</option><option value="E">E</option><option value="F">F</option>
        <option value="G">G</option><option value="H">H</option><option value="I">I</option>
        <option value="J">J</option><option value="K">K</option><option value="L">L</option>
        <option value="M">M</option><option value="N">N</option><option value="O">O</option>
        <option value="P">P</option><option value="Q">Q</option><option value="R">R</option>
        <option value="S">S</option><option value="T">T</option><option value="U">U</option>
        <option value="V">V</option><option value="W">W</option><option value="X">X</option>
        <option value="Y">Y</option><option value="Z">Z</option>
      </select>
      <button id="createEditBtn" class="create-btn">➕ Create / Edit</button>
    </div>
    <div class="tabs-wrapper" id="tabs-wrapper"></div>
    <div class="view-toggle" style="display: flex; gap: 8px; padding: 0 20px 14px; justify-content: flex-start;">
      <button id="view-card" class="view-toggle-btn active">▦ Card</button>
      <button id="view-line" class="view-toggle-btn">≡ Line</button>
    </div>
    <div id="cat-desc-bar" style="display:none;margin:0 16px 16px;padding:14px 16px;background:#fff;border-radius:12px;border-left:4px solid #000;font-size:13.5px;"></div>
    <div class="grid card-view" id="grid"></div>
  </div>
</div>
<div class="modal-overlay" id="modal-overlay" onclick="closeModalOnOverlay(event)">
  <div class="modal">
    <div class="modal-top"><span class="modal-top-label">CANDI</span><button class="close-btn" onclick="closeModal()">✕</button></div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
const SHEET_ID = '1grSMSRuWMvC5F5V82tMY0PJwV4WBHUn7OijZ6j3_Zxg';
const API_KEY = 'AIzaSyAIbTx6x5mDZC9_rgFcRpHeq4mx2tdNMII';
const RANGE_DOCS = 'Sheet1!A2:V10000';
const RANGE_CATS = 'Categories!A2:A100';
const USE_MOCK = false;
const CAT_DESC = {
  'System Architect': { sub: 'ถนัดเรื่องการทำงานของระบบ โครงสร้าง เครือข่ายการรับส่งข้อมูล', roles: 'Software Engineer, Tech Developer, IT Manager, System Admin, DevOps' },
  'Conversation Builder': { sub: 'ชอบสร้างการรับรู้ สร้างความสนใจ ทำให้ผู้คนคิด ตัดสินใจ และลงมือทำ', roles: 'Marketing, Copywriter, Content Creator, PR, Communications Manager' },
  'Revenue Generator': { sub: 'มองเห็นโอกาสในการสร้างยอดขาย รู้วิธีเปลี่ยนความต้องการให้เป็นรายได้', roles: 'Sales Manager, Business Development, Account Executive, Growth Manager' },
  'People Connector': { sub: 'เข้าใจความแตกต่างของผู้คน มองเห็นศักยภาพที่ซ่อนอยู่', roles: 'HR Manager, Recruiter, Talent Acquisition, People & Culture' },
  'Money Guardian': { sub: 'มองเห็นเรื่องราวที่ซ่อนอยู่หลังตัวเลข ตัดสินใจด้วยความรอบคอบ', roles: 'CFO, Finance Manager, Accountant, Financial Analyst' },
  'Make Things Beauty': { sub: 'เชื่อในพลังของภาพ สี รูปทรง ถ่ายทอดความรู้สึกได้ชัดเจน', roles: 'Graphic Designer, UI/UX Designer, Art Director, Brand Designer' },
  'Flow Planner': { sub: 'จัดระเบียบความซับซ้อน เชื่อมโยงทุกอย่างให้ดำเนินไปอย่างราบรื่น', roles: 'Project Manager, Operations Manager, COO, Logistics, Event Manager' },
  'Trust Keeper': { sub: 'ทำให้ลูกค้ารู้สึกว่าได้รับการดูแล รับฟังในสิ่งที่เขาไม่ได้พูด', roles: 'Customer Success, Account Manager, Client Service, CX Manager' },
  'Pattern Hunter': { sub: 'ค้นหารูปแบบ ความเชื่อมโยงและสัญญาณเล็กๆ ในข้อมูล', roles: 'Data Analyst, Business Intelligence, Market Research, Insights Manager' },
  'Hands-on Maker': { sub: 'ซ่อม สร้าง เสริม เติม แต่ง ปรับปรุง ให้สิ่งของกลับมาใช้งานได้', roles: 'ช่างซ่อม, Maintenance Engineer, Fabricator, Craftsman' }
};
const CAT_COLORS = {
  'System Architect': '#4A6FA5', 'Conversation Builder': '#3A9E8F', 'Revenue Generator': '#2E8B57',
  'People Connector': '#E8734A', 'Money Guardian': '#B8860B', 'Make Things Beauty': '#C4637A',
  'Flow Planner': '#7B5EA7', 'Trust Keeper': '#4A90C4', 'Pattern Hunter': '#D4832A', 'Hands-on Maker': '#8B5A2B'
};
function getCatColor(c) { if (!c) return '#8E8E93'; const k = Object.keys(CAT_COLORS).find(k => c.includes(k)); return k ? CAT_COLORS[k] : '#8E8E93'; }
let allTalent = [], activeCategories = ["All"];
function photoURL(id) { if (!id) return null; if (id.startsWith('http')) return id; return `https://drive.google.com/thumbnail?id=${id.trim()}&sz=w400`; }
function avatarSVG() { return `<div class="avatar-placeholder"><svg viewBox="0 0 64 64"><circle cx="32" cy="22" r="12" stroke="white" stroke-width="2"/><path d="M8 58c0-13.255 10.745-24 24-24s24 10.745 24 24" stroke="white" stroke-width="2"/></svg></div>`; }
function imgOrAvatar(id) { const url = photoURL(id); if (url) return `<img src="${url}" alt="photo" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">${avatarSVG()}`; return avatarSVG(); }
async function fetchFromSheet(range) { const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${range}?key=${API_KEY}`; const res = await fetch(url); const json = await res.json(); return json.values || []; }
async function initData() {
  if (USE_MOCK) { allTalent = []; buildTabs(["All"]); buildGrid([]); return; }
  try {
    const [docsRows, catsRows] = await Promise.all([fetchFromSheet(RANGE_DOCS), fetchFromSheet(RANGE_CATS)]);
    const rawDocs = docsRows.map(r => ({ id: r[0] || '', firstname: r[1] || '', lastname: r[2] || '', photo_id: r[3] || '', description: r[4] || '', i_do_good: r[5] || '', experience: r[6] || '', skill_tags: r[7] || '', language: r[8] || '', work_type: r[9] || '', expected_salary: r[10] || '', available_date: r[11] || '', contact_phone: r[12] || '', contact_line: r[13] || '', contact_email: r[14] || '', work_zone: r[15] || '', youtube: r[16] || '', instagram: r[17] || '', tiktok: r[18] || '', status: r[19] || 'FALSE', purpose_category: r[20] || '', resume: r[21] || '' }));
    allTalent = rawDocs.filter(c => c.status === 'TRUE');
    const categories = ["All", ...catsRows.map(row => row[0]).filter(c => c && c !== "All")];
    buildTabs(categories);
    buildGrid(allTalent);
    initViewToggle();
    initCreateButton();
  } catch(err) { document.getElementById('grid').innerHTML = '<p>Failed to load data.</p>'; }
}
function buildTabs(cats) { const w = document.getElementById('tabs-wrapper'); w.innerHTML = cats.map(c => `<button class="tab-btn ${c === 'All' ? 'active' : ''}" onclick="handleTabClick('${c}')">${c}</button>`).join(''); }
function handleTabClick(cat) { activeCategories = [cat]; document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active')); event.target.classList.add('active'); handleFilterChange(); }
function handleFilterChange() {
  const searchVal = document.getElementById('search-input').value.toLowerCase().trim();
  const alpha = document.getElementById('sort-select').value;
  const filtered = allTalent.filter(c => {
    const name = `${c.firstname} ${c.lastname}`.toLowerCase();
    const matchSearch = name.includes(searchVal) || (c.i_do_good || '').toLowerCase().includes(searchVal) || (c.description || '').toLowerCase().includes(searchVal) || (c.purpose_category || '').toLowerCase().includes(searchVal) || (c.skill_tags || '').toLowerCase().includes(searchVal) || (c.experience || '').toLowerCase().includes(searchVal) || (c.language || '').toLowerCase().includes(searchVal) || (c.work_type || '').toLowerCase().includes(searchVal) || (c.work_zone || '').toLowerCase().includes(searchVal) || (c.available_date || '').toLowerCase().includes(searchVal);
    const matchAlpha = !alpha || c.firstname.toUpperCase().startsWith(alpha);
    let matchCat = activeCategories.includes("All");
    if (!matchCat) { const cats = c.purpose_category.split(',').map(s => s.trim()); matchCat = activeCategories.some(cat => cats.includes(cat)); }
    return matchSearch && matchAlpha && matchCat;
  });
  buildGrid(filtered);
}
function buildGrid(talent) {
  const activeCat = activeCategories.length === 1 && activeCategories[0] !== 'All' ? activeCategories[0] : null;
  const descBar = document.getElementById('cat-desc-bar');
  if (descBar && activeCat && CAT_DESC[activeCat]) { const d = CAT_DESC[activeCat]; descBar.style.display = 'block'; descBar.innerHTML = `<strong>${activeCat}</strong> — ${d.sub}<br><span style="font-size:12px;">เทียบได้กับ: ${d.roles}</span>`; }
  else if (descBar) descBar.style.display = 'none';
  const grid = document.getElementById('grid');
  if (!talent.length) { grid.innerHTML = '<p style="text-align:center;padding:60px;">No talent found.</p>'; return; }
  grid.innerHTML = talent.map(c => { const cat = c.purpose_category ? c.purpose_category.split(',')[0].trim() : ''; const avail = (c.available_date || '').includes('ทันที'); const iDo = c.i_do_good || ''; return `<div class="thumb-card" data-cat="${cat}" onclick="openModal('${c.id}')"><div class="thumb-img">${imgOrAvatar(c.photo_id)}</div><div class="thumb-info"><div class="thumb-name">${c.firstname}<br>${c.lastname}</div><div class="thumb-purpose">${iDo}</div><div class="thumb-meta">${c.expected_salary ? `<div class="thumb-meta-row">💰 ${c.expected_salary}</div>` : ''}<div class="thumb-meta-row" style="gap:6px;flex-wrap:wrap;">${c.purpose_category ? `<span class="thumb-badge" style="background:${getCatColor(c.purpose_category)}20;color:${getCatColor(c.purpose_category)};">${c.purpose_category.split(',')[0]}</span>` : ''}${c.work_type ? `<span class="thumb-badge">${c.work_type}</span>` : ''}${avail ? `<span class="thumb-badge available">พร้อมทันที</span>` : ''}</div></div></div>${c.work_zone ? `<div class="line-workzone">📍 ${c.work_zone}</div>` : ''}<div class="line-sentence">💬 ${iDo}</div></div>`; }).join('');
}
function openModal(id) { const c = allTalent.find(x => x.id === id); if (!c) return; const info = [['Capability', c.purpose_category], ['What I Do Best', c.i_do_good], ['Experience', c.experience], ['Language', c.language], ['Work Type', c.work_type], ['Work zone', c.work_zone], ['Expected', c.expected_salary], ['Available', c.available_date]].filter(([,v]) => v).map(([l,v]) => `<div class="info-label">${l}</div><div class="info-value">${v}</div>`).join(''); const contacts = []; if (c.contact_line) contacts.push(`<button class="contact-btn" onclick="openLink('https://line.me/ti/p/${c.contact_line}')">LINE</button>`); if (c.contact_phone) contacts.push(`<button class="contact-btn" onclick="openLink('tel:${c.contact_phone}')">Call</button>`); if (c.resume) contacts.push(`<button class="contact-btn" onclick="openLink('${c.resume}')">Resume</button>`); document.getElementById('modal-body').innerHTML = `<div class="profile-top"><div class="profile-img" onclick="openLightbox('${c.photo_id}')">${imgOrAvatar(c.photo_id)}</div><div><div class="fname">${c.firstname}</div><div class="lname">${c.lastname}</div></div></div><div class="info-grid">${info}</div><div class="contact-section"><div class="contact-title">Contact</div><div class="contact-links">${contacts.join('')}</div></div>`; document.getElementById('modal-overlay').classList.add('open'); }
function closeModal() { document.getElementById('modal-overlay').classList.remove('open'); }
function closeModalOnOverlay(e) { if (e.target === document.getElementById('modal-overlay')) closeModal(); }
function openLightbox(id) { const url = photoURL(id); if (url) window.open(url, '_blank'); }
function openLink(url) { window.open(url, '_blank'); }
function initViewToggle() { const cardBtn = document.getElementById('view-card'), lineBtn = document.getElementById('view-line'), grid = document.getElementById('grid'); if (!cardBtn || !lineBtn) return; function setView(v) { if (v === 'line') { grid.classList.remove('card-view'); grid.classList.add('line-view'); cardBtn.classList.remove('active'); lineBtn.classList.add('active'); } else { grid.classList.remove('line-view'); grid.classList.add('card-view'); lineBtn.classList.remove('active'); cardBtn.classList.add('active'); } } cardBtn.onclick = () => setView('card'); lineBtn.onclick = () => setView('line'); setView('card'); }
function initCreateButton() { const btn = document.getElementById('createEditBtn'); if (btn) btn.onclick = () => { const action = confirm('คุณต้องการทำอะไร?\n• OK = สร้างโปรไฟล์ใหม่\n• Cancel = แก้ไข/ลบ'); if (action) window.open('create.html', '_blank'); else window.open('edit.html', '_blank'); }; }
(() => { initData(); })();
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=1000, scrolling=True)
