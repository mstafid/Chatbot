import streamlit as st
import requests
import time
import markdown

def render_md(text):
    return markdown.markdown(text)

# ===== CONFIG =====
st.set_page_config(
    page_title="Chatbot Statistika",
    page_icon="🤖",
    layout="centered"
)

# ===== BACKGROUND + STYLE =====
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* pattern */
.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    z-index: 0;
}

/* container */
.block-container {
    position: relative;
    z-index: 1;
}

/* input */
.stChatInput textarea {
    background-color: #1f2a38 !important;
    color: white !important;
}

/* USER bubble kanan */
.user-bubble {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
    display: inline-block;
    float: right;
    clear: both;
    margin: 5px 0;
}

/* BOT bubble kiri */
.bot-bubble {
    background-color: #1f2a38;
    padding: 10px 15px;
    border-radius: 15px;
    display: inline-block;
    float: left;
    clear: both;
    margin: 5px 0;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.title("🤖 Chatbot Statistika UII")
st.caption("AI Assistant • n8n • RAG System")

# ===== SESSION =====
if "chatInputs" not in st.session_state:
    st.session_state.chatInputs = []

if "waiting_response" not in st.session_state:   # ✅ FIX WAJIB
    st.session_state.waiting_response = False

# ===== INITIAL MESSAGE =====
if len(st.session_state.chatInputs) == 0:
    with st.spinner("🤖 Memulai chatbot..."):
        time.sleep(1)
    st.session_state.chatInputs.append({
        "role": "assistant",
        "content": "👋 Assalamualaikum brosis statistician!\n\nAku adalah AI Assistant Statistika UII yang akan membantu kamu.\n\nAda yang mau ditanyain? 😊"
    })

# ===== DISPLAY CHAT =====
for msg in st.session_state.chatInputs:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-bubble">🧑 {render_md(msg["content"])}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-bubble">🤖 {render_md(msg["content"])}</div>',
            unsafe_allow_html=True
        )

# ===== INPUT =====
prompt = st.chat_input("Tanya tentang statistika UII...")

if prompt:
    st.session_state.chatInputs.append({
        "role": "user",
        "content": prompt
    })

    st.session_state.waiting_response = True
    st.rerun()

# ===== HANDLE RESPONSE =====
if st.session_state.waiting_response:

    prompt = st.session_state.chatInputs[-1]["content"]

    with st.spinner("📊 Bot sedang mencari informasi..."):
        time.sleep(1)

        try:
            response = requests.post(
                "https://kaletooo.app.n8n.cloud/webhook/2eae7dfc-cc03-4d86-a3ac-a514950ed67c/chat",
                json={"chatInput": prompt}
            )

            data = response.json()
            reply = data.get("output") or data.get("reply") or "Tidak ada respon dari server"

        except Exception as e:
            reply = f"⚠️ Error: {e}"

    st.session_state.chatInputs.append({
        "role": "assistant",
        "content": reply
    })

    st.session_state.waiting_response = False
    st.rerun()
