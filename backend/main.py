from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

from backend.utils.route_parser import RouteParser
from config import Config


app = FastAPI()

# Enable CORS (for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tfl_key = Config.TFL_KEY
tfl_url = Config.TFL_URL
# NATIONAL_RAIL_API_URL = "https://api.nationalrail.co.uk/fares"

@app.get("/")
def home():
    return {"message": "Ticket Optimizer API"}

@app.get("/find-best-fare/")
def find_best_fare(from_station: str, to_station: str, railcard: bool = False):
    return RouteParser.find_optimum_fare(from_station, to_station, "1630", railcard)

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

