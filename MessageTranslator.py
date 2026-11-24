
import streamlit as st

st.set_page_config(
    page_title="Message Translator",
    page_icon="💬"
)

st.title("💬 Message Translator")
st.subheader("Chat with Alex")
st.caption("Messaging prototype — messages are simulated")


# -----------------------------------
# TRANSLATIONS
# -----------------------------------

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


# -----------------------------------
# SESSION STATE
# -----------------------------------

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store the current message
if "draft" not in st.session_state:
    st.session_state.draft = ""

# Store translation preview
if "preview" not in st.session_state:
    st.session_state.preview = None

# Store editable translation
if "edited_translation" not in st.session_state:
    st.session_state.edited_translation = ""


# -----------------------------------
# FUNCTIONS
# -----------------------------------

def preview_message():

    message = st.session_state.draft.strip()
    language = st.session_state.language

    if not message:
        return

    # Standardise message
    key = message.lower().rstrip(".!")

    # Look up translation
    translation = translations[language].get(key, "")

    # Store preview details
    st.session_state.preview = (message, language)
    st.session_state.edited_translation = translation


def send_message():

    message = st.session_state.draft.strip()
    language = st.session_state.language

    # Check translation is for the current message
    if st.session_state.preview != (message, language):
        return

    translated = st.session_state.edited_translation.strip()

    if not translated:
        return

    # Add message to conversation
    st.session_state.messages.append({
        "sender": "user",
        "original": message,
        "translated": translated,
        "language": language
    })

    # Reset input fields
    st.session_state.draft = ""
    st.session_state.preview = None
    st.session_state.edited_translation = ""


def clear_conversation():

    st.session_state.messages = []
    st.session_state.draft = ""
    st.session_state.preview = None
    st.session_state.edited_translation = ""


# -----------------------------------
# CONVERSATION
# -----------------------------------

st.write("### Conversation")

# Clear conversation button
st.button(
    "🗑️ Clear conversation",
    on_click=clear_conversation
)

if not st.session_state.messages:
    st.info("No messages yet. Start a conversation below.")


# Display chat messages
for message in st.session_state.messages:

    sender = message.get("sender", "user")

    # Old message formats are supported too
    if sender in ("user", "You"):
        role = "user"
    else:
        role = "assistant"

    with st.chat_message(role):

        # FIX: Handle messages from previous versions
        text = message.get(
            "translated",
            message.get(
                "text",
                message.get("original", "")
            )
        )

        st.write(text)

        # Show original underneath translated message
        if "translated" in message:

            language = message.get("language", "Unknown")
            original = message.get("original", "")

            st.caption(
                f"Translated to {language} | "
                f"Original: {original}"
            )


st.divider()


# -----------------------------------
# MESSAGE INPUT
# -----------------------------------

st.write("### New Message")

# Select language
language = st.selectbox(
    "Translate into:",
    ["Spanish", "French", "Punjabi"],
    key="language"
)

# Type message
st.text_area(
    "Type your message:",
    key="draft",
    height=100,
    placeholder="Type a message to Alex..."
)

# Preview button
st.button(
    "🌐 Preview translation",
    on_click=preview_message,
    disabled=not bool(st.session_state.draft.strip())
)


# -----------------------------------
# TRANSLATION PREVIEW
# -----------------------------------

current_preview = (
    st.session_state.draft.strip(),
    st.session_state.language
)

if st.session_state.preview == current_preview:

    st.write(f"### {language} Translation")

    # Editable translated text
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

    # Meaning check
    user_message = st.session_state.draft.lower()

    if "next friday" in user_message:
        st.warning(
            "Meaning check: 'Next Friday' could refer "
            "to different calendar dates."
        )

    elif "tomorrow" in user_message:
        st.warning(
            "Meaning check: 'Tomorrow' depends on "
            "the date and time zone."
        )

    elif "later" in user_message:
        st.warning(
            "Meaning check: 'Later' does not "
            "specify an exact time."
        )

    # Send button
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

st.caption(
    "Messages are simulated and are not delivered to a real person."
)
