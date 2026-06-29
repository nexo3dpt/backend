from fastapi import FastAPI, Request
import uuid
import os
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    job_id = str(uuid.uuid4())

    try:
        photo_url = data["line_items"][0]["properties"]["Foto do Pet"]
    except:
        photo_url = None

    if photo_url:
        os.makedirs(f"jobs/{job_id}", exist_ok=True)
        img = requests.get(photo_url).content

        with open(f"jobs/{job_id}/pet.png", "wb") as f:
            f.write(img)

    print("JOB CRIADO:", job_id)

    return {"status": "ok", "job_id": job_id}
