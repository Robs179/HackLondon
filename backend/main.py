from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import json
import pandas as pd
import os
import sys
from config import Config
import re

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.utils.route_parser import RouteParser
from backend.utils.tfl_fare_calculator import TfLFareManager

# Print current directory to understand where Python is looking
# print(f"Current directory: {os.getcwd()}")

# # Get the absolute path to the backend directory
# backend_dir = os.path.abspath(os.path.dirname(__file__))
# print(f"Backend directory: {backend_dir}")

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
    list_of_dicts = RouteParser.find_optimum_fare(from_station, to_station, "0900", railcard)
    tfl_fares = {}
    nr_fares = {}
    for i in list_of_dicts:
         if i["is_nr"] == False:
             tfl_fares = i
             i["origin_code"] = re.sub(r'%20', ' ', RouteParser.tfl_code_to_name(i["origin_code"]))
             i["destination_code"] = re.sub(r'%20', ' ',RouteParser.tfl_code_to_name(i["destination_code"]))
         else:
             i["origin_code"] = re.sub(r'%20', ' ',i["origin_code"])
             i["destination_code"] = re.sub(r'%20', ' ',i["destination_code"])
             nr_fares = i

    return JSONResponse(content={"tfl": tfl_fares, "nr": nr_fares})


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

