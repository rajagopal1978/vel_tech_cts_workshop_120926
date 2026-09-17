import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="ReWOO", page_icon="🚀")

st.title("ReWOO")

st.image("assets/phase2/image5.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models (Xu et al.)](https://arxiv.org/abs/2305.18323)

### ⚙️ How it Works
ReWOO (May 2023) decouples reasoning from execution to create highly efficient, parallel tool graphs. Instead of waiting for tool observations sequentially (like ReAct), ReWOO generates a comprehensive tool execution graph upfront. Workers execute the independent tools in parallel, and a final solver synthesizes the results.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[User Task] --> B[Planner LLM]
    B -->|Decoupled DAG| C[Parallel Execution]
    C --> D[Worker: Web Search]
    C --> E[Worker: Calculator]
    C --> F[Worker: Database]
    D --> G[Solver LLM]
    E --> G
    F --> G
    G --> H[Final Synthesized Output]
    style B fill:#f9f,stroke:#333
    style G fill:#f9f,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend uses a `Planner` LLM to generate a dependency graph of actions. It parses this graph and dispatches independent `Worker` threads (using `asyncio` or ThreadPools) to execute API calls concurrently. Once all promises are resolved and observations are collected, the `Solver` LLM takes the initial prompt and all observations to generate the final response, significantly saving on token costs and latency.

### 📝 Example Prompt
```text
Find the current weather in New York and the current stock price of Apple.
```
""")

with st.expander("🔍 View Underlying System Prompt Template (Planner)"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase2_agentic_architecture", "prompts", "rewoo_plan.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a task requiring parallel tool execution:", value="Find the current weather in New York and the current stock price of Apple.")
if st.button("Run ReWOO"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase2/rewoo", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Simulated Execution Trace:**")
                for step in data["trace"]:
                    st.json(step)
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
