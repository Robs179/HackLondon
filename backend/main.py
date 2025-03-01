from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from config import Config
# Updated import from utils package:
from utils.route_parser import RouteParser as rp

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
NATIONAL_RAIL_API_URL = "https://api.nationalrail.co.uk/fares"

@app.get("/")
def home():
    return {"message": "Ticket Optimizer API"}

@app.get("/get-fares-tfl/")
def get_fares_tfl(from_station: str, to_station: str):
    return rp.route_finder(from_station, to_station)

@app.get("/get-fares/")
def get_fares(from_station: str, to_station: str):
    # Call TfL API
    tfl_response = requests.get(f"{tfl_url}/{from_station}/to/{to_station}")
    
    # Call BR Fares API
    national_rail_response = requests.get(f"{NATIONAL_RAIL_API_URL}?from={from_station}&to={to_station}")

    return {
        "tfl_fares": tfl_response.json(),
        "national_rail_fares": national_rail_response.json()
    }

# Run with: uvicorn main:app --reload
