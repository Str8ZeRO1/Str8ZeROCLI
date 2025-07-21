from fastapi import FastAPI, Request
from str8zero_core import Str8ZeroCore

app = FastAPI()

@app.post("/build/")
async def build_app(request: Request):
    data = await request.json()
    user_context = data.get("user_id", "default")
    prompt = data["prompt"]
    core = Str8ZeroCore(user_context, prompt)
    result = core.build()
    return result
