from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai

router = APIRouter()
client = openai.OpenAI()

def load_prompt(filename, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    if not os.path.exists(path):
        return f"Fallback prompt for {filename}: {kwargs.get('USER_PROMPT', '')}"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for k, v in kwargs.items():
        content = content.replace(f"{{{k}}}", str(v))
    return content

class PromptRequest(BaseModel):
    prompt: str

@router.post("/openai_o1")
def openai_o1_simulate(req: PromptRequest):
    # o1 does not take system prompts in the same way, but we will pass the user prompt.
    # Note: We didn't explicitly create an o1.md because o1 natively ignores instructions like "think step by step".
    # We will just pass the user prompt for demonstration.
    model = "o1-preview"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": req.prompt}]
        )
    except:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": req.prompt}]
        )
    return {
        "approach": "OpenAI o1 Native Reasoning",
        "prompt": req.prompt,
        "internal_thought_process": f"[Thought process handled natively by {model}. Hidden from API.]",
        "final_answer": response.choices[0].message.content
    }

@router.post("/deepseek_r1")
def deepseek_r1(req: PromptRequest):
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    prompt_text = load_prompt("deepseek_r1.md", USER_PROMPT=req.prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}]
    )
    content = response.choices[0].message.content
    think_part = ""
    ans_part = content
    if "<think>" in content and "</think>" in content:
        think_part = content.split("</think>")[0].replace("<think>", "").strip()
        ans_part = content.split("</think>")[1].strip()
    return {
        "approach": "DeepSeek-R1 Native Reasoning",
        "prompt": req.prompt,
        "internal_thought_process": think_part,
        "final_answer": ans_part
    }

@router.post("/maker")
def maker(req: PromptRequest):
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    orch_prompt = load_prompt("maker_orchestrator.md", USER_PROMPT=req.prompt)
    decomp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": orch_prompt}]
    ).choices[0].message.content
    
    comp_prompt = load_prompt("maker_compiler.md", USER_PROMPT=req.prompt, DECOMP=decomp)
    final = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": comp_prompt}]
    ).choices[0].message.content
    
    return {
        "approach": "MAKER Massively Decomposed Processes",
        "prompt": req.prompt,
        "internal_thought_process": decomp,
        "final_answer": final
    }



