
import streamlit as st

st.set_page_config(page_title="Message Translator", page_icon="💬")

st.title("💬 Message Translator")

# Choose language (we'll use this later)
language = st.selectbox(
    "Select language:",
    ["Spanish", "French", "Punjabi"]
)

st.subheader("Chat with Alex")
st.caption("Messaging prototype")

# Store messages so they don't disappear
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["sender"]):
        st.write(message["text"])

# Input box at the bottom
message = st.chat_input("Type your message here...")

# Add new messages to the conversation
if message:
    st.session_state.messages.append({
        "sender": "user",
        "text": message
    })

    st.rerun()
