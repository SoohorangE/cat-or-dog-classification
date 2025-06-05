from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

import base64
import io
from PIL import Image

class ImageRequest(BaseModel):
    image: str  # base64 string

from generator import Generator

# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="front")
app.mount("/front", StaticFiles(directory="front"), name="front")

# 모델 초기화
generator = Generator()

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(req: ImageRequest):
    image_data = base64.b64decode(req.image)
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    base64_result = generator.generate(image)
    return {"image": base64_result}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)



