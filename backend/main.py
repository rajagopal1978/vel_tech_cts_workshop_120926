from fastapi import FastAPI
from dotenv import load_dotenv
import os
from backend.phase1_prompt_engineering.core import router as phase1_router
from backend.phase2_agentic_architecture.core import router as phase2_router
from backend.phase3_native_reasoning.core import router as phase3_router

load_dotenv()

app = FastAPI(title="Chain-of-Thought Evolution Showcase API")

app.include_router(phase1_router, prefix="/api/phase1", tags=["Phase 1: Prompt Engineering"])
app.include_router(phase2_router, prefix="/api/phase2", tags=["Phase 2: Agentic Architecture"])
app.include_router(phase3_router, prefix="/api/phase3", tags=["Phase 3: Native Reasoning"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CoT Showcase API"}

