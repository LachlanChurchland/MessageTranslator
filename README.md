# Meaning-Aware Message Translator

**README prose word count:** approximately 1189 (excluding headings, tables and code)  
**Project status:** Working Streamlit prototype; messages are simulated.  
**Testing status:** Manual prototype testing completed by the developer.

## 1. Project Overview

This project explores how a messaging interface can help people avoid misunderstandings when communicating across languages. The prototype allows users to write an English message, optionally translate it into **French, Spanish or Punjabi**, inspect the result and send it to a simulated conversation with Alex.

The focus is not on building a general-purpose translation service. Instead, it explores **human-centred interaction design**, particularly how users can maintain control over translations, clarify ambiguous wording and recover when translations are unavailable or incorrect.

The accompanying Assignment 2 report provides the academic design rationale, architecture diagram and three illustrated storyboards. This README records the practical implementation, development decisions, testing and AI assistance.

## 2. Project Status and Features

### Implemented functionality

- **Optional translation:** Users can send English messages directly or enable translation.
- **Language selection:** Predefined English translations into French, Spanish and Punjabi.
- **Translation preview:** Users can inspect translated messages before sending.
- **Translation correction:** Users can optionally edit a suggested translation.
- **Date clarification:** The system offers optional clarification when the phrase "next Friday" is detected. Supported "see you" phrases can be translated with a chosen Friday date.
- **Risk-sensitive confirmation:** An additional check is required for translated messages containing detected prices or numbered street addresses.
- **Error recovery:** Unsupported phrases allow the user to revise their wording, enter a translation manually or send the original English.
- **Conversation history:** Messages are displayed in a messaging-style interface, with an option to clear the conversation.

### Simulated functionality

Messages appear in a simulated conversation with Alex. They are not delivered to another person. Streamlit stores the conversation in session state rather than in a persistent database.

### Unimplemented or future functionality

Real messaging, user accounts, permanent conversation storage, translation of unrestricted sentences and AI-based verification of translation accuracy are not implemented.

### Future development priorities

If the prototype were developed into a practical messaging application, I would prioritise:

- **More languages:** Expand beyond French, Spanish and Punjabi, allowing users to select from a wider range of languages and potentially translate in both directions.
- **Translation API integration:** Connect to an established translation service so messages outside the predefined dictionary could be translated. The interface would still show previews, correction options and clear uncertainty or failure messages.
- **Real messaging integration:** Replace the simulated conversation with authenticated contacts and actual message delivery, including appropriate privacy and security controls.
- **Better handling of meaning and context:** Improve detection of ambiguous wording, names
