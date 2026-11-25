import streamlit as st
import asyncio
import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from AGENT.Agent import run_agent


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="KLayout AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 KLayout AI Assistant")

st.caption(
    "Streamlit + LangChain + Ollama + MCP"
)


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.header("Configuration")

    st.text("LLM: Ollama beam:cloud")

    st.text("MCP: FastMCP HTTP")

    if st.button("Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# --------------------------------
# Initialize session
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------
# Display chat history
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------
# User input
# --------------------------------

if prompt := st.chat_input("Ask KLayout AI something..."):

    # Display user message

    with st.chat_message("user"):

        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Execute LangChain agent

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Connecting to MCP and executing..."
            ):

                response, tools = asyncio.run(
                    run_agent(
                        st.session_state.messages
                    )
                )

            st.markdown(response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            # Show available MCP tools
            with st.expander("Available MCP Tools"):

                for tool in tools:
                    st.write(
                        f"- {tool.name}: {tool.description}"
                    )

        except Exception as e:

            st.error(
                f"Application Error: {str(e)}"
            )