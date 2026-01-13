import streamlit as st
from openai import OpenAI
import os

# --- 1. SETTING UP THE ROBOT'S BRAIN ---
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("🌍 My Travel Agent")

# --- 2. SETTING UP THE ROBOT'S MEMORY ---
# This part makes sure the robot doesn't forget your name or where you want to go.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional Travel Agent. Your goal is to help the user plan a 3-day trip. Always ask about their budget and preferred weather first."}
    ]

# Display previous conversation on the screen
for message in st.session_state.messages:
    if message["role"] != "system": # We hide the 'secret instructions' from the screen
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 3. TALKING TO THE ROBOT ---
if prompt := st.chat_input("Where should we go?"):
    # Add what you said to the memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ask the brain (Gemini) for an answer
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    # Add the robot's answer to the memory too!
    st.session_state.messages.append({"role": "assistant", "content": answer})
