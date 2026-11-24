import streamlit as st
from langchain_ollama import ChatOllama

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="LLM Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Chat Assistant")
st.caption("Powered by Streamlit + LangChain + Ollama")

# ---------------------------------
# Sidebar Configuration
# ---------------------------------

with st.sidebar:
    st.header("Settings")

    model_name = st.selectbox(
        "Select LLM Model",
        ["beam:cloud", "llama3.1", "qwen2.5", "mistral"]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------
# Initialize LLM
# ---------------------------------

llm = ChatOllama(
    model=model_name,
    temperature=temperature,
    #base_url="http://localhost:11434"
)

# ---------------------------------
# Initialize Chat History
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------
# Display Previous Messages
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# Chat Input
# ---------------------------------

if prompt := st.chat_input("Ask your question..."):

    # Display user message

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate LLM response

    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in llm.stream(
                st.session_state.messages
            ):
                full_response += chunk.content

                response_placeholder.markdown(
                    full_response + "▌"
                )

            response_placeholder.markdown(full_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"LLM Error: {str(e)}")