from flask import Flask, render_template, request, jsonify
from config import Config
from utils.route_parser import RouteParser as rp

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/greet", methods=["GET"])
def greet():
    return jsonify({"message": "Hello, Hackathon Team!"})

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name", "Guest")
    return jsonify({"message": f"Hello, {name}!"})

@app.route("/api/fares-tfl", methods=["GET"])
def fares_tfl():
    from_station = request.args.get("from_station")
    to_station = request.args.get("to_station")
    railcard_param = request.args.get("railcard", "false").lower()
    railcard = railcard_param in ["true", "1", "yes"]
    
    # Use fixed time (e.g. 1630) and a flag (True) similar to your FastAPI example
    fares = rp.getTfLDict(from_station, to_station, 1630, railcard, True)
    return jsonify({
        "tfl_fares": fares[0],
        "national_rail_fares": fares[1]
    })

if __name__ == "__main__":
    app.run(debug=True)
