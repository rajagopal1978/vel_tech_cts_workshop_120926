import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import render_mermaid
import requests
import os

st.set_page_config(page_title="MAKER", page_icon="🏭")

st.title("MAKER & Massively Decomposed Processes")

st.image("assets/phase3/image3.png", use_container_width=True)

st.markdown("""
### 📄 Reference Paper
[From Chain-of-Thought to Massively Decomposed Agentic Processes (2026 Research Overview)](#)

### ⚙️ How it Works
Moving beyond single-agent architectures, Massively Decomposed Processes (like the theoretical MAKER framework) avoid context collapse on massive, long-horizon tasks (e.g., building a complete OS from scratch). It orchestrates a massive Directed Acyclic Graph (DAG) of thousands of micro-agents, each solving tiny atomic tasks, and recompiles them into a master deliverable.

### 🧠 Logic Architecture (Mermaid)
""")

render_mermaid("""
graph TD
    A[Massive Long-Horizon Task] --> B[MAKER Orchestrator]
    B --> C[DAG of 1000s of Micro-Tasks]
    C --> D[Swarm of Specialized Agents]
    D --> E[Sub-task Compilation]
    E --> F[MAKER Compiler]
    F --> G[Final Master Output]
    style B fill:#f9f,stroke:#333
    style F fill:#f9f,stroke:#333
    style D fill:#dfd,stroke:#333
""")

st.markdown("""

### 💻 Code Explanation
The backend simulates a massively scalable architecture. An `Orchestrator` LLM breaks down a huge user request into a JSON structure of sub-tasks. In a real system, these would queue into an asynchronous pub/sub system for thousands of micro-agents. Finally, a `Compiler` LLM combines the results into a cohesive final output.

### 📝 Example Prompt
```text
Write a full-stack, production-ready Twitter clone from scratch, including frontend, backend, database migrations, CI/CD pipelines, and unit tests, and deploy it to AWS.
```
""")

with st.expander("🔍 View Underlying System Prompt Template (Orchestrator)"):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "phase3_native_reasoning", "prompts", "maker_orchestrator.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.error("Prompt file not found.")

st.header("Interactive Example")
prompt = st.text_area("Enter a massive, multi-stage project requirement:", value="Write a full-stack, production-ready Twitter clone from scratch, including frontend, backend, database migrations, CI/CD pipelines, and unit tests.")
if st.button("Decompose & Execute"):
    if prompt:
        try:
            response = requests.post("http://127.0.0.1:8000/api/phase3/maker", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.write("**Agent Coordination Process:**")
                st.info(data["internal_thought_process"])
                st.write("**Compiled Final Output:**")
                st.success(data["final_answer"])
            else:
                st.error("Error connecting to backend.")
        except Exception as e:
            st.error(f"Connection failed: {e}")
