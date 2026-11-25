
import hashlib
import re
import streamlit as st

st.set_page_config(page_title="Message Translator", page_icon="💬")

st.title("💬 Message Translator")
st.subheader("Chat with Alex")
st.caption("Messaging prototype — messages are simulated")


# -----------------------------------
# PREDEFINED TRANSLATIONS
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

if "messages" not in st.session_state:
    st.session_state.messages = []

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "preview" not in st.session_state:
    st.session_state.preview = None

if "preview_number" not in st.session_state:
    st.session_state.preview_number = 0

if "translate_before_sending" not in st.session_state:
    st.session_state.translate_before_sending = True


# -----------------------------------
# FUNCTIONS
# -----------------------------------

def normalise(text):
    """Standardise messages for dictionary matching."""

    return " ".join(
        text.strip()
        .lower()
        .replace("’", "'")
        .rstrip(".!? ")
        .split()
    )


def sensitive_details(text):
    """
    Detect prices and addresses that deserve
    additional confirmation.
    """

    found = []

    price_pattern = (
        r"[£€$₹]\s*\d[\d,.]*"
        r"|\b\d[\d,.]*\s*"
        r"(?:pounds?|euros?|dollars?|rupees?|gbp|usd|eur)\b"
    )

    address_pattern = (
        r"\b\d{1,5}\s+"
        r"(?:[A-Za-z.'-]+\s+){0,4}"
        r"(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|"
        r"Drive|Dr|Boulevard|Blvd)\b"
    )

    if re.search(price_pattern, text, re.IGNORECASE):
        found.append("price")

    if re.search(address_pattern, text, re.IGNORECASE):
        found.append("street address")

    return found


def translated_date(date, language):
    """Translate the date for supported examples."""

    day = date.day
    month = month_names[language][date.month - 1]
    year = date.year

    if language == "Spanish":
        return f"Nos vemos el {day} de {month} de {year}."

    if language == "French":
        return f"Je te verrai le {day} {month} {year}."

    return f"{day} {month} {year} ਨੂੰ ਮਿਲਾਂਗੇ।"


def reset_preview():
    st.session_state.preview = None


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


def send_original(message=None, from_preview=False, ready=True):
    """Send a message without translating it."""

    if not ready:
        return

    if from_preview:

        if not st.session_state.translate_before_sending:
            return

        if st.session_state.preview != (
            st.session_state.draft.strip(),
            st.session_state.language
        ):
            return

        text = message.strip()

    else:

        if st.session_state.translate_before_sending:
            return

        text = st.session_state.draft.strip()

    if not text:
        return

    st.session_state.messages.append({
        "sender": "user",
        "text": text,
        "untranslated": True
    })

    st.session_state.draft = ""
    st.session_state.preview = None


def send_translated(
    original,
    language,
    translation,
    confirm_key,
    ready=True
):

    if not ready:
        return

    if not st.session_state.translate_before_sending:
        return

    if st.session_state.preview != (
        st.session_state.draft.strip(),
        st.session_state.language
    ):
        return

    if not translation.strip():
        return

    # Confirm only sensitive information
    if sensitive_details(original):

        if (
            not confirm_key
            or not st.session_state.get(confirm_key, False)
        ):
            return

    st.session_state.messages.append({
        "sender": "user",
        "original": original,
        "translated": translation.strip(),
        "language": language
    })

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

    sender = item.get("sender", "user")

    role = (
        "user"
        if sender in ("user", "You")
        else "assistant"
    )

    with st.chat_message(role):

        text = item.get(
            "translated",
            item.get(
                "text",
                item.get("original", "")
            )
        )

        st.write(text)

        if "translated" in item:

            st.caption(
                f"Translated to {item.get('language', 'Unknown')} | "
                f"Original: {item.get('original', '')}"
            )

        elif item.get("untranslated"):

            st.caption("Sent without translation")


st.divider()


# -----------------------------------
# MESSAGE INPUT
# -----------------------------------

st.write("### New message")

st.checkbox(
    "Translate before sending",
    key="translate_before_sending",
    on_change=reset_preview
)

if st.session_state.translate_before_sending:

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


# -----------------------------------
# SEND WITHOUT TRANSLATION
# -----------------------------------

if not st.session_state.translate_before_sending:

    st.button(
        "📤 Send original message",
        on_click=send_original,
        disabled=not bool(
            st.session_state.draft.strip()
        )
    )


# -----------------------------------
# TRANSLATION MODE
# -----------------------------------

