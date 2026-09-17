import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="OpenAI o1 Series", page_icon="🧠")

st.title("OpenAI o1 Series")

st.image("assets/phase3/image1.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[OpenAI o1 System Card (OpenAI)](https://openai.com/index/openai-o1-system-card/)

### ⚙️ How it Works
The OpenAI o1 series shifts reasoning from prompting tricks to native inference-time computation. The model uses reinforcement learning to "think" internally before responding. It autonomously generates a hidden chain of thought, self-corrects, and prunes bad ideas without requiring external scaffolds like ReAct or ToT.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[User Prompt] --> B[RL-Trained Model]
    B --> C[Hidden Chain of Thought Loop]
    C --> D[Self-Correction / Verification]
    D --> C
    C --> E[Final Answer Emission]
    style C fill:#fcc,stroke:#333,stroke-dasharray: 5 5
    style D fill:#fcc,stroke:#333,stroke-dasharray: 5 5
""")

st.markdown("""

### 💻 Code Explanation
From a backend perspective, implementing o1 is trivially simple. You do not provide a "system prompt" instructing it to think step-by-step; the model ignores such instructions anyway. You simply pass the user prompt to the `o1-preview` or `o1-mini` model, and wait for the response.

### 📝 Example Prompt
```text
Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4]' and prints the transpose in the same format.
```
""")

st.header("Interactive Example")
prompt = st.text_area("Enter a very complex reasoning task:", value="Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4]' and prints the transpose in the same format.")
if st.button("Reason Native"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase3/openai_o1", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                with st.expander("Internal Thought Process (Hidden)"):
                    st.info(data["internal_thought_process"])
                st.write("**Final Answer:**")
                st.success(data["final_answer"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
