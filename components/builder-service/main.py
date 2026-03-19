from typing import Optional, Any
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from arduino_blocks import arduino_block_coder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class BuilderRequest(BaseModel):
    preset: str
    username: Optional[str] = None
    page: Optional[str] = None
    drawer_content: Optional[Any] = None

@app.post("/builder", response_class=HTMLResponse)
def builder(req: BuilderRequest):
    html = arduino_block_coder(
        preset=req.preset,
        username=req.username,
        page=req.page,
        drawer_content=req.drawer_content,
        return_html=True,
        is_overlay=True,
    )
    return html

@app.get("/health")
def health():
    return {"status": "ok"}