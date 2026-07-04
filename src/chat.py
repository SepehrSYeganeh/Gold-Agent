from google.genai import errors
import json
import streamlit as st
from .config import chat, CHAT_MODEL_NAME, HISTORY_FILE


def _append_session_to_disk():
    """
    updates the chat history file
    """
    try:
        current_session_messages = chat.get_history()

        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            for message in current_session_messages:
                role = message.role
                text = (
                    message.parts[0].text
                    if message.parts and hasattr(message.parts[0], "text")
                    else ""
                )

                log_entry = {"role": role, "content": text}

                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"\n[System Error]: Could not append history to disk: {e}")


def start_chat():
    """
    Starts a terminal chat session
    """
    st.set_page_config(
        page_title="Gold Analysis Agent",
        page_icon="🪙",
        layout="centered"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("🪙 Gold Market Analyst")
        st.caption(f"Powered by {CHAT_MODEL_NAME}")

        st.divider()

        st.subheader("Suggested Queries:")
        st.markdown("- What is the current price of gold?")
        st.markdown("- What is the status of the DXY?")
        st.markdown("- What is the current gold trend?")
        st.markdown("- Show me the gold price trend chart.")
        st.markdown("- What are the major economic news events impacting gold?")
        st.markdown("- What is your forecast for gold's short-term behavior?")

        st.divider()

    st.header("Live Market Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about the gold market..."):
        st.chat_message("user").markdown(prompt)

        # 2. Append user message to Streamlit's UI state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 3. Generate and display the assistant's response
        try:
            # Show a loading spinner while Gemini processes the tools and data
            with st.spinner("Analyzing market data..."):

                # Send the message to your existing Gemini chat object
                response = chat.send_message(prompt)

                # Display the response in the UI
                with st.chat_message("assistant"):
                    st.markdown(response.text)

                # Append the assistant's response to Streamlit's UI state
                st.session_state.messages.append({"role": "assistant", "content": response.text})

        except errors.APIError as e:
            st.error(f"Gemini API Error: {e.message} (Status Code: {e.code})")
            if e.code == 429:
                st.warning("You've hit the free tier rate limit. Please wait a moment before trying again.")
            elif e.code == 403:
                st.warning("Authentication error. Please check your GEMINI_API_KEY.")

        except Exception as e:
            st.error(f"System Error: An unexpected error occurred: {e}")


# def start_chat():
#     """
#     Starts a terminal chat session
#     """
#     print(
#         f"""
#         --- {CHAT_MODEL_NAME} ---
#         I am your Gold Market Analyst. Ask me:
#         - "What is the current price of gold?"
#         - "What is the status of the DXY?"
#         - "What is the current gold trend?"
#         - "Show me the gold price trend chart."
#         - "What are the major economic news events impacting gold?"
#         - "What is your forecast for gold's short-term behavior?"
#
#         Type 'exit' to quit.
#         """
#     )
#
#     while True:
#         try:
#             user_input = input("You: ")
#
#             if user_input.strip().lower() == "exit":
#                 _append_session_to_disk()
#                 break
#
#             if not user_input.strip():
#                 continue
#
#             response = chat.send_message(user_input)
#             print(f"\nGemini: {response.text}\n")
#
#         except errors.APIError as e:
#             # This catches specific Google API errors (Rate limits, invalid key, blocked content)
#             print(f"\n[Gemini API Error]: {e.message} (Status Code: {e.code})")
#             if e.code == 429:
#                 print("-> You've hit the free tier rate limit. Please wait a moment before trying again.\n")
#             elif e.code == 403:
#                 print("-> Authentication error. Please check your GOOGLE_API_KEY.\n")
#
#         except Exception as e:
#             # This catches unexpected errors (like local network disconnects)
#             print(f"\n[System Error]: An unexpected error occurred: {e}\n")
#
#         except KeyboardInterrupt:
#             print("\nGoodbye!")
#             _append_session_to_disk()
#             break


def test():
    pass
