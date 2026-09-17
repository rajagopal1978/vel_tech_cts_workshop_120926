import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Least-to-Most", page_icon="📝")

st.title("Least-to-Most Prompting")

st.image("assets/phase1/image4.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Least-to-Most Prompting Enables Complex Reasoning in Large Language Models (Google Strategy)](https://arxiv.org/abs/2205.10625)

### ⚙️ How it Works
Least-to-Most Prompting (Apr 2022) breaks down a complex problem into a series of simpler sub-problems. It solves them sequentially, feeding the answers of the previously solved sub-problems into the prompt for the next sub-problem.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Complex Problem] --> B[LLM Decomposer]
    B --> C[Sub-Problem 1]
    B --> D[Sub-Problem 2]
    B --> E[Sub-Problem N]
    C --> F[LLM Solver: SP1]
    F --> G[Context for SP2]
    G --> H[LLM Solver: SP2]
    H --> I[...Final Answer]
    style B fill:#eef,stroke:#333,stroke-width:2px
    style F fill:#dfd,stroke:#333
    style H fill:#dfd,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend performs two main stages. Stage 1: The model is prompted to decompose the user's problem into a list of sub-questions. Stage 2: A loop iterates over the sub-questions. For each question, the model is prompted with the original problem, the history of answered sub-questions, and the current sub-question to solve.

### 📝 Example Prompt
```text
Question: Amy is 5 years older than Bob. Bob is 3 times as old as Charlie. Charlie was born 2 years ago. How old is Amy?
```
""")

with st.expander("🔍 View Underlying System Prompt Template (Decompose)"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase1_prompt_engineering", "prompts", "least_to_most_decompose.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a complex logic problem:", value="Question: Amy is 5 years older than Bob. Bob is 3 times as old as Charlie. Charlie was born 2 years ago. How old is Amy?")
if st.button("Generate Answer"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase1/least_to_most", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Sequential Sub-problem Resolution:**")
                st.success(data["simulated_response"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
