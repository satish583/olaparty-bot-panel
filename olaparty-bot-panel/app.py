import streamlit as st
import requests
import re
import urllib3
from urllib.parse import quote                                          

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Apne deployed Bot Server ki URL yahan daalein (jaise Render URL)
BOT_SERVER_URL = "https://tumhara-bot-server.onrender.com" 
TOTAL_BOTS = 8

def extract_cid_from_link(text):
    match = re.search(r'(https?://api\.olaparty\.com/d/[\w-]+)', text)
    if match: return match.group(1)
    match = re.search(r'(https?://[\w\.]+/d/[\w-]+)', text)
    if match: return match.group(1)
    match = re.search(r'(https?://[^\s]+)', text)
    if match: return match.group(1)
    return None

def smart_resolve_input(input_str):
    cid_match = re.search(r'(C_\d+_V[12]_[A-Za-z0-9_]+)', input_str, re.IGNORECASE)
    if cid_match:
        return cid_match.group(1).upper()
    if "http" in input_str:
        link = extract_cid_from_link(input_str)
        if link: return link
    clean_str = input_str.strip()
    if clean_str.isdigit(): return clean_str
    return None

st.set_page_config(page_title="LUCKY GODFATHER | FLEET COMMAND", page_icon="🎮", layout="wide")

st.markdown("<h1 style='text-align: center;'>☠️ <span style='color: #ff0040;'>𝐋𝐔𝐂𝐊𝐘</span> 🌎 <span style='color: #0088ff;'>𝙂𝙤𝙙fatheR</span> 🖥️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.5rem; font-weight: bold;'>FLEET CONTROL CENTER</p><hr style='border:1px solid #333;'>", unsafe_allow_html=True)

for i in range(1, TOTAL_BOTS + 1):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown(f"<h4>🤖 Bot {i}</h4>", unsafe_allow_html=True)
    with col2:
        target_input = st.text_input("Target", key=f"input_{i}", label_visibility="collapsed", placeholder=f"Room Link / ID for Bot {i}...")
    with col3:
        if st.button("🚀 CLICK", key=f"btn_{i}"):
            if not target_input:
                st.warning(f"⚠️ Bot {i} ke liye link daalo!")
            else:
                target_dest = smart_resolve_input(target_input)
                if target_dest:
                    try:
                        api_link = f"{BOT_SERVER_URL.strip('/')}/change_room?link={quote(target_dest)}&bot={i}"
                        res = requests.get(api_link, timeout=15, verify=False)
                        if res.status_code == 200:
                            st.success(f"✅ Bot {i} SUCCESS!")
                        else:
                            st.error(f"❌ ERROR {res.status_code}")
                    except:
                        st.error("❌ SERVER OFFLINE.")
                else:
                    st.error("❌ INVALID TARGET.")

st.markdown("<hr style='border:1px dashed #333;'>", unsafe_allow_html=True)

# ALL BOTS CONTROL
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.markdown("<h3>🚀 ALL BOTS</h3>", unsafe_allow_html=True)
with col2:
    all_target_input = st.text_input("Target", key="input_all", label_visibility="collapsed", placeholder="Sabhi bots ke liye Room Link / ID yaha daalein...")
with col3:
    if st.button("🔥 SEND ALL", key="btn_all"):
        if not all_target_input:
            st.warning("⚠️ Link ya ID daalo!")
        else:
            target_dest = smart_resolve_input(all_target_input)
            if target_dest:
                try:
                    api_link = f"{BOT_SERVER_URL.strip('/')}/change_room?link={quote(target_dest)}&bot=all"
                    res = requests.get(api_link, timeout=15, verify=False)
                    if res.status_code == 200:
                        st.success("✅ SUCCESS: Sabhi bots shift ho gaye!")
                        st.balloons()
                    else:
                        st.error("❌ ERROR")
                except:
                    st.error("❌ SERVER OFFLINE.")
            else:
                st.error("❌ INVALID TARGET.")