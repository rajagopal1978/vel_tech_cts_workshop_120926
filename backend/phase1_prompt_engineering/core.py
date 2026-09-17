from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai
from collections import Counter

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

@router.post("/standard_cot")
def standard_cot(req: PromptRequest):
    prompt_text = load_prompt("standard_cot.md", USER_PROMPT=req.prompt)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_text}]
    )
    return {"approach": "Standard CoT", "modified_prompt": prompt_text, "simulated_response": response.choices[0].message.content}

@router.post("/zero_shot_cot")
def zero_shot_cot(req: PromptRequest):
    prompt_text = load_prompt("zero_shot_cot.md", USER_PROMPT=req.prompt)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_text}]
    )
    return {"approach": "Zero-Shot CoT", "modified_prompt": prompt_text, "simulated_response": response.choices[0].message.content}

@router.post("/self_consistency")
def self_consistency(req: PromptRequest):
    prompt_text = load_prompt("self_consistency.md", USER_PROMPT=req.prompt)
    paths = []
    for _ in range(3): # N=3 for demonstration speed
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7
        )
        paths.append(response.choices[0].message.content)
    return {"approach": "Self-Consistency", "modified_prompt": prompt_text, "simulated_response": "\n\n---\n\n".join(paths)}

@router.post("/least_to_most")
def least_to_most(req: PromptRequest):
    # Step 1: Decompose
    decompose_prompt = load_prompt("least_to_most_decompose.md", USER_PROMPT=req.prompt)
    sub_questions = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": decompose_prompt}]
    ).choices[0].message.content
    
    # Step 2: Solve with context
    solve_prompt = load_prompt("least_to_most_solve.md", USER_PROMPT=req.prompt, SUB_QUESTIONS=sub_questions)
    final_solution = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": solve_prompt}]
    ).choices[0].message.content
    
    return {"approach": "Least-to-Most Prompting", "modified_prompt": solve_prompt, "simulated_response": final_solution}



