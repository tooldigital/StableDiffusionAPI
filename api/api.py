import tool_methods
import random
from PIL import Image, ImageOps
from auth_token import auth_token
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from torch import autocast
from io import BytesIO
import base64 


app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
def generate(prompt: str, negative_prompt: str, steps: int,seed: int, guidance: float, scheduler: str,selected_model: str):
    if seed == 0:
       seed = random.randint(0, 2147483647) 

    print(seed)
    with autocast("cuda"): 
        images = tool_methods.getImageForPrompt(prompt,negative_prompt,512,512,steps,guidance,seed,scheduler,1,selected_model)
    images[0].save("testimage.png")
    buffer = BytesIO()
    images[0].save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())
    seed = 0

    return Response(content=imgstr, media_type="image/png")