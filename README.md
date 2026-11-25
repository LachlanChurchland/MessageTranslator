Meaning-Aware Message Translator

README prose word count: 1039 (excluding headings, tables and code)
Project status: Working Streamlit prototype; messages are simulated.
Testing status: Manual prototype testing completed by the developer.

1. Project Overview

This project explores how a messaging interface can help people avoid misunderstandings when communicating across languages. The prototype allows users to write an English message, optionally translate it into French, Spanish or Punjabi, inspect the result and send it to a simulated conversation with Alex.

The focus is not on building a general-purpose translation service. Instead, it explores human-centred interaction design, particularly how users can maintain control over translations, clarify ambiguous wording and recover when translations are unavailable or incorrect.

The accompanying Assignment 2 report provides the academic design rationale, architecture diagram and three illustrated storyboards. This README records the practical implementation, development decisions, testing and AI assistance.

2. Project Status and Features

Implemented functionality

Optional translation: Users can send English messages directly or enable translation.

Language selection: Predefined English translations into French, Spanish and Punjabi.

Translation preview: Users can inspect translated messages before sending.

Translation correction: Users can optionally edit a suggested translation.

Date clarification: The system offers optional clarification when the phrase "next Friday" is detected. Supported "see you" phrases can be translated with a chosen Friday date.

Risk-sensitive confirmation: An additional check is required for translated messages containing detected prices or numbered street addresses.

Error recovery: Unsupported phrases allow the user to revise their wording, enter a translation manually or send the original English.

Conversation history: Messages are displayed in a messaging-style interface, with an option to clear the conversation.

Simulated functionality

Messages appear in a simulated conversation with Alex. They are not delivered to another person. Streamlit stores the conversation in session state rather than in a persistent database.

Unimplemented or future functionality

Real messaging, user accounts, permanent conversation storage, translation of unrestricted sentences and AI-based verification of translation accuracy are not implemented.

Integrating a translation model is a possible future improvement, not a feature of the current submission.

3. Technology Stack

The application was developed using:

Python 3: Main programming language and rule-based interaction logic.

Streamlit: Web interface, message display, user inputs and session management.

Python standard library: Regular expressions for identifying predefined message patterns and hashing for managing confirmation state.

Translation dictionaries: Predefined translations and date templates.

The prototype does not use an external translation API or language model. No API key is required.

4. Installation and Running Instructions

Download or clone the GitHub repository.

Open the project folder in VS Code or another Python development environment.

Open a terminal in the project directory.

Install Streamlit and start the application:

python -m pip install streamlit
python -m streamlit run MessageTranslator.py

Open the local address displayed in the terminal, normally http://localhost:8501.

Trying the prototype

Enter Hello, select French and choose Preview translation. The predefined suggestion is Bonjour. To demonstrate ambiguity handling, enter See you next Friday and optionally specify an exact Friday. Entering The ticket costs £20 demonstrates selective confirmation. Unticking Translate before sending allows an untranslated message to be sent directly. An unfamiliar sentence demonstrates the unsupported-translation recovery options.

5. Design Decisions and Technical Reasoning

The initial project explored conversational misunderstandings in intelligent assistants. During development, the idea shifted towards multilingual messaging, retaining the underlying concerns of clarification, feedback and conversational repair.

The prototype was deliberately designed to avoid excessive interruptions. Routine translations do not require additional confirmation beyond the normal sending action. Clarification is offered when "next Friday" is detected but remains optional. Extra confirmation is reserved for detected prices and street addresses, where an incorrect translation could affect plans or costs.

When users edit the original text or switch languages, the previous preview becomes invalid and must be regenerated. For consequential details, changing the message or translated wording invalidates the previous approval. These rules help prevent stale previews and approvals from being reused.

The dictionary-based approach makes the prototype predictable, inspectable and straightforward to test. Its disadvantage is limited coverage and little context sensitivity. The system cannot translate arbitrary sentences or judge whether the suggested meaning is correct. Pattern rules may also miss important details or identify harmless text, so the interface exposes its limitations rather than implying complete language understanding.

