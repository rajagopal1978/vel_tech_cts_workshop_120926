import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Self-Consistency", page_icon="📝")

st.title("Self-Consistency")

st.image("assets/phase1/image3.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Self-Consistency Improves Chain of Thought Reasoning in Language Models (Google Brain)](https://arxiv.org/abs/2203.11171)

### ⚙️ How it Works
Self-Consistency (Mar 2022) mitigates the risk of the model going down a flawed reasoning path. Instead of generating a single Chain-of-Thought, the system queries the model multiple times with a high temperature to generate diverse reasoning paths. It then parses the final answer from each path and selects the most frequent answer (majority vote) as the final output.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Prompt] -->|High Temp| B[LLM Path 1]
    A -->|High Temp| C[LLM Path 2]
    A -->|High Temp| D[LLM Path N]
    B --> E[Answer Extractor]
    C --> E
    D --> E
    E --> F[Majority Vote Voting Logic]
    F --> G[Final Consensus Answer]
    style B fill:#eef,stroke:#333
    style C fill:#eef,stroke:#333
    style D fill:#eef,stroke:#333
    style F fill:#dfd,stroke:#333,stroke-width:2px
""")

st.markdown("""

### 💻 Code Explanation
The backend takes the prompt and fires off $N$ (e.g., 3 for demo) parallel API requests to the LLM. Once all $N$ responses return, a parsing function extracts the final numerical or logical answer from the end of each trace. A simple `Counter` is used to find the majority vote, which is returned to the user.

### 📝 Example Prompt
```text
If John has 5 pears, eats 2, and buys 5 more, and gives half to his friend. How many does he have?
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase1_prompt_engineering", "prompts", "self_consistency.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a math problem:", value="If John has 5 pears, eats 2, and buys 5 more, and gives half to his friend. How many does he have?")
if st.button("Generate Answer"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase1/self_consistency", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Diverse Paths & Majority Vote:**")
                st.success(data["simulated_response"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
