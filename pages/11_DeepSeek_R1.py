import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="DeepSeek-R1", page_icon="🐋")

st.title("DeepSeek-R1")

st.image("assets/phase3/image2.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (DeepSeek-AI)](https://arxiv.org/abs/2501.12948)

### ⚙️ How it Works
Unlike OpenAI's o1 which hides its reasoning trace, DeepSeek-R1 is trained via pure Reinforcement Learning to emit its entire raw thinking process surrounded by `<think>` tags. The model exhibits emergent self-verification and reflection natively within this token block.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[User Prompt] --> B[R1 Model]
    B --> C["<think> tag generation start"]
    C --> D[Internal CoT / Self-Verification]
    D --> C
    D --> E["</think> tag generation end"]
    E --> F[Final Answer]
    style C fill:#eef,stroke:#333
    style E fill:#eef,stroke:#333
    style D fill:#dfd,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend simply hits the R1 API (or simulates it using a strong model prompted to use tags). Once the payload returns, the backend splits the string by `</think>` to cleanly separate the raw reasoning trace from the final polished answer.

### 📝 Example Prompt
```text
If I have a 3 gallon jug and a 5 gallon jug, how do I measure exactly 4 gallons of water?
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase3_native_reasoning", "prompts", "deepseek_r1.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a complex mathematical or coding task:", value="How many 'r's are in the word strawberry? Explain your counting carefully.")
if st.button("Reason Native (Open Thoughts)"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase3/deepseek_r1", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Visible Internal Thought Process (`<think>`):**")
                st.code(data["internal_thought_process"], language="markdown")
                st.write("**Final Answer:**")
                st.success(data["final_answer"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
