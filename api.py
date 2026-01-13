# api.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from core.agent import JarvisAgent
from memory.task_store import TaskStore

router = APIRouter()
store = TaskStore()


# -------- Schemas --------

class ExecuteRequest(BaseModel):
    goal: str


class ExecuteResponse(BaseModel):
    status: str
    result: str
    confidence: Optional[str] = None


# -------- Routes --------

@router.get("/")
def root():
    return {
        "message": "JARVIS backend running",
        "status": "healthy"
    }


@router.post("/execute", response_model=ExecuteResponse)
def execute_task(req: ExecuteRequest):
    agent = JarvisAgent(req.goal, fast_mode=True)
    results = agent.run()

    if not results:
        return ExecuteResponse(
            status="failed",
            result="No meaningful output produced"
        )

    final = results[-1]

    if "RESULT_FAILED" in final:
        return ExecuteResponse(
            status="failed",
            result=final
        )

    if "LOW CONFIDENCE" in final:
        return ExecuteResponse(
            status="completed",
            result=final,
            confidence="low"
        )

    return ExecuteResponse(
        status="completed",
        result=final,
        confidence="high"
    )


@router.post("/continue", response_model=ExecuteResponse)
def continue_last_task():
    task = store.get_last_incomplete_task()
    if not task:
        return ExecuteResponse(
            status="idle",
            result="No incomplete task found"
        )

    agent = JarvisAgent(task["goal"], fast_mode=True)
    agent.task = task
    agent.planner_steps = task["steps"]
    results = agent.act()

    final = results[-1] if results else "No output"

    return ExecuteResponse(
        status=task["status"],
        result=final
    )


@router.get("/memory")
def memory_dump():
    return store._load()
