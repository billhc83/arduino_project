import sys
import os
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'components'))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from arduino_blocks import arduino_block_coder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/builder", response_class=HTMLResponse)
def builder(
    preset: str,
    username: Optional[str] = None,
    page: Optional[str] = None,
):
    html = arduino_block_coder(
        preset=preset,
        username=username,
        page=page,
        return_html=True,
        is_overlay=True,
    )
    return html

@app.get("/health")
def health():
    return {"status": "ok"}