
import streamlit as st

st.set_page_config(page_title="Message Translator", page_icon="💬")

st.title("💬 Message Translator")
st.subheader("Chat with Alex")
st.caption("Messaging prototype — messages are simulated")

# Predefined translations
translations = {
    "Spanish": {
        "hello": "Hola",
        "how are you?": "¿Cómo estás?",
        "thank you": "Gracias",
        "good morning": "Buenos días",
        "are you free tomorrow?": "¿Estás libre mañana?",
        "see you later": "Hasta luego",
        "i will see you next friday": "Nos vemos el próximo viernes",
        "eyesight": "Vista"
    },

    "French": {
        "hello": "Bonjour",
        "how are you?": "Comment ça va ?",
        "thank you": "Merci",
        "good morning": "Bonjour",
        "are you free tomorrow?": "Tu es libre demain ?",
        "see you later": "À plus tard",
        "i will see you next friday": "Je te verrai vendredi prochain",
        "eyesight": "Vue"
    },

    "Punjabi": {
        "hello": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
        "how are you?": "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?",
        "thank you": "ਧੰਨਵਾਦ",
        "good morning": "ਸ਼ੁਭ ਸਵੇਰ",
        "are you free tomorrow?": "ਕੀ ਤੁਸੀਂ ਕੱਲ੍ਹ ਖਾਲੀ ਹੋ?",
        "see you later": "ਫਿਰ ਮਿਲਾਂਗੇ",
        "i will see you next friday": "ਅਗਲੇ ਸ਼ੁੱਕਰਵਾਰ ਮਿਲਾਂਗੇ",
        "eyesight": "ਨਜ਼ਰ"
    }
}

# Store conversation and translation preview
if "messages" not in st.session_state:
    st.session_state.messages = []

if "preview" not in st.session_state:
    st.session_state.preview = None

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "edited_translation" not in st.session_state:
    st.session_state.edited_translation = ""


# Generate the translation preview
def preview_message():
    message = st.session_state.draft.strip()
    language = st.session_state.language

    # Standardise text to find predefined translations
    key = message.lower().rstrip(".!")

    translation = translations[language].get(key, "")

    st.session_state.preview = (message, language)
    st.session_state.edited_translation = translation


# Send the approved translation
def send_message():
    message = st.session_state.draft.strip()
    language = st.session_state.language

    # Only send if the preview matches the current draft
    if st.session_state.preview != (message, language):
        return

    translated = st.session_state.edited_translation.strip()

    if not translated:
        return

    st.session_state.messages.append({
        "original": message,
        "translated": translated,
        "language": language
    })

    # Clear the input after sending
    st.session_state.draft = ""
    st.session_state.preview = None
    st.session_state.edited_translation = ""


# Display conversation
st.write("### Conversation")

if not st.session_state.messages:
    st.info("No messages yet. Start a conversation below.")

for message in st.session_state.messages:
    with st.chat_message("user"):
        st.write(message["translated"])
        st.caption(
            f"Translated to {message['language']} | "
            f"Original: {message['original']}"
        )

st.divider()

# Message composer
st.write("### New message")

language = st.selectbox(
    "Translate into:",
    ["Spanish", "French", "Punjabi"],
    key="language"
)

st.text_area(
    "Type your message:",
    key="draft",
    height=100
)

# Preview translation before sending
st.button(
    "🌐 Preview translation",
    on_click=preview_message,
    disabled=not bool(st.session_state.draft.strip())
)

# Check whether the preview is still current
current_preview = (
    st.session_state.draft.strip(),
    st.session_state.language
)

if st.session_state.preview == current_preview:

    st.write(f"### {language} translation")

    st.text_area(
        "Edit translation before sending:",
        key="edited_translation",
        height=100
    )

    if not st.session_state.edited_translation.strip():
        st.warning(
            "No predefined translation found. "
            "Enter a translation manually to continue."
        )

    st.button(
        "📤 Send message",
        on_click=send_message,
        disabled=not bool(
            st.session_state.edited_translation.strip()
        )
    )

elif st.session_state.preview is not None:
    st.info(
        "Your message or language has changed. "
        "Preview the translation again before sending."
    )
