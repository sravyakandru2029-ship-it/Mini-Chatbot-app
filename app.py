import streamlit as st
from openai import OpenAI

# ============================================
# Page configuration
st.set_page_config(
    page_title="Mini ChatGPT - Mistral",
    page_icon="🤖",
    layout="centered"
)

# =======================================
st.title("🤖 Mini ChatGPT (Mistral AI)")

# Your API Key
api_key = "LyixJ46VyOuuPdWkex2XfGwl5o5tloWp"

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

# Show previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:
    if not api_key:
        st.error("Please enter your API key")
        st.stop()
        
    # Initialize the client with correct variable name and base URL
    client = OpenAI(api_key=api_key, base_url="https://api.mistral.ai/v1")
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="mistral-small-latest", # Fixed typo here
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            
    # Save assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ========================================================================
# Sidebar (Added missing colons)
with st.sidebar:
    st.header("Options")
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        st.sidebar.success("Chat history cleared!")
        st.rerun()
        
    st.markdown("---")
    st.write("**Model:** mistral-small-latest")