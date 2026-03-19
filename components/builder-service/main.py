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
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuilderRequest(BaseModel):
    preset: str
    username: Optional[str] = None
    page: Optional[str] = None
    drawer_content: Optional[Any] = None
    pin_refs: Optional[Any] = None

@app.post("/builder", response_class=HTMLResponse)
def builder(req: BuilderRequest):
    html = arduino_block_coder(
        preset=req.preset,
        username=req.username,
        page=req.page,
        drawer_content=req.drawer_content,
        pin_refs=req.pin_refs,
        return_html=True,
        is_overlay=True,
    )
    return html

@app.get("/builder", response_class=HTMLResponse)
def builder_get(preset: Optional[str] = None, username: Optional[str] = None, page: Optional[str] = None):
    html = arduino_block_coder(
        preset=preset,
        username=username,
        page=page,
        return_html=True,
        is_overlay=True,
    )
    return html

@app.get("/")
def root():
    return {"message": "Arduino Builder Service is active"}

@app.get("/health")
def health():
    return {"status": "ok"}