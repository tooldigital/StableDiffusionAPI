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
    return Response("Hello World from Tool! Try this http://localhost/generate?prompt=hello world&negative_prompt=hands&steps=25&seed=0&guidance=7.5&scheduler=PNDMScheduler&selected_model=runwayml/stable-diffusion-v1-5")

@app.get("/generate")
def generate(prompt: str, negative_prompt: str, steps: int,seed: int, guidance: float, scheduler: str,selected_model: str):
    #prompt: str, negative_prompt: str, steps: int,seed: int, guidance: float, scheduler: str,selected_model: str
    k = str(uuid.uuid4())
    print("started request with id: "+k)
    d = {"id": k, "prompt": prompt,"negative_prompt":negative_prompt,"steps":steps,"seed":seed,"guidance":guidance,"scheduler":scheduler,"selected_model":selected_model}
    db.rpush("sd_queue", json.dumps(d))
    data = {"success": False, "image":""}
    num_tries = 0
    imgdata = None
    while num_tries < 100:
        num_tries += 1
        output = db.get(k)
        # Check to see if our model has classified the input image
        if output is not None:

            #convert bytes to PIL image
            image = Image.open(BytesIO(output))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            imgstr = base64.b64encode(buffer.getvalue())
            imgdata = imgstr
            #images[0].save("testimage.png")
            #buffer = BytesIO(output)
            #images[0].save(buffer, format="PNG")
            #imgstr = base64.b64encode(buffer.getvalue())
            #imgdata = imgstr
            # Delete the result from the database and break from the polling loop
            data["success"] = True
            db.delete(k)
            break
        
        # Sleep for a small amount to give the model a chance to classify the input image
        tt = 0.6*15
        time.sleep(tt)

    return Response(content=imgdata, media_type="image/png")