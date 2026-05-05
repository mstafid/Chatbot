import streamlit as st
import requests

st.title("Chatbot Skripsi")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Tanya sesuatu...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # contoh request ke n8n / API
    response = requests.post(
        "https://your-n8n-url/webhook/chat",
        json={"message": user_input}
    )

    bot_reply = response.json().get("reply", "Error")

    st.session_state.messages.append(("bot", bot_reply))

for role, msg in st.session_state.messages:
    st.write(f"**{role}**: {msg}")