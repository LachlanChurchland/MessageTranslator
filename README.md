# Meaning-Aware Message Translator

**Project status:** Working Streamlit prototype; messages are simulated.

## 1. Project Overview

This project explores how a messaging interface can help people avoid misunderstandings when communicating across languages. The prototype allows users to write an English message, optionally translate it into **French, Spanish or Punjabi**, inspect the result and send it to a simulated conversation with Alex.

The focus is not on building a general-purpose translation service. Instead, it explores **human-centred interaction design**, particularly how users can maintain control over translations, clarify ambiguous wording and recover when translations are unavailable or incorrect.

## 2. Project Status and Features

### Implemented functionality

- **Optional translation:** Users can send English messages directly or enable translation.
- **Language selection:** Predefined English translations into French, Spanish and Punjabi.
- **Translation preview:** Users can inspect translated messages before sending.
- **Translation correction:** Users can optionally edit a suggested translation.
- **Date clarification:** The system offers optional clarification when the phrase "next Friday" is detected.
- **Risk-sensitive confirmation:** An additional check is required for translated messages containing detected prices or street addresses.
- **Error recovery:** Unsupported translations provide alternatives, including sending the original English message or entering a translation manually.
- **Conversation history:** Messages are displayed in a messaging-style interface, with an option to clear the conversation.

### Simulated functionality

Messages appear in a simulated conversation with Alex. They are not delivered to another person.

### Unimplemented or future functionality

Real messaging, user accounts, permanent conversation storage, automatic translation of unrestricted sentences and AI-based verification of translation accuracy are not implemented.

Integrating a translation model is a possible future improvement, not a feature of the current submission.

## 3. Technology Stack

The application was developed using:

- **Python 3:** Main programming language and rule-based interaction logic.
- **Streamlit:** Web interface, message display, user inputs and session management.
- **Python standard library:** Regular expressions for identifying predefined message patterns and hashing for managing confirmation state.
- **Translation dictionaries:** Predefined translations and date templates.

The prototype does not use an external translation API or language model. No API key is required.

## 4. Installation and Running Instructions

1. Download or clone the GitHub repository.
2. Open the project folder in VS Code or another Python development environment.
3. Open a terminal in the project directory.
4. Install Streamlit:

   `python -m pip install streamlit`

5. Start the application:

   `python -m streamlit run MessageTranslator.py`

6. Open the local address displayed in the terminal, normally:

   `http://localhost:8501`

### Trying the prototype

Enter `Hello`, select French and preview the translation. To demonstrate ambiguity handling, enter `See you next Friday` and optionally specify an exact date.

Entering `The ticket costs £20` demonstrates risk-sensitive confirmation.

Unticking **Translate before sending** allows users to send an untranslated message directly.

## 5. Design Decisions and Technical Reasoning

The initial project explored conversational misunderstandings in intelligent assistants. During development, the idea shifted towards multilingual messaging, retaining the underlying concerns of clarification, feedback and conversational repair.

The prototype was deliberately designed to avoid excessive interruptions.

Routine translations do not require additional confirmation beyond the normal sending action. Clarification is offered when "next Friday" is detected but remains optional. Extra confirmation is reserved for detected prices and street addresses, where an incorrect translation
