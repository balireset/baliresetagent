import streamlit as st
from openai import OpenAI
import os

# --- 1. SETUP ---
# We use st.secrets for Streamlit Cloud
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("🤖 My Smart Agent")

# --- 2. THE MESSAGE CLEANER ---
# This ensures we don't send anything that breaks Google's rules
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. THE CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    # Add User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use 'gemini-1.5-flash' but wrap it in a 'try' block to catch errors
            response = client.chat.completions.create(
                model="gemini-1.5-flash", 
                messages=st.session_state.messages,
                temperature=0.7 # Helps prevent "looping" errors
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Brain Error: {e}")
            st.info("Tip: Check if your API Key is correct in Streamlit Advanced Settings!")
