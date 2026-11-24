
import streamlit as st

st.title("Message Translator")
st.write("Enter a message to translate from English to Spanish.")

# Example translations
translations = {
    "hello": "Hola",
    "how are you?": "¿Cómo estás?",
    "thank you": "Gracias",
    "good morning": "Buenos días",
    "are you free tomorrow?": "¿Estás libre mañana?",
    "see you later": "Hasta luego",
    "i will see you next friday": "Nos vemos el próximo viernes"
}

# User input
message = st.text_input("Enter your message:")

if st.button("Translate"):

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        # Standardise the message for matching
        user_message = message.strip().lower()

        st.write("Original message:")
        st.info(message)

        # Find a predefined translation
        if user_message in translations:
            translation = translations[user_message]

            st.write("Spanish translation:")
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

        elif "later" in user_message:
            st.warning(
                "Meaning check: 'Later' does not specify an exact time."
            )

        elif "next friday" in user_message:
            st.warning(
                "Meaning check: 'Next Friday' could refer "
                "to different calendar dates."
            )
