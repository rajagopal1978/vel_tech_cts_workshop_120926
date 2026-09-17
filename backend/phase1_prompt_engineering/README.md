# Phase 1: The Prompt Engineering Era (2022–2023)
Focus: Figuring out that text formatting and "in-context learning" can unlock step-by-step reasoning.

## Techniques:
- **Chain-of-Thought (CoT) Prompting (Jan 2022)**: Elicits reasoning by showing a few examples containing intermediate steps.
- **Zero-Shot CoT (May 2022)**: Discovered that simply appending the phrase "Let's think step by step" forces the model to generate its own reasoning chain without needing examples.
- **Self-Consistency (Mar 2022)**: Generates multiple diverse CoT paths for a single prompt and takes the majority vote to pick the most common final answer.
- **Least-to-Most Prompting (Apr 2022)**: Dynamically breaks a complex problem down into a sub-question list and solves them sequentially.
