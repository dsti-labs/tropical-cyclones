from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("xgboost_tropical_cyclone.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_text = None  # Keep the last prediction on screen

    if request.method == "POST":
        try:
            # Get input values from form
            lat = request.form["lat"]
            lon = request.form["lon"]
            dist2land = request.form["dist2land"]
            storm_speed = request.form["storm_speed"]
            storm_dir = request.form["storm_dir"]
            month = request.form["month"]
            hour = request.form["hour"]

            # Debug prints for received input
            print("\nReceived Input Data:")
            print(f"LAT: {lat}, LON: {lon}, DIST2LAND: {dist2land}, STORM_SPEED: {storm_speed}, STORM_DIR: {storm_dir}, MONTH: {month}, HOUR: {hour}")

            # Convert input to float
            lat = float(lat)
            lon = float(lon)
            dist2land = float(dist2land)
            storm_speed = float(storm_speed)
            storm_dir = float(storm_dir)
            month = float(month)
            hour = float(hour)

            # Normalize DIST2LAND (ensure same scaling as used in training)
            dist2land_norm = dist2land / 3079.0  # Max value found during data analysis

            # Debug print for transformed input
            print(f"Transformed Input Data for Model: {[lat, lon, dist2land_norm, storm_speed, storm_dir, month, hour]}")

            # Make prediction
            input_features = np.array([[lat, lon, dist2land_norm, storm_speed, storm_dir, month, hour]])
            prediction = model.predict(input_features)[0]

            # Map prediction to severity labels
            severity_mapping = {
                0: "Tropical Depression",
                1: "Tropical Storm",
                2: "Category 1",
                3: "Category 2",
                4: "Category 3",
                5: "Category 4",
                6: "Category 5"
            }
            prediction_text = f"Predicted Severity: {severity_mapping.get(prediction, 'Unknown')}"
            print(f"Prediction Output: {prediction_text}")

        except ValueError as e:
            print(f"Error During Prediction: {e}")
            prediction_text = "Invalid input! Please enter valid numbers."

    return render_template("index.html", prediction=prediction_text)

if __name__ == "__main__":
    app.run(debug=True)