else:

    st.button(
        "🌐 Preview translation",
        on_click=preview_message,
        disabled=not bool(
            st.session_state.draft.strip()
        )
    )

    current_preview = (
        st.session_state.draft.strip(),
        st.session_state.language
    )

    if st.session_state.preview == current_preview:

        original, language = current_preview

        key = normalise(original)

        revised_original = original

        # Find matching translation
        translation = next(
            (
                value
                for phrase, value in translations[language].items()
                if normalise(phrase) == key
            ),
            ""
        )

        ready = True
        selected_date = None


        # -----------------------------------
        # OPTIONAL DATE CLARIFICATION
        # -----------------------------------

        if re.search(
            r"\bnext\s+friday\b",
            original,
            re.IGNORECASE
        ):

            st.info(
                "'Next Friday' can mean different dates."
            )

            clarify = st.checkbox(
                "Specify the exact Friday (optional)",
                key=f"clarify_{st.session_state.preview_number}"
            )

            if clarify:

                selected_date = st.date_input(
                    "Choose the intended Friday:",
                    value=None,
                    key=f"date_{st.session_state.preview_number}"
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
                        r"\b(?:on\s+)?next\s+friday\b",
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

                        translation = translated_date(
                            selected_date,
                            language
                        )

                    else:

                        translation = ""


        # -----------------------------------
        # MESSAGE PREVIEW
        # -----------------------------------

        st.write("### Message preview")

        st.caption(f"English: {revised_original}")

        date_id = (
            selected_date.isoformat()
            if selected_date
            else "none"
        )

        edit_key = (
            f"edit_{st.session_state.preview_number}_"
            f"{language}_{date_id}"
        )


        # -----------------------------------
        # TRANSLATION AVAILABLE
        # -----------------------------------

        if translation:

            st.info(
                f"Suggested translation: {translation}"
            )

            # NEW: Editing is optional
            edit_choice = st.checkbox(
                "✏️ Translation looks wrong? Edit it",
                key=(
                    f"edit_choice_"
                    f"{st.session_state.preview_number}_"
                    f"{date_id}"
                )
            )

            if edit_key not in st.session_state:
                st.session_state[edit_key] = translation

            if edit_choice:

                st.text_area(
                    "Correct the translated message:",
                    key=edit_key,
                    height=90
                )

                final_translation = (
                    st.session_state[edit_key].strip()
                )

            else:

                final_translation = translation


        # -----------------------------------
        # TRANSLATION UNAVAILABLE
        # -----------------------------------

        else:

            st.info(
                "This wording isn't in the demo's "
                "translation library. You can rephrase "
                "it above, send the English message, "
                "or enter a translation yourself."
            )

            if edit_key not in st.session_state:
                st.session_state[edit_key] = ""

            st.text_area(
                "Enter your own translation (optional):",
                key=edit_key,
                height=90
            )

            final_translation = (
                st.session_state[edit_key].strip()
            )

            # Let user send original text instead
            st.button(
                "📤 Send English instead",
                on_click=send_original,
                args=(
                    revised_original,
                    True,
                    ready
                ),
                disabled=not ready
            )


        # -----------------------------------
        # RISK-SENSITIVE CONFIRMATION
        # -----------------------------------

        risks = (
            sensitive_details(revised_original)
            if final_translation
            else []
        )

        confirm_key = None

        if risks:

            st.warning(
                "Please check the "
                + " and ".join(risks)
                + " in the translation."
            )

            # Confirmation resets when translation changes
            signature = hashlib.sha256(
                (
                    f"{revised_original}|"
                    f"{language}|"
                    f"{final_translation}"
                ).encode("utf-8")
            ).hexdigest()[:16]

            confirm_key = (
                f"approve_"
                f"{st.session_state.preview_number}_"
                f"{signature}"
            )

            approved = st.checkbox(
                "I've checked these important details",
                key=confirm_key
            )

            ready = ready and approved


        # -----------------------------------
        # SEND TRANSLATED MESSAGE
        # -----------------------------------

        if final_translation:

            st.button(
                "📤 Send translated message",
                on_click=send_translated,
                args=(
                    revised_original,
                    language,
                    final_translation,
                    confirm_key,
                    ready
                ),
                disabled=not ready
            )


    elif st.session_state.preview is not None:

        st.info(
            "Your message or language changed. "
            "Preview again before sending."
        )


st.caption(
    "Simulated messages only. Automatic translation "
    "uses predefined phrases, not an AI API."
)
