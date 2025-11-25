import streamlit as st
from langchain_community.llms import Ollama

# Use gemma:2b for speed
MODEL = "gemma:2b"

# Create LLM client
llm = Ollama(model=MODEL)

# Helper to get clean text
def ask_ollama(prompt):
    try:
        response = llm.invoke(prompt)
        if isinstance(response, str):
            return response
        # LangChain responses may be nested
        if hasattr(response, "generations"):
            return response.generations[0][0].text
        return str(response)
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="AI Multi-Agent Chat", layout="wide")
st.title("🤖 Offline Multi-Agent AI (Ollama)")

# Chat message template
def chat(role, message):
    color = "#DCF8C6" if role == "User" else "#F1F0F0"
    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:12px;
            border-radius:10px;
            margin-bottom:8px;
            width:80%;
        ">
        <b>{role}:</b> <br> {message}
        </div>
        """,
        unsafe_allow_html=True
    )

task = st.text_input("Enter your task")

if st.button("Run Agents"):
    if not task.strip():
        st.warning("Please enter a task!")
    else:
        # User input
        chat("User", task)

        # Planner agent
        with st.spinner("🧠 Planner Agent thinking..."):
            plan = ask_ollama(f"Break this task into simple steps:\n{task}")
        chat("Planner Agent", plan)

        # Research agent
        with st.spinner("🔍 Research Agent thinking..."):
            research = ask_ollama(f"Explain each step in detail:\n{plan}")
        chat("Research Agent", research)

        # Decision agent
        with st.spinner("🤝 Decision Agent thinking..."):
            final = ask_ollama(f"Give final summarized result:\n{research}")
        chat("Decision Agent", final)


