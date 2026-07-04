from google.genai import errors
import json
import streamlit as st
from .config import chat, CHAT_MODEL_NAME, HISTORY_FILE


def _append_session_to_disk(role: str, content: str):
    """
    updates the chat history file
    """
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            log_entry = {"role": role, "content": content}

            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"\n[System Error]: Could not append history to disk: {e}")


def render_chat():
    """
    Renders the Streamlit chat interface
    """
    st.set_page_config(
        page_title="Gold Analysis Agent",
        page_icon="🪙",
        layout="centered"
    )

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

    # init history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # show history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # new message
    if prompt := st.chat_input("Ask me anything about the gold market..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        _append_session_to_disk("user", prompt)

        try:
            with st.spinner("Analyzing market data..."):
                response = chat.send_message(prompt)

                with st.chat_message("assistant"):
                    st.markdown(response.text)

                st.session_state.messages.append({"role": "assistant", "content": response.text})
                _append_session_to_disk("assistant", response.text)

        except errors.APIError as e:
            st.error(f"Gemini API Error: {e.message} (Status Code: {e.code})")
            if e.code == 429:
                st.warning("You've hit the free tier rate limit. Please wait a moment before trying again.")
            elif e.code == 403:
                st.warning("Authentication error. Please check your GEMINI_API_KEY.")

        except Exception as e:
            st.error(f"System Error: An unexpected error occurred: {e}")
