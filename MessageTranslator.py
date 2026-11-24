
import re
import streamlit as st

st.set_page_config(page_title="Message Translator", page_icon="💬")

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
        "i will see you next friday": "Nos vemos el próximo viernes.",
        "i'll see you next friday": "Nos vemos el próximo viernes.",
        "eyesight": "Vista"
    },
    "French": {
        "hello": "Bonjour",
        "how are you?": "Comment ça va ?",
        "thank you": "Merci",
        "good morning": "Bonjour",
        "are you free tomorrow?": "Tu es libre demain ?",
        "see you later": "À plus tard",
        "i will see you next friday": "Je te verrai vendredi prochain.",
        "i'll see you next friday": "Je te verrai vendredi prochain.",
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
        "i'll see you next friday": "ਅਗਲੇ ਸ਼ੁੱਕਰਵਾਰ ਮਿਲਾਂਗੇ",
        "eyesight": "ਨਜ਼ਰ"
    }
}

# Month names for the date clarification example
months = {
    "Spanish": [
        "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"
    ],
    "French": [
        "janvier", "février", "mars", "avril",
        "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"
    ],
    "Punjabi": [
        "ਜਨਵਰੀ", "ਫ਼ਰਵਰੀ", "ਮਾਰਚ", "ਅਪ੍ਰੈਲ",
        "ਮਈ", "ਜੂਨ", "ਜੁਲਾਈ", "ਅਗਸਤ",
        "ਸਤੰਬਰ", "ਅਕਤੂਬਰ", "ਨਵੰਬਰ", "ਦਸੰਬਰ"
    ]
}

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "preview" not in st.session_state:
    st.session_state.preview = None

if "preview_number" not in st.session_state:
    st.session_state.preview_number = 0


# -----------------------------------
# FUNCTIONS
# -----------------------------------

def normalise(text):
    return text.strip().lower().rstrip(".! ")


def preview_message():
    message = st.session_state.draft.strip()

    if message:
        st.session_state.preview = (
            message,
            st.session_state.language
        )

        st.session_state.preview_number += 1


def send_message(original, translation_key, language):
    translated = st.session_state[translation_key].strip()

    if not translated:
        return

    st.session_state.messages.append({
        "sender": "user",
        "original": original,
        "translated": translated,
        "language": language
    })

    st.session_state.draft = ""
    st.session_state.preview = None


def clear_conversation():
    st.session_state.messages = []
    st.session_state.draft = ""
    st.session_state.preview = None


def clarify_example_translation(selected_date, language):
    """
    Translate the clarified version of the known
    'I will see you next Friday' example.
    """

    day = selected_date.day
    month = months[language][selected_date.month - 1]
    year = selected_date.year

    if language == "Spanish":
        return f"Nos vemos el {day} de {month} de {year}."

    elif language == "French":
        return f"Je te verrai le {day} {month} {year}."

    else:
        return f"{day} {month} {year} ਨੂੰ ਮਿਲਾਂਗੇ।"


# -----------------------------------
# CONVERSATION
# -----------------------------------

st.write("### Conversation")

st.button(
    "🗑️ Clear conversation",
    on_click=clear_conversation
)

if not st.session_state.messages:
    st.info("No messages yet. Start a conversation below.")

for message in st.session_state.messages:

    with st.chat_message("user"):

        # Support messages from older versions too
        text = message.get(
            "translated",
            message.get("text", message.get("original", ""))
        )

        st.write(text)

        if "translated" in message:
            st.caption(
                f"Translated to {message.get('language', 'Unknown')} | "
                f"Original: {message.get('original', '')}"
            )

st.divider()


# -----------------------------------
# NEW MESSAGE
# -----------------------------------

st.write("### New Message")

st.selectbox(
    "Translate into:",
    ["Spanish", "French", "Punjabi"],
    key="language"
)

st.text_area(
    "Type your message:",
    key="draft",
    height=100,
    placeholder="Type a message to Alex..."
)

st.button(
    "🌐 Preview translation",
    on_click=preview_message,
    disabled=not bool(st.session_state.draft.strip())
)


# -----------------------------------
# TRANSLATION & CLARIFICATION
# -----------------------------------

current_preview = (
    st.session_state.draft.strip(),
    st.session_state.language
)

if st.session_state.preview == current_preview:

    original, language = current_preview
    key = normalise(original)

    translation = translations[language].get(key, "")
    revised_original = original

    ready_to_send = True
    choice = "Not needed"
    selected_date = None

    # Detect "next Friday"
    if re.search(r"\bnext friday\b", original, re.IGNORECASE):

        st.warning(
            "⚠️ 'Next Friday' could refer to different dates. "
            "Would you like to clarify it?"
        )

        choice = st.radio(
            "How would you like to handle this?",
            ["Keep original wording", "Specify exact date"],
            index=None,
            key=f"choice_{st.session_state.preview_number}"
        )

        # Require a choice before sending
        ready_to_send = choice is not None

        # User chooses to clarify
        if choice == "Specify exact date":

            selected_date = st.date_input(
                "Which exact Friday do you mean?",
                value=None,
                key=f"date_{st.session_state.preview_number}"
            )

            if selected_date is None:
                ready_to_send = False

            elif selected_date.weekday() != 4:
                st.warning("Please select a Friday.")
                ready_to_send = False

            else:
                # Replace "next Friday" with the chosen date
                date_text = (
                    f"{selected_date.day} "
                    f"{selected_date.strftime('%B')} "
                    f"{selected_date.year}"
                )

                revised_original = re.sub(
                    r"\bnext friday\b",
                    f"on {date_text}",
                    original,
                    flags=re.IGNORECASE
                )

                # Automatic date translation only for
                # our supported example sentence
                supported_examples = {
                    "i will see you next friday",
                    "i'll see you next friday"
                }

                if key in supported_examples:
                    translation = clarify_example_translation(
                        selected_date,
                        language
                    )

                else:
                    translation = ""

                    st.info(
                        "This sentence is not supported by the "
                        "demo's date translations. "
                        "Enter the translation manually."
                    )

    # Display the message after any clarification
    st.write("### Message preview")
    st.info(revised_original)

    # Use a new editable field whenever the date or
    # clarification choice changes
    date_id = (
        selected_date.isoformat()
        if selected_date is not None
        else "none"
    )

    edit_key = (
        f"edit_{st.session_state.preview_number}_"
        f"{language}_{choice}_{date_id}"
    )

    if edit_key not in st.session_state:
        st.session_state[edit_key] = translation

    st.text_area(
        f"Review or edit {language} translation:",
        key=edit_key,
        height=100
    )

    if not st.session_state[edit_key].strip():
        st.warning(
            "No predefined translation found. "
            "Enter a translation manually to continue."
        )

    # Send only after the user has handled the warning
    st.button(
        "📤 Send message",
        on_click=send_message,
        args=(revised_original, edit_key, language),
        disabled=not (
            ready_to_send
            and bool(st.session_state[edit_key].strip())
        )
    )

elif st.session_state.preview is not None:

    st.info(
        "Your message or language has changed. "
        "Preview the translation again before sending."
    )

st.caption(
    "All messages are simulated. "
    "Nothing is sent to another person."
)
