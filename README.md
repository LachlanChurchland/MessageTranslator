# Meaning-Aware Message Translator

**README prose word count:** approximately 1383 (including tables and bullet points; excluding headings and code blocks)  
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

### Future development priorities (planned)

Possible extensions include a wider range of languages, translation of unknown phrases, real message delivery with appropriate privacy controls, more context-aware clarification and a multilingual user study. These are **planned directions**, not implemented capabilities in the submitted prototype.

## 3. Technology Stack

The application was developed using:

- **Python 3:** Main programming language and rule-based interaction logic.
- **Streamlit:** Web interface, message display, user inputs and session management.
- **Python standard library:** Regular expressions for identifying predefined message patterns and hashing for managing confirmation state.
- **Translation dictionaries:** Predefined translations and date templates.

The implemented scenarios use predefined translations and local Python rules. Python and Streamlit are the only required technologies.

## 4. Installation and Running Instructions

1. Download or clone the GitHub repository.
2. Open the project folder in VS Code or another Python development environment.
3. Open a terminal in the project directory.
4. Install Streamlit and start the application:

   ```bash
   python -m pip install streamlit
   python -m streamlit run MessageTranslator.py
   ```

5. Open the local address displayed in the terminal, normally `http://localhost:8501`.

### Trying the prototype

Enter `Hello`, select French and choose **Preview translation**. The predefined suggestion is `Bonjour`. To demonstrate ambiguity handling, enter `See you next Friday` and optionally specify an exact Friday. Entering `The ticket costs £20` demonstrates selective confirmation. Unticking **Translate before sending** allows an untranslated message to be sent directly. An unfamiliar sentence demonstrates the unsupported-translation recovery options.

## 5. Design Decisions and Technical Reasoning

The project changed from a reminder assistant to multilingual messaging while retaining the original focus on misunderstanding and conversational repair. Translation remains optional; date clarification is offered when relevant; and extra confirmation is restricted to detected prices and addresses. This keeps routine exchanges relatively uninterrupted.

Editing the source or changing language invalidates the previous preview. Changing a translated message with important details invalidates its approval. Predefined phrases make these interactions repeatable, at the cost of limited linguistic coverage and context sensitivity. The application therefore identifies unsupported input rather than implying that it has understood arbitrary messages.

## 6. Development Record

| Development stage | Change, reason and review |
|---|---|
| Initial concept | Changed from the Assignment 1 reminder-assistant direction to multilingual messaging, while retaining clarification and conversational repair as the design focus. |
| Message interface | Added the chat history, original text, translation preview and the option to send English without translation. |
| Debugging | Revised message rendering after a `KeyError: 'translated'` revealed that earlier message records used a different structure. |
| Ambiguous wording | Added optional clarification of "next Friday" and expanded the supported "see you" variants after restrictive matching was identified. |
| Selective confirmation | Added extra approval for detected prices and street addresses, while allowing routine messages to proceed without extra warnings. |
| Recovery | Added manual translation entry, optional editing of available translations and a clear fallback when the dictionary has no match. |

These changes demonstrate iterative development: problems encountered during use influenced the interactions that were refined. The repository's **Commits** history provides a further record of revisions.

## 7. Testing and Evaluation

**Manual testing status: Completed.** The following scenarios were run during development. The outcomes in the table are supported by checks of the corresponding Python logic. These checks are distinct from independently recorded observations of the Streamlit interface.

| Test scenario | Checked result |
|---|---|
| Translate `Hello` into French | **Pass:** French lookup returns `Bonjour` without triggering additional price or address confirmation. |
| Send with translation turned off | **Pass:** The original English message is stored in the simulated chat and marked as untranslated. |
| Enter an unsupported sentence | **Pass:** The interface provides manual translation entry and the option to send English instead. |
| Clarify `See you next Friday` | **Pass:** A valid Friday produces the supported date translation; a Thursday is rejected for the clarified path. |
| Translate `The ticket costs £20` | **Pass:** A price is detected and additional approval is required before the translated send. |
| Edit `Bonjour` to `Salut` | **Pass:** The translated message record uses the corrected wording and retains the English original. |
| Clear conversation | **Pass:** The clear action resets the conversation history, draft and preview. |

**Additional verification:** Eight source-level checks passed against the local single-file prototype on 25 November 2026, including prevention of sending from an outdated preview after the draft changes. The [`Screenshots/`](Screenshots/) folder contains supporting images of the interface. These code checks do not constitute automated browser testing or a participant study.

**Development issues addressed:** Earlier message records triggered a `KeyError: 'translated'`, which led to more tolerant message rendering. Restrictive phrase matching also prompted support for additional “next Friday” expressions.

**Evaluation limitations:** The checks assess selected interactions, not translation accuracy or a measured reduction in misunderstandings. No participant usability study or real message delivery test was conducted.

## 8. AI Assistance, Authorship and Review

**Tool and purpose:** I used OpenAI ChatGPT mainly to improve the organisation, formatting and visual layout of the report and README, help prepare illustrative translation examples and create the storyboards. I also consulted it when I could not readily identify solutions to particular development bugs. During this troubleshooting it suggested implementation changes, which I reviewed and checked against the working prototype.

| Area | My work and how AI assistance was reviewed |
|---|---|
| Project design | I selected the multilingual messaging problem and decided to demonstrate optional translation, clarification, correction and selective confirmation. These decisions responded to the interaction problems I wanted to investigate. |
| Difficult bugs | I asked ChatGPT to help explain a `KeyError: 'translated'` caused by older chat records and the limited recognition of variations of “next Friday”. I examined the suggested changes, adapted the message handling and date examples, and checked the relevant interaction paths. |
| Translation examples | ChatGPT helped suggest wording for the short French, Spanish and Punjabi demonstration phrases and date-related examples. These are fixed examples used to demonstrate the interface, not independently validated translations or evidence of general translation accuracy. |
| Layout and illustrations | ChatGPT helped organise and format the report and README and generate the storyboard illustrations. I reviewed the figures and corrected an inaccurate English-send control and fictional delivery indicators so the illustrations better reflected the prototype. |

**Authorship and limitations:** Some implementation suggestions came from ChatGPT during development and debugging, but the submitted project decisions, review of suggested changes and testing record are my responsibility. The storyboards are illustrative rather than screenshots. Academic research is cited in the report; actual interface screenshots are in [`Screenshots/`](Screenshots/).

## 9. Project Files and Submission

| Item | Purpose |
|---|---|
| `MessageTranslator.py` | Main Python and Streamlit application. |
| `README.md` | Installation instructions, project scope, development record, testing and AI assistance. |
| Assignment 2 report | Submitted document containing the research rationale, architecture and storyboards. It may be uploaded separately. |
| `Screenshots/` | Screenshots of selected working Streamlit interface states, separate from the illustrated storyboards. |

**Repository:** [MessageTranslator on GitHub](https://github.com/LachlanChurchland/MessageTranslator).  
**README:** [README.md on GitHub](https://github.com/LachlanChurchland/MessageTranslator/blob/main/README.md).  
**Repository commit recorded for this report:** [`07b45eb1653559339ce13b190b3b3d3221ad6a69`](https://github.com/LachlanChurchland/MessageTranslator/commit/07b45eb1653559339ce13b190b3b3d3221ad6a69).

The report identifies the same repository checkpoint. **After pushing any further changes, replace the hash in both the README and the report with the new final commit hash.** No private credentials are needed to run the prototype.
