# app.py
import streamlit as st
import requests
import uuid

# --- Configuration ---
# BACKEND_URL = "http://localhost:3000/calculate"
BACKEND_URL = "https://multi-agent-price-calculator-backend.onrender.com"
# --- Page Setup ---
st.set_page_config(
    page_title="Multi-Agent Price Calculator",
    page_icon="🤖",
    layout="centered"
)

# --- Session State Initialization ---
# This helps us remember the conversation thread ID
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = f"st-thread-{uuid.uuid4()}"
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

# --- UI Components ---
st.title("🤖 Multi-Agent Price Calculator")
st.caption("Enter a query like: 'What is the price of a 150 EUR product in USD with a 25% tax?'")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Logic ---
prompt = st.chat_input("Enter your price calculation query...")

if prompt:
    # Add user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a spinner while the agent is working
    with st.spinner("The agents are collaborating..."):
        try:
            payload = {
                "userInput": prompt,
                "threadId": st.session_state.thread_id
            }
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            
            result = response.json().get("result", "Sorry, I received an empty response.")
            
            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result})
            with st.chat_message("assistant"):
                st.markdown(result)

        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred while contacting the backend: {e}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})