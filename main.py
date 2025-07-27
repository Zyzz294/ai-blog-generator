from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
import os 

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def generate_blog(topic:str, wordcount: int) -> str:
    prompt = f"""Write a detailed, SEO friendly blog post about: "{topic}".
    Please keep the response around {wordcount} words.
Include:
- A catchy Title 
- Introduction (80-100 words)
- 4-5 subheadings with explanations
- Conclusion
Use a friendly professional tone."""
    

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    return result.stdout.decode()


@app.get("/", response_class=HTMLResponse)

def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "blog": None})

@app.post("/", response_class=HTMLResponse)

def form_post(request: Request, topic: str = Form(...), wordcount: int = Form(...)):
    blog = generate_blog(topic, wordcount)

    return templates.TemplateResponse("index.html", {"request": request, "blog": blog})