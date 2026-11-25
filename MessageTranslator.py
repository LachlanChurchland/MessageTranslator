
import hashlib
import re
import streamlit as st

st.set_page_config(page_title="Message Translator", page_icon="💬")
st.title("💬 Message Translator")
st.subheader("Chat with Alex")
st.caption("Messaging prototype — nothing is sent to a real person")

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
        "see you next friday": "Nos vemos el próximo viernes.",
        "the ticket costs £20": "La entrada cuesta 20 libras.",
        "meet me at 12 king street": "Nos vemos en el número 12 de King Street.",
        "eyesight": "Vista",
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
        "see you next friday": "À vendredi prochain.",
        "the ticket costs £20": "Le billet coûte 20 livres sterling.",
        "meet me at 12 king street": "Retrouve-moi au 12 King Street.",
        "eyesight": "Vue",
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
        "see you next friday": "ਅਗਲੇ ਸ਼ੁੱਕਰਵਾਰ ਮਿਲਾਂਗੇ",
        "the ticket costs £20": "ਟਿਕਟ ਦੀ ਕੀਮਤ 20 ਪੌਂਡ ਹੈ।",
        "meet me at 12 king street": "ਮੈਨੂੰ 12 ਕਿੰਗ ਸਟ੍ਰੀਟ 'ਤੇ ਮਿਲੋ।",
        "eyesight": "ਨਜ਼ਰ",
    },
}

# -----------------------------------
# MONTH NAMES
# -----------------------------------

month_names = {
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
    ],
}

# -----------------------------------
# SESSION STATE
# -----------------------------------

for state_key, default in {
    "messages": [],
    "draft": "",
    "preview": None,
    "preview_number": 0,
}.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default


# -----------------------------------
# FUNCTIONS
# -----------------------------------

def normalise(text):
    return " ".join(
        text.strip()
        .lower()
        .replace("’", "'")
        .rstrip(".!? ")
        .split()
    )


def important_details(text):
    """
    Detect important details using predefined
    text patterns, not an AI model.
    """

    findings = []

    weekday = (
        r"monday|tuesday|wednesday|thursday|"
        r"friday|saturday|sunday"
    )

    month = (
        r"january|february|march|april|may|june|"
        r"july|august|september|october|november|december"
    )

    # Check for dates
    date_pattern = (
        rf"\b(?:today|tomorrow|tonight|{weekday})\b"
        rf"|\b\d{{1,2}}\s+(?:{month})\b"
        rf"|\b(?:{month})\s+\d{{1,2}}\b"
        r"|\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b"
        r"|\b\d{4}-\d{2}-\d{2}\b"
    )

    if re.search(date_pattern, text, re.IGNORECASE):
        findings.append("Date or time")

    # Check for prices
    price_pattern = (
        r"[£€$₹]\s*\d[\d,.]*"
        r"|\b\d[\d,.]*\s*"
        r"(?:pounds?|euros?|dollars?|rupees?|gbp|usd|eur)\b"
    )

    if re.search(price_pattern, text, re.IGNORECASE):
        findings.append("Price or payment amount")

    # Check for street addresses
    street_pattern = (
        r"\b\d{1,5}\s+"
        r"(?:[A-Za-z.'-]+\s+){0,4}"
        r"(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|"
        r"Drive|Dr|Boulevard|Blvd)\b"
    )

    if re.search(street_pattern, text, re.IGNORECASE):
        findings.append("Street address")

    return findings


def translated_date(example_date, language):

    day = example_date.day
    month = month_names[language][example_date.month - 1]
    year = example_date.year

    if language == "Spanish":
        return f"Nos vemos el {day} de {month} de {year}."

    if language == "French":
        return f"Je te verrai le {day} {month} {year}."

    return f"{day} {month} {year} ਨੂੰ ਮਿਲਾਂਗੇ।"


def preview_message():

    draft = st.session_state.draft.strip()

    if draft:
        st.session_state.preview = (
            draft,
            st.session_state.language
        )

        st.session_state.preview_number += 1


def clear_conversation():

    st.session_state.messages = []
    st.session_state.draft = ""
    st.session_state.preview = None


def send_message(
    original,
    translation_field,
    language,
    confirmation_field,
    can_proceed
):

    # Check that the preview is still valid
    if not can_proceed:
        return

    if st.session_state.preview != (
        st.session_state.draft.strip(),
        st.session_state.language
    ):
        return

    translated = st.session_state.get(
        translation_field, ""
    ).strip()

    if not translated:
        return

    # Require approval for important details
    if important_details(original + "\n" + translated):

        if (
            not confirmation_field
            or not st.session_state.get(
                confirmation_field, False
            )
        ):
            return

    # Store the simulated message
    st.session_state.messages.append({
        "sender": "user",
        "original": original,
        "translated": translated,
        "language": language,
    })

    # Reset input fields
    st.session_state.draft = ""
    st.session_state.preview = None


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

