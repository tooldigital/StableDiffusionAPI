import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'diffusers==0.13.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'transformers==4.26.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scipy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ftfy==6.1.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'accelerate==0.16.0'])


import tool_methods
import random
from PIL import Image, ImageOps


selected_model ="runwayml/stable-diffusion-v1-5"
#["PNDMScheduler","LMSDiscreteScheduler","DDIMScheduler","EulerDiscreteScheduler","EulerAncestralDiscreteScheduler","DPMSolverMultistepScheduler"]
scheduler = 'DPMSolverMultistepScheduler'
#prompt = "A photo of a person with paint makeup in rainbow colors, ultrarealistic, portrait, cinematic lighting, award winning photo, no color, 80mm lense \u2013beta \u2013upbeta \u2013upbeta" # @param {type:'string'}
#(high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3
prompt = "A photo of a man holding a fuel can, ultrarealistic, portrait, cinematic lighting, award winning photo"
negative_prompt = "text, ugly,duplicate, mutilated, out of frame,  mutation, blurry, bad anatomy, extra legs,low resolution,disfigured"
guidance = 7.5 
steps = 50 
seed = 0 
num_samples = 1 

if seed == 0:
  seed = random.randint(0, 2147483647)

images = tool_methods.getImageForPrompt(prompt,negative_prompt,512,512,steps,guidance,seed,scheduler,num_samples,selected_model)
widths, heights = zip(*(i.size for i in images))
total_width = sum(widths)
max_height = max(heights)
x_offset = 0
new_im = Image.new('RGB', (total_width, max_height))
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.show()