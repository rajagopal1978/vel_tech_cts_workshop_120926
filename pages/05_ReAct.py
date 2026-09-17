import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="ReAct", page_icon="🤖")

st.title("ReAct (Reason + Act)")

st.image("assets/phase2/image1.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[ReAct: Synergizing Reasoning and Acting in Language Models (Princeton / Google Brain)](https://arxiv.org/abs/2210.03629)

### ⚙️ How it Works
ReAct (Oct 2022) interleaves step-by-step reasoning logs with real-world tool execution in a "Thought, Action, Observation" loop. By giving language models the ability to execute API calls (like searching Wikipedia or using a calculator), they can dynamically fetch data they need to proceed with their reasoning instead of hallucinating.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[User Prompt] --> B[LLM Thought]
    B --> C[Action: Tool Call]
    C --> D[Observation]
    D --> B
    D --> E[Final Answer]
    style B fill:#f9f,stroke:#333
    style C fill:#9cf,stroke:#333
    style D fill:#dfd,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend implements a `while` loop. In each iteration, the prompt (which includes the history of thoughts/actions/observations) is sent to the LLM. If the LLM generates an `Action` (e.g., `Search[Apple]`), the backend intercepts it, runs a real Python function to get the `Observation`, appends it to the prompt, and continues the loop until the LLM outputs a `Finish` action.

### 📝 Example Prompt
```text
Question: What is the profession of the person who created the Ruby programming language?
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase2_agentic_architecture", "prompts", "react.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a task requiring external knowledge:", value="Question: What is the profession of the person who created the Ruby programming language?")
if st.button("Run Agent"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase2/react", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Execution Trace:**")
                for step in data["trace"]:
                    st.json(step)
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
