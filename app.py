from flask import Flask, render_template, request, jsonify
import googlemaps
import requests

app = Flask(__name__)

# API Keys
GOOGLE_MAPS_API_KEY = "AIzaSyBKGNjFdSudXigNkFhL1BLX7EqZPEaOSYw"

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_traffic_data(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}&departure_time=now&traffic_model=best_guess&alternatives=true"
    response = requests.get(url)
    data = response.json()

    if "routes" in data and data["routes"]:
        traffic_info = data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
        return {"traffic_status": traffic_info}
    return {"error": "No traffic data available"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/traffic", methods=["GET"])
def traffic():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    return jsonify(get_traffic_data(origin, destination))

if __name__ == "__main__":
    app.run(debug=True)



