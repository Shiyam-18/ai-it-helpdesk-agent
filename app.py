import streamlit as st
from dotenv import load_dotenv

from src.agent import HelpdeskAgent
from src.config import settings

load_dotenv()

st.set_page_config(
    page_title="AI IT Helpdesk Agent",
    page_icon="🛠️",
    layout="wide",
)

@st.cache_resource
def get_agent():
    return HelpdeskAgent()

agent = get_agent()

st.title("🛠️ AI IT Helpdesk Agent")
st.caption("TN Skill Project — Agent + RAG + Tools")

with st.sidebar:
    st.header("Project Components")
    st.write("✅ AI Agent")
    st.write("✅ RAG Knowledge Base")
    st.write("✅ Tool Calling")
    st.write("✅ SQLite Support Tickets")
    st.divider()
    st.write(f"LLM: `{settings.gemini_model}`")
    st.write(f"Embedding: `{settings.embedding_model}`")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Describe your IT problem (e.g. Wi-Fi connected but no internet)"
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Diagnosing the issue..."):
            try:
                result = agent.handle(
                    user_message=prompt,
                    history=st.session_state.messages[:-1],
                )
                answer = result["answer"]
                st.markdown(answer)

                if result.get("sources"):
                    with st.expander("📚 Knowledge Base Sources"):
                        for source in result["sources"]:
                            st.write(f"- `{source}`")

                if result.get("tool_events"):
                    with st.expander("🔧 Agent Tool Activity"):
                        for event in result["tool_events"]:
                            st.write(f"- {event}")

            except Exception as exc:
                answer = (
                    "I could not complete the request.\n\n"
                    f"**Error:** `{exc}`\n\n"
                    "Check your `.env` file and make sure the Gemini API key is valid."
                )
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
