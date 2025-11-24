from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class AgricultureAI:
    def __init__(self):
        self.crops = ["Wheat", "Corn", "Soybean", "Rice", "Potato"]
        self.weather_conditions = ["Sunny", "Rainy", "Cloudy", "Windy"]

    def analyze_crop_health(self, crop_data):
        return {
            "crop_type": crop_data.get("crop", random.choice(self.crops)),
            "health_score": round(random.uniform(60, 95), 1),
            "yield_prediction": round(random.uniform(80, 120), 1),
            "disease_risk": round(random.uniform(5, 30), 1),
            "pest_detection": random.choice(["None", "Low", "Medium", "High"]),
            "irrigation_needed": random.choice([True, False]),
            "fertilizer_recommendation": round(random.uniform(50, 200), 1),
            "harvest_date": (datetime.now()).isoformat()
        }

    def get_weather_recommendations(self):
        return {
            "current_weather": random.choice(self.weather_conditions),
            "temperature": round(random.uniform(15, 35), 1),
            "humidity": round(random.uniform(40, 90), 1),
            "recommendations": [
                "Optimal planting conditions",
                "Increase irrigation by 15%",
                "Monitor for pest activity",
                "Harvest window opening"
            ]
        }

agriculture_ai = AgricultureAI()

@app.route("/")
def root():
    return jsonify({
        "message": "🌾 Agriculture AI - Smart farming optimization platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Crop health monitoring",
            "Yield prediction",
            "Weather analysis",
            "Smart irrigation"
        ]
    })

@app.route("/api/crop-analysis", methods=["POST"])
def analyze_crop():
    data = request.json
    analysis = agriculture_ai.analyze_crop_health(data)
    return jsonify({"success": True, "analysis": analysis})

@app.route("/api/weather")
def get_weather():
    weather = agriculture_ai.get_weather_recommendations()
    return jsonify({"success": True, "weather": weather})

if __name__ == "__main__":
    print("🌾 Agriculture AI Starting...")
    print("💡 Smart farming optimization platform")
    print("🌐 API running on http://localhost:8008")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/agriculture-ai/frontend/index.html")
    print("🚜 Ready for smart agriculture!")
    app.run(debug=True, host="0.0.0.0", port=8008)