for item in st.session_state.messages:

    role = (
        "user"
        if item.get("sender", "user") in ("user", "You")
        else "assistant"
    )

    with st.chat_message(role):

        st.write(
            item.get(
                "translated",
                item.get(
                    "text",
                    item.get("original", "")
                )
            )
        )

        if "translated" in item:
            st.caption(
                f"Translated to {item.get('language', 'Unknown')} | "
                f"Original: {item.get('original', '')}"
            )

st.divider()


# -----------------------------------
# NEW MESSAGE
# -----------------------------------

st.write("### New message")

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
    disabled=not bool(
        st.session_state.draft.strip()
    )
)


# -----------------------------------
# TRANSLATION AND CLARIFICATION
# -----------------------------------

current_preview = (
    st.session_state.draft.strip(),
    st.session_state.language
)

if st.session_state.preview == current_preview:

    original, language = current_preview
    key = normalise(original)

    revised_original = original

    translated = {
        normalise(k): v
        for k, v in translations[language].items()
    }.get(key, "")

    selected_date = None
    choice = "Not needed"
    ready = True

    # -----------------------------------
    # DETECT "NEXT FRIDAY"
    # -----------------------------------

    if re.search(
        r"\bnext\s+friday\b",
        original,
        re.IGNORECASE
    ):

        st.warning(
            "'Next Friday' may refer to different dates. "
            "Would you like to clarify?"
        )

        choice = st.radio(
            "How would you like to handle this?",
            [
                "Keep original wording",
                "Specify exact date"
            ],
            index=None,
            key=f"choice_{st.session_state.preview_number}",
        )

        ready = choice is not None

        # -----------------------------------
        # EXACT DATE CLARIFICATION
        # -----------------------------------

        if choice == "Specify exact date":

            selected_date = st.date_input(
                "Which exact Friday do you mean?",
                value=None,
                key=f"date_{st.session_state.preview_number}",
            )

            if selected_date is None:
                ready = False

            elif selected_date.weekday() != 4:
                st.warning("Please choose a Friday.")
                ready = False

            else:

                date_text = (
                    f"{selected_date.day} "
                    f"{selected_date.strftime('%B')} "
                    f"{selected_date.year}"
                )

                revised_original = re.sub(
                    r"\bnext\s+friday\b",
                    f"on {date_text}",
                    original,
                    flags=re.IGNORECASE
                )

                supported = {
                    "i will see you next friday",
                    "i'll see you next friday",
                    "see you next friday"
                }

                if key in supported:

                    translated = translated_date(
                        selected_date,
                        language
                    )

                else:

                    translated = ""

                    st.info(
                        "The demo has no automatic date "
                        "translation for this sentence. "
                        "Enter it manually."
                    )

    # -----------------------------------
    # MESSAGE PREVIEW
    # -----------------------------------

    st.write("### Message preview")
    st.info(revised_original)

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
        st.session_state[edit_key] = translated

    st.text_area(
        f"Review or edit {language} translation:",
        key=edit_key,
        height=100
    )

    current_translation = (
        st.session_state[edit_key].strip()
    )

    if not current_translation:
        st.warning(
            "No automatic translation found. "
            "Enter one manually to continue."
        )

    # -----------------------------------
    # RISK-SENSITIVE CONFIRMATION
    # -----------------------------------

    risks = important_details(
        revised_original + "\n" + current_translation
    )

    confirm_key = None

    if risks:

        st.warning(
            "⚠️ Important details detected: "
            + ", ".join(risks)
            + ". Check them before sending."
        )

        st.caption(
            "This is a basic keyword/pattern check, "
            "not a guarantee that the translation is accurate."
        )

        # Create a different approval checkbox
        # if the message or translation changes
        content_signature = hashlib.sha256(
            (
                f"{st.session_state.preview_number}|"
                f"{revised_original}|"
                f"{language}|"
                f"{current_translation}"
            ).encode("utf-8")
        ).hexdigest()[:16]

        confirm_key = f"approve_{content_signature}"

        approved = st.checkbox(
            "I have checked these details "
            "and approve this translation",
            key=confirm_key,
        )

        ready = ready and approved

    # -----------------------------------
    # SEND MESSAGE
    # -----------------------------------

    st.button(
        (
            "✅ Confirm & send (simulation)"
            if risks
            else "📤 Send message (simulation)"
        ),
        on_click=send_message,
        args=(
            revised_original,
            edit_key,
            language,
            confirm_key,
            ready
        ),
        disabled=not (
            ready
            and bool(current_translation)
        ),
    )

elif st.session_state.preview is not None:

    st.info(
        "Your message or language changed. "
        "Preview again before sending."
    )

st.caption(
    "Simulated messaging only. "
    "Translations use predefined examples, not an AI API."
)
