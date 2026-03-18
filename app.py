import streamlit as st
from groq import Groq

# --- 1. SET THE STAGE ---
st.set_page_config(page_title="NEXUS AI", page_icon="⭐")
st.title("🤖 Nexus AI")
st.write("Welcome! This is a simple AI assistant built with Python.")

# --- 2. GET THE BRAIN (The API Key) ---
# We use st.secrets so your private key stays hidden from the public
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Error: Please add your Groq API Key to the settings!")
    st.stop()

# --- 3. CREATE MEMORY ---
# This keeps track of what you and the AI have said so far
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SHOW THE CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 5. CHAT WITH THE AI ---
if prompt := st.chat_input("Write a message..."):
    # Remember what the user just typed
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Ask the AI for an answer
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        # Show the AI's response as it "thinks"
        response = st.write_stream(chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content)
    
    # Save the AI's answer to memory
    st.session_state.messages.append({"role": "assistant", "content": response})