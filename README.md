
# Stable Diffusion API

This project runs a Stable Diffusion backend and frontend to communicate with.

![Screenshot](https://raw.githubusercontent.com/tooldigital/StableDiffusionAPI/main/readme/house.png)

Kudos https://github.com/nicknochnack 🙌

## Run Locally

Windows PC with Nvidia GPU with 8Gb of RAM or more

Install Miniconda (Windows) - Make sure Conda is in your system path
```bash
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
```
Make sure Miniconda is added to the PATH environment variable
![anaconda_install](https://raw.githubusercontent.com/tooldigital/StableDiffusionAPI/main/readme/conda.png)

Clone the project
```bash
git clone https://github.com/tooldigital/StableDiffusionAPI
```

☕ Create Python environment (this can take a while) or double click `init_api.bat`☕
```bash
cd StableDiffusionAPI/api
conda env create --file environment.yml
```

Start api or double click `start_api.bat`
```bash
cd StableDiffusionAPI/api
conda activate tool
uvicorn api:app --reload
```

Start frontend or double click `start_client.bat`
```bash
cd StableDiffusionAPI/client
npm i
npm start
```

## ENDPOINTS

### API

API is running at http://localhost:8000

Documentation is at http://localhost:8000/docs

### FRONTEND

Frontend is running at http://localhost:3000

## API reference

#### Generate image

```http
  GET /
```

| Parameter | Type     |    
| :-------- | :------- | 
| `prompt`  | `string` | 
| `negavtive_prompt`  | `string` | 
| `steps`  | `integer` | 
| `seed`  | `integer` | 
| `guidance`  | `float` |
| `scheduler`  | `string` |
| `selected_model `  | `string` | 


http://localhost:8000/?prompt=little%20house%20on%20the%20prairie&negative_prompt=ugly&steps=50&seed=0&guidance=7.5&scheduler=DPMSolverMultistepScheduler&selected_model=runwayml%2Fstable-diffusion-v1-5
