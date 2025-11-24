from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class SpaceExplorationPlatform:
    def __init__(self):
        self.missions = ["Mars Rover", "Satellite Deployment", "Space Station", "Asteroid Mining"]
        self.planets = ["Mars", "Jupiter", "Saturn", "Venus", "Mercury"]

    def get_mission_status(self):
        missions = []
        for i in range(5):
            mission = {
                "id": f"MISSION_{i:03d}",
                "name": f"Space Mission {i+1}",
                "type": random.choice(self.missions),
                "target": random.choice(self.planets),
                "status": random.choice(["Planning", "Active", "Completed", "Delayed"]),
                "progress": round(random.uniform(0, 100), 1),
                "crew_size": random.randint(2, 8),
                "duration_days": random.randint(30, 365),
                "budget": round(random.uniform(1000000, 10000000), 2),
                "launch_date": datetime.now().isoformat()
            }
            missions.append(mission)
        return missions

    def analyze_space_data(self, data_type):
        return {
            "data_type": data_type,
            "samples_collected": random.randint(100, 10000),
            "analysis_accuracy": round(random.uniform(85, 99), 1),
            "discoveries": random.randint(0, 5),
            "anomalies_detected": random.randint(0, 3),
            "recommended_actions": [
                "Continue current trajectory",
                "Adjust orbit parameters",
                "Collect additional samples",
                "Monitor for changes"
            ]
        }

space_platform = SpaceExplorationPlatform()

@app.route("/")
def root():
    return jsonify({
        "message": "🚀 Space Exploration Platform - Advanced space mission management",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Mission planning",
            "Space data analysis",
            "Satellite tracking",
            "Planetary exploration"
        ]
    })

@app.route("/api/missions")
def get_missions():
    missions = space_platform.get_mission_status()
    return jsonify({"success": True, "missions": missions})

@app.route("/api/analyze-space-data", methods=["POST"])
def analyze_space_data():
    data = request.json
    data_type = data.get("data_type", "Planetary Surface")
    analysis = space_platform.analyze_space_data(data_type)
    return jsonify({"success": True, "analysis": analysis})

if __name__ == "__main__":
    print("🚀 Space Exploration Platform Starting...")
    print("💡 Advanced space mission management")
    print("🌐 API running on http://localhost:8011")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/space-exploration/frontend/index.html")
    print("🌌 Ready for space exploration!")
    app.run(debug=True, host="0.0.0.0", port=8011)

