from fastapi import FastAPI
from config import Config

app = FastAPI()

# Access the API key
api_key = Config.API_KEY

@app.get("/")
def read_root():
    return {"API_KEY": api_key}