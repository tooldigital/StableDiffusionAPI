from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
import uuid
import json
import time
import PIL.Image as Image
from io import BytesIO
import base64 

app = FastAPI()

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
db = redis.Redis(connection_pool=pool)

db.ping() 

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
def index():
    return Response("Hello World from Tool stable diffusion text to image!")

@app.get("/generate")
def generate(prompt: str, negative_prompt: str, steps: int,seed: int, guidance: float, scheduler: str,selected_model: str,amount: int):
    k = str(uuid.uuid4())
    print("started request with id: "+k)
    d = {"id": k, "prompt": prompt,"negative_prompt":negative_prompt,"steps":steps,"seed":seed,"guidance":guidance,"scheduler":scheduler,"selected_model":selected_model,"amount":amount}
    db.rpush("sd_queue", json.dumps(d))
    num_tries = 0
    imgdata = None
    while num_tries < 100:
        num_tries += 1
        output = db.get(k)
        # Check to see if our model has classified the input image
        if output is not None:
            myarr = output.split(b"*****!!!!!*****")
            newarr = []
            for el in myarr:
                el.decode("utf-8")
                newarr.append(el.decode("utf-8"))

            ele= newarr.pop()
            jsonob = json.dumps(newarr)
            imgdata = jsonob
            db.delete(k)
            break
        
        # Sleep for a small amount to give the model a chance to classify the input image
        tt = 0.6*15
        time.sleep(tt)

    return Response(content=imgdata, media_type="application/json")