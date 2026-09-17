import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="LATS", page_icon="🌲")

st.title("Language Agent Tree Search (LATS)")

st.image("assets/phase2/image4.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[LATS: Language Agent Tree Search as a Unified Framework for Reasoning and Acting (UIUC / Allen Institute)](https://arxiv.org/abs/2310.04406)

### ⚙️ How it Works
LATS (Oct 2023) unifies ToT, ReAct, and Reflexion by mapping reasoning into a Monte Carlo Tree Search (MCTS) loop. It uses environment feedback (tools) and self-reflection to generate internal rewards, balancing exploration of new reasoning paths and exploitation of known good paths.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Root Node] -->|MCTS Selection| B[Node 1]
    B -->|MCTS Expansion| C[Node 2]
    C -->|Evaluation| D[Reward Score]
    D -->|Backpropagation| B
    style A fill:#eef,stroke:#333
    style D fill:#dfd,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend implements MCTS. A node represents the state of reasoning. During `Selection`, the algorithm chooses the most promising node using the UCT formula. During `Expansion`, the LLM generates new possible actions. During `Simulation/Evaluation`, the LLM (and tools) evaluate the path and generate a reward score (0.0 to 1.0). During `Backpropagation`, this reward updates the values of parent nodes.

### 📝 Example Prompt
```text
Design a relational database schema for a ride-sharing app.
```
""")

with st.expander("🔍 View Underlying System Prompt Template (Expand)"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase2_agentic_architecture", "prompts", "lats.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a task for MCTS exploration:", value="Design a relational database schema for a ride-sharing app.")
if st.button("Run LATS"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase2/lats", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated MCTS Trace:**")
                for step in data["trace"]:
                    st.json(step)
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
