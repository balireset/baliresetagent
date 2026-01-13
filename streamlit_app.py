import streamlit as st
from openai import OpenAI
import os

# --- 1. SETUP ---
# This pulls your key from the Streamlit "Secrets" box
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("🤖 My Smart Agent")

# --- 2. THE MESSAGE CLEANER ---
if "messages" not in st.session_state:
    # We start with a "System" message to give the agent its personality
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI agent. Be concise and friendly."}
    ]

# --- 3. THE CHAT INTERFACE ---
for message in st.session_state.messages:
    if message["role"] != "system": # Hide the secret instructions from the screen
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    # Add User message to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # FIXED: We are now using the current 2026 model 'gemini-2.5-flash'
            response = client.chat.completions.create(
                model="gemini-2.5-flash", 
                messages=st.session_state.messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            
            # Add the response to memory
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Brain Error: {e}")
            st.info("Tip: If you see 'API key not valid', check your Streamlit Secrets again!")
