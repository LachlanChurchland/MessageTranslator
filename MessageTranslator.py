
import streamlit as st

st.title("Message Translator")
st.write("Enter a message to translate.")

# Spanish translations
spanish_translations = {
    "hello": "Hola",
    "how are you?": "¿Cómo estás?",
    "thank you": "Gracias",
    "good morning": "Buenos días",
    "are you free tomorrow?": "¿Estás libre mañana?",
    "see you later": "Hasta luego",
    "i will see you next friday": "Nos vemos el próximo viernes"
}

# French translations
french_translations = {
    "hello": "Bonjour",
    "how are you?": "Comment ça va ?",
    "thank you": "Merci",
    "good morning": "Bonjour",
    "are you free tomorrow?": "Tu es libre demain ?",
    "see you later": "À plus tard",
    "i will see you next friday": "Je te verrai vendredi prochain"
}

# Select translation language
language = st.selectbox(
    "Select translation language:",
    ["Spanish", "French"]
)

# User input
message = st.text_input("Enter your message:")

if st.button("Translate"):

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        # Standardise the message
        user_message = message.strip().lower()

        st.write("Original message:")
        st.info(message)

        # Choose the correct translation dictionary
        if language == "Spanish":
            translations = spanish_translations
        else:
            translations = french_translations

        # Find the translation
        if user_message in translations:
            translation = translations[user_message]

            st.write(f"{language} translation:")
            st.success(translation)

        else:
            st.warning(
                "This message is not available in the demo translator yet."
            )

        # Detect potentially ambiguous wording
        if "tomorrow" in user_message:
            st.warning(
                "Meaning check: 'Tomorrow' depends on the date "
                "and time zone of the conversation."
            )

        elif "next friday" in user_message:
            st.warning(
                "Meaning check: 'Next Friday' could refer "
                "to different calendar dates."
            )

        elif "later" in user_message:
            st.warning(
                "Meaning check: 'Later' does not specify an exact time."
            )
