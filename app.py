import streamlit as st
from groq import Groq

# 1. Initialize Groq Client using Streamlit Secrets
# This looks for the key in .streamlit/secrets.toml locally
# or in the "Secrets" settings on Streamlit Cloud
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("API Key not found! Please set GROQ_API_KEY in your secrets.toml or Streamlit settings.")
    st.stop()

st.set_page_config(page_title="Chatbot", page_icon="🚀")
st.title("🚀 Chatbot")
st.caption("Let's chat!!")

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle User Input
if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 5. Generate Response
    with st.chat_message("assistant"):
        try:
            # Using Llama 3.3 for high performance
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            
            reply = completion.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"Error: {e}")