import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Standard CoT", page_icon="📝")

st.title("Standard Chain-of-Thought (CoT)")

st.image("assets/phase1/image1.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Google Brain)](https://arxiv.org/abs/2201.11903)

### ⚙️ How it Works
Chain-of-Thought (CoT) Prompting (Jan 2022) is the fundamental discovery that language models can solve complex reasoning tasks if they are prompted to generate intermediate reasoning steps before answering. Instead of asking for the final answer immediately, you provide a few examples ("Few-Shot") that demonstrate step-by-step logic. The model mimics this structure to solve the new problem.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Few-Shot Examples] --> B[User Prompt]
    B --> C[LLM Processing]
    C --> D[Generate Step-by-step Reasoning]
    D --> E[Output Final Answer]
    style C fill:#f9f,stroke:#333,stroke-width:2px
""")

st.markdown("""

### 💻 Code Explanation
In the backend, this algorithm doesn't require an agentic loop. It simply takes the user's prompt and formats it alongside a few predefined examples containing reasoning paths before sending it to the LLM API. The LLM then generates the thought process followed by the final answer.

### 📝 Example Prompt
```text
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase1_prompt_engineering", "prompts", "standard_cot.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a complex question (similar to the example above):", value="Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?")
if st.button("Generate Answer"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase1/standard_cot", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Response:**")
                st.success(data["simulated_response"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
