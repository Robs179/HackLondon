from flask import Flask, render_template, request, jsonify

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

if __name__ == "__main__":
    app.run(debug=True)
