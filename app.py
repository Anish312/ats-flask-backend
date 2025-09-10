from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import nltk

# Ensure required corpora are available
for package in ["punkt", "averaged_perceptron_tagger", "wordnet"]:
    try:
        nltk.data.find(f"tokenizers/{package}" if package == "punkt" else f"taggers/{package}" if package == "averaged_perceptron_tagger" else f"corpora/{package}")
    except LookupError:
        nltk.download(package)

app = FastAPI()

class JobDesc(BaseModel):
    text: str

@app.post("/extract-skills")
def extract_skills(data: JobDesc):
    job_text = data.text
    skills = []
    for skill in ["React.js", "Node.js", "Docker", "AWS", "Kubernetes"]:
        if skill.lower() in job_text.lower():
            skills.append(skill)
    return {"skills": skills}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
