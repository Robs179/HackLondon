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
# NATIONAL_RAIL_API_URL = "https://api.nationalrail.co.uk/fares"

@app.get("/")
def home():
    return {"message": "Ticket Optimizer API"}

@app.get("/get-fares-tfl/")
def get_fares_tfl(from_station: str, to_station: str):
    tdl_dict = rp.getTfLDict(from_station, to_station, 1630, True, True)
    # tdl_dict = rp.getTfLDict("910GBONDST", "910GGTWK", 1630, True, True)
    return {
        "tfl_fares": tdl_dict[0]}

@app.get("/get-fares/")
def get_fares(from_station: str, to_station: str):
    # Call TfL API
    tfl_response = requests.get(f"{tfl_url}/{from_station}/to/{to_station}")

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