6. Development Record

Development stage

Change, reason and review

Initial concept

Changed from the Assignment 1 reminder-assistant direction to multilingual messaging, while retaining clarification and conversational repair as the design focus.

Message interface

Added the chat history, original text, translation preview and the option to send English without translation.

Debugging

Revised message rendering after a KeyError: 'translated' revealed that earlier message records used a different structure.

Ambiguous wording

Added optional clarification of "next Friday" and expanded the supported "see you" variants after restrictive matching was identified.

Selective confirmation

Added extra approval for detected prices and street addresses, while allowing routine messages to proceed without extra warnings.

Recovery

Added manual translation entry, optional editing of available translations and a clear fallback when the dictionary has no match.

These changes demonstrate iterative development: issues found during use influenced which interactions were refined. The repository's actual commit history can provide further evidence once it is published.

7. Testing and Evaluation

Manual testing: Completed. The developer has confirmed that they ran tests on the prototype. The scenarios below document the main behaviours being checked. They are not a measured accuracy study, and individual browser observations have not been independently recorded in this README.

Test scenario

Expected behaviour

Status

Translate Hello into French

Preview displays Bonjour without an additional risk warning.

Completed (developer reported)

Turn translation off

The original English message appears in chat with Sent without translation.

Completed (developer reported)

Enter an unsupported sentence

The application explains the limitation and offers manual entry or English sending.

Completed (developer reported)

Clarify See you next Friday

Selecting a valid Friday updates a supported date translation; an invalid weekday prevents that clarified send.

Completed (developer reported)

Translate The ticket costs £20

Extra approval is required before the translated message can be sent.

Completed (developer reported)

Edit Bonjour to Salut

The edited translation is used for the simulated outgoing message.

Completed (developer reported)

Clear conversation

Displayed message history is cleared.

Completed (developer reported)

Problems addressed during development: Earlier conversation records caused a message-rendering error, and exact phrase matching initially excluded some date variations. The corresponding logic was revised. These are documented examples of review and improvement, not evidence of general translation accuracy.

Evaluation limitations: No participant usability study, accuracy benchmark, real delivery test or measured reduction in misunderstandings has been conducted. Manual checks demonstrate selected prototype interactions only. Users who do not know the target language may still be unable to judge a suggestion's correctness.

8. AI Assistance and Authorship

OpenAI ChatGPT was used during development to assist with Python and Streamlit coding refinement, debugging, the creation and revision of visual storyboards, and the organisation of project documentation. The running prototype itself does not use ChatGPT or another language model to translate messages.

Coding review and adaptation: AI-assisted code suggestions were reviewed as development problems emerged. For example, message rendering was revised after the KeyError: 'translated' issue and date handling was expanded after restrictive phrase matching was identified. Further refinements kept routine messages free from unnecessary confirmation.

Storyboard creation: AI helped create the three illustrated storyboards for routine translation, optional date clarification and translation failure recovery. They were used to explain user actions, system feedback and user choice. They are conceptual illustrations, not exact screenshots of the Streamlit interface or evidence of real message delivery.

Responsibility: The final implementation, design decisions, testing claims and submitted content remain my responsibility. AI assistance is disclosed here so the development record distinguishes assisted material from the working application.

9. Project Files and Submission

Item

Purpose

MessageTranslator.py

Main Python and Streamlit application.

README.md

Installation instructions, project scope, development record, testing and AI assistance.

Assignment 2 report

Submitted document containing the research rationale, architecture and storyboards. The report may be uploaded separately rather than stored in the GitHub repository.

Repository: The GitHub repository containing this README.
README: README.md in the root of that repository.
Submitted commit: To be identified by its exact Git commit hash when the final version is pushed.

The accompanying report must contain the public repository URL, direct README link and exact submitted commit hash. Those identifiers cannot be supplied before the repository and final commit are available. No API secrets or private information are required to run the prototype.
