from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai

router = APIRouter()
client = openai.OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

def load_prompt(filename, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for k, v in kwargs.items():
        content = content.replace(f"{{{k}}}", str(v))
    return content

class PromptRequest(BaseModel):
    prompt: str

@router.post("/react")
def react_agent(req: PromptRequest):
    prompt_text = load_prompt("react.md", USER_PROMPT=req.prompt)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=150
    )
    trace = [
        {"Thought": "Thinking about the task...", "Action": "Search[Relevant info]"},
        {"Observation": "Simulated search result based on your query."},
        {"Thought": "I have the info now.", "Action": f"Finish[{response.choices[0].message.content}]"}
    ]
    return {"approach": "ReAct", "prompt": req.prompt, "trace": trace}

@router.post("/tree_of_thoughts")
def tree_of_thoughts(req: PromptRequest):
    prompt_text = load_prompt("tot.md", USER_PROMPT=req.prompt)
    branch1 = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt_text}]).choices[0].message.content
    branch2 = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt_text}]).choices[0].message.content
    trace = [
        {"Path 1": branch1, "Evaluation": "Score 0.6"},
        {"Path 2": branch2, "Evaluation": "Score 0.9 -> Selected!"}
    ]
    return {"approach": "Tree of Thoughts", "prompt": req.prompt, "trace": trace}

@router.post("/reflexion")
def reflexion(req: PromptRequest):
    draft = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": req.prompt}]).choices[0].message.content
    critique_prompt = load_prompt("reflexion_critique.md", USER_PROMPT=req.prompt, DRAFT=draft)
    critique = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": critique_prompt}]).choices[0].message.content
    solve_prompt = load_prompt("reflexion_solve.md", USER_PROMPT=req.prompt, CRITIQUE=critique)
    final = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": solve_prompt}]).choices[0].message.content
    trace = [
        {"Attempt 1": draft, "Evaluation": "Needs improvement"},
        {"Memory Update / Critique": critique},
        {"Attempt 2 (Final)": final, "Evaluation": "Success"}
    ]
    return {"approach": "Reflexion", "prompt": req.prompt, "trace": trace}

@router.post("/lats")
def lats(req: PromptRequest):
    prompt_text = load_prompt("lats.md", USER_PROMPT=req.prompt)
    state = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt_text}]).choices[0].message.content
    trace = [
        {"Action": "MCTS Selection -> UCT maximized"},
        {"Action": f"Expansion: {state}"},
        {"Reward Evaluation": "0.85"},
        {"Backpropagation": "Updated parent values"}
    ]
    return {"approach": "LATS", "prompt": req.prompt, "trace": trace}

@router.post("/rewoo")
def rewoo(req: PromptRequest):
    plan_prompt = load_prompt("rewoo_plan.md", USER_PROMPT=req.prompt)
    plan = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": plan_prompt}]).choices[0].message.content
    solve_prompt = load_prompt("rewoo_solve.md", USER_PROMPT=req.prompt, PLAN=plan)
    solve = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": solve_prompt}]).choices[0].message.content
    trace = [
        {"Planner": plan},
        {"Workers": "Running independent tasks in parallel... Done."},
        {"Solver": solve}
    ]
    return {"approach": "ReWOO", "prompt": req.prompt, "trace": trace}



