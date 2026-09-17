import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Zero-Shot CoT", page_icon="📝")

st.title("Zero-Shot CoT")

st.image("assets/phase1/image2.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Large Language Models are Zero-Shot Reasoners (University of Tokyo / Google)](https://arxiv.org/abs/2205.11916)

### ⚙️ How it Works
Zero-Shot CoT (May 2022) discovered that you do not need to provide manual, hand-crafted examples to elicit step-by-step reasoning. By simply appending the magic phrase `"Let's think step by step"` to the user's prompt, the model is forced into a mode where it generates its own reasoning chain before providing the final answer.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[User Prompt] --> B["Append: 'Let's think step by step'"]
    B --> C[LLM Processing]
    C --> D[Generate Step-by-step Reasoning]
    D --> E[Output Final Answer]
    style C fill:#f9f,stroke:#333,stroke-width:2px
""")

st.markdown("""

### 💻 Code Explanation
The FastAPI backend receives the raw user prompt. Before sending it to the OpenAI API, the backend code automatically concatenates `\\n\\nLet's think step by step.` to the end of the prompt. This modified string is what the LLM actually sees and processes.

### 📝 Example Prompt
```text
I went to the market and bought 10 apples. I gave 2 to my neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase1_prompt_engineering", "prompts", "zero_shot_cot.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a complex math or logic question:", value="I went to the market and bought 10 apples. I gave 2 to my neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?")
if st.button("Generate Answer"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase1/zero_shot_cot", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Modified Prompt Sent to LLM:**")
                st.code(data["modified_prompt"])
                st.write("**Simulated Response:**")
                st.success(data["simulated_response"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
