import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="Tree of Thoughts", page_icon="🌳")

st.title("Tree of Thoughts (ToT)")

st.image("assets/phase2/image2.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[Tree of Thoughts: Deliberate Problem Solving with Large Language Models (Princeton / Google DeepMind)](https://arxiv.org/abs/2305.10601)

### ⚙️ How it Works
Tree-of-Thoughts (May 2023) frames problem solving as search over a tree where each node represents a partial solution or thought. It allows the agent to branch out multiple self-contained reasoning paths and evaluate them. This enables classic search algorithms like BFS/DFS to backtrack when a path fails.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Start State] --> B[Branch 1]
    A --> C[Branch 2]
    A --> D[Branch 3]
    B --> E[Evaluate: Fail / Prune]
    C --> F[Evaluate: Success]
    D --> G[Evaluate: Fail / Prune]
    F --> H[Final Answer]
    style C fill:#dfd,stroke:#333
    style B fill:#fcc,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend uses a search algorithm (like Breadth-First Search). At each step, it prompts the LLM to generate $K$ possible next "thoughts" (branches). Then, it prompts an LLM evaluator to score each thought (e.g., sure/maybe/impossible). The search keeps the top-scoring branches and discards the impossible ones, iteratively building a tree of thoughts until a solution is reached.

### 📝 Example Prompt
```text
Solve the Game of 24: Use the numbers [4, 9, 10, 13] and basic arithmetic operations (+, -, *, /) to reach 24.
```
""")

with st.expander("🔍 View Underlying System Prompt Template"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase2_agentic_architecture", "prompts", "tot.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a planning or combinatorial search task:", value="Solve the Game of 24: Use the numbers [4, 9, 10, 13]")
if st.button("Run Search"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase2/tree_of_thoughts", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Exploration Trace:**")
                for step in data["trace"]:
                    st.json(step)
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
