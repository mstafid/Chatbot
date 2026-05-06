import streamlit as st
import requests
import time

# ===== CONFIG =====
st.set_page_config(
    page_title="Chatbot Statistika",
    page_icon="🤖",
    layout="centered"
)

# ===== BACKGROUND + STYLE =====
st.markdown("""
<style>

/* Background gradient + pattern */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* overlay pattern statistik */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    z-index: 0;
}

/* chat container */
.block-container {
    position: relative;
    z-index: 1;
}

/* bubble styling */
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

/* input box */
.stChatInput textarea {
    background-color: #1f2a38 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.title("🤖 Chatbot Statistika UII")
st.caption("AI Assistant • n8n • RAG System")

# ===== SESSION =====
if "chatInputs" not in st.session_state:
    st.session_state.chatInputs = []

# ===== INITIAL MESSAGE (NEW) =====
if len(st.session_state.chatInputs) == 0:
    with st.spinner("🤖 Memulai chatbot..."):
        time.sleep(1)
    st.session_state.chatInputs.append({
        "role": "assistant",
        "content": "👋 Assalamualaikum brosis statistician!\n\naku adalah AI Assistant Statistika UII yang akan menjawab kamu seputar Statistika UII.\n\nAda yang mau ditanyain? 😊"
    })

# ===== DISPLAY CHAT =====
for msg in st.session_state.chatInputs:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ===== INPUT =====
prompt = st.chat_input("Tanya tentang statistika UII...")

if prompt:
    st.session_state.chatInputs.append({"role": "user", "content": prompt})

    with st.spinner("📊 Bot sedang menganalisis data..."):
        time.sleep(1)

        try:
            response = requests.post(
                "https://yape.app.n8n.cloud/webhook/2eae7dfc-cc03-4d86-a3ac-a514950ed67c/chat",
                json={"chatInput": prompt}
            )

            data = response.json()

            # fleksibel
            reply = data.get("output") or data.get("reply") or "Tidak ada respon dari server"

        except Exception as e:
            reply = f"⚠️ Error: {e}"

    st.session_state.chatInputs.append({"role": "assistant", "content": reply})

    st.rerun()
