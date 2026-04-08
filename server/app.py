from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from server.environment import CodeReviewEnv

from typing import Optional

app = FastAPI(title="OpenEnv Code Review Space")

_env = None

class ActionRequest(BaseModel):
    action: str

class ResetRequest(BaseModel):
    difficulty: str = "medium"

@app.get("/")
def ping():
    return {"status": "ok", "message": "Hugging Face Space is running"}

@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    global _env
    difficulty = req.difficulty if req else "medium"
    _env = CodeReviewEnv(difficulty=difficulty)
    obs = _env.reset()
    return {"observation": obs, "status": "reset_successful"}

@app.post("/step")
def step(req: ActionRequest):
    global _env
    if _env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    obs, reward, done, error = _env.step(req.action)
    return {
        "observation": obs,
        "reward": float(reward) if reward else 0.0,
        "done": done,
        "error": error
    }

@app.get("/state")
def state():
    global _env
    if _env is None:
        return {"status": "uninitialized"}
    return {
        "steps_taken": _env.steps_taken,
        "rewards": _env.rewards,
        "difficulty": _env.difficulty,
        "correct_comments": _env.correct_comments
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
