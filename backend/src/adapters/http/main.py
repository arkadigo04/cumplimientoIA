from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_salud():
    return {"status": "ok"}