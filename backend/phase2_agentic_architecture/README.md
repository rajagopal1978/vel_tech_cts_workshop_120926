# Phase 2: The Agentic Architecture Era (2023–Early 2024)
Focus: Wrapping the linear CoT loops into code-driven loops (external tools, search graphs, and self-evaluation loops).

## Architectures:
- **ReAct (Reason + Act)**: Interleaves step-by-step reasoning logs with real-world tool execution ("Thought, Action, Observation").
- **Tree-of-Thoughts (ToT)**: Allows the agent to branch out multiple self-contained reasoning paths and evaluate them, enabling algorithms like BFS/DFS to backtrack when a path fails.
- **Reflexion**: Equips the agent with dynamic memory. It self-evaluates failed attempts and logs the critique into a text memory bank to avoid repeating mistakes.
- **LATS (Language Agent Tree Search)**: Unifies ToT, ReAct, and Reflexion by mapping reasoning into a Monte Carlo Tree Search (MCTS) loop, using internal rewards to select paths.
- **ReWOO**: Decouples reasoning from execution to create highly efficient, parallel tool graphs.
