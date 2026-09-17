import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Reflexion", page_icon="🪞")

st.title("Reflexion")

st.image("assets/phase2/image3.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Reflexion: Language Agents with Verbal Reinforcement Learning (Northeastern / MIT)](https://arxiv.org/abs/2303.11366)

### ⚙️ How it Works
Reflexion (Mar 2023) equips the agent with dynamic memory. It generates a response, executes or evaluates it, and if it fails, a "Reflector" LLM analyzes the trajectory, self-evaluates the failed attempt, and logs a verbal critique into a text memory bank. The next attempt reads from this memory bank to avoid repeating the mistake.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Task Input] --> B[Actor Model]
    B --> C[Draft Solution]
    C --> D[Evaluator / Env]
    D -->|Failure| E[Critique Model]
    E -->|Verbal Feedback| B
    D -->|Success| F[Final Output]
    style B fill:#eef,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#f9f,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend initiates an Actor-Evaluator loop. The `Actor` LLM generates code/text. An external `Evaluator` (like a python compiler or unit tests) tests the output. If it fails, the `Reflector` LLM is given the code and the error trace to generate a critique (e.g., "I forgot to import math"). This critique is appended to the `Actor`'s prompt for the next iteration.

### 📝 Example Prompt
```text
Write a Python function to find the longest palindromic substring in O(n) time using Manacher's algorithm.
```
""")

with st.expander("🔍 View Underlying System Prompt Template (Critique)"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase2_agentic_architecture", "prompts", "reflexion_critique.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a coding or writing task requiring iterative improvement:", value="Write a Python function to find the longest palindromic substring in O(n) time.")
if st.button("Run with Reflection"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase2/reflexion", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Evaluation Trace:**")
                for step in data["trace"]:
                    st.json(step)
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
