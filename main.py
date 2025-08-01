from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def start_root():
    return {"message": "Welcome to the Vulnability tracker"}
