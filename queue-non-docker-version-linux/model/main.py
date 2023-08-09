import tool_methods
import random
from PIL import Image, ImageOps
import redis
import os
import json
import time
import base64
from io import BytesIO

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
db = redis.Redis(connection_pool=pool)
db.ping() 
print("MODEL STARTED")

def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1

def generateSD():
   # Continually poll for new images to classify
    while True:

      
        # Pop off multiple images from Redis queue atomically
        with db.pipeline() as pipe:
            pipe.lrange("sd_queue", 0, 0)
            pipe.ltrim("sd_queue", 1, -1)
            queue, _ = pipe.execute()

        imageIDs = []
        sd_objects = []
        for q in queue:
            # Deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            obj = {"prompt": q['prompt'],"negative_prompt":q['negative_prompt'],"steps":q['steps'],"seed":q['seed'],"guidance":q['guidance'],"scheduler":q['scheduler'],"selected_model":q['selected_model'],"amount":q['amount']}
            sd_objects.append(obj)
            # Update the list of image IDs
            imageIDs.append(q["id"])

        # Check to see if we need to process the batch
        if len(imageIDs) > 0:
            # Classify the batch
            # Loop over the image IDs and their corresponding set of results from our model
            for id in imageIDs:
                # Initialize the list of output predictions
                # Store the output predictions in the database, using image ID as the key so we can fetch the results
                
                images = tool_methods.getImageForPrompt(sd_objects[0]['prompt'],sd_objects[0]['negative_prompt'],512,512,sd_objects[0]['steps'],sd_objects[0]['guidance'],0,sd_objects[0]['scheduler'],sd_objects[0]['amount'],sd_objects[0]['selected_model'])
                
                base64strings = []
                imagstrings = ""
                for n in range(len(images)):
                    image = images[n]
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    imgstr = base64.b64encode(buffer.getvalue())
                    base64strings.append(imgstr)
                    imagstrings = imagstrings+"data:image/png;base64,"+imgstr.decode()+"*****!!!!!*****"
                db.set(id, imagstrings)
              
                time.sleep(0.1)
        # Sleep for a small amount
        time.sleep(0.05)

if __name__ == "__main__":
    generateSD()