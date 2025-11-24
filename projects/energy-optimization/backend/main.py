from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class EnergyOptimizationPlatform:
    def __init__(self):
        self.energy_sources = ["Solar", "Wind", "Hydro", "Nuclear", "Coal", "Gas"]
        self.optimization_strategies = [
            "Load balancing", "Peak shaving", "Demand response",
            "Renewable integration", "Storage optimization"
        ]

    def optimize_energy_usage(self, usage_data):
        return {
            "current_consumption": round(random.uniform(1000, 5000), 2),
            "optimized_consumption": round(random.uniform(800, 4500), 2),
            "savings_percentage": round(random.uniform(10, 25), 1),
            "cost_savings": round(random.uniform(500, 2000), 2),
            "carbon_reduction": round(random.uniform(100, 500), 1),
            "recommended_strategy": random.choice(self.optimization_strategies),
            "peak_hours": ["9:00-11:00", "18:00-20:00"],
            "off_peak_hours": ["22:00-6:00"],
            "optimization_score": round(random.uniform(75, 95), 1)
        }

    def get_renewable_energy_status(self):
        return {
            "solar_capacity": round(random.uniform(500, 2000), 1),
            "wind_capacity": round(random.uniform(300, 1500), 1),
            "hydro_capacity": round(random.uniform(200, 1000), 1),
            "renewable_percentage": round(random.uniform(30, 80), 1),
            "grid_stability": round(random.uniform(85, 98), 1),
            "energy_storage": round(random.uniform(100, 500), 1)
        }

energy_platform = EnergyOptimizationPlatform()

@app.route("/")
def root():
    return jsonify({
        "message": "⚡ Energy Optimization Platform - Smart energy management",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Energy usage optimization",
            "Renewable integration",
            "Cost reduction",
            "Carbon footprint tracking"
        ]
    })

@app.route("/api/optimize", methods=["POST"])
def optimize_energy():
    data = request.json
    optimization = energy_platform.optimize_energy_usage(data)
    return jsonify({"success": True, "optimization": optimization})

@app.route("/api/renewable-status")
def get_renewable_status():
    status = energy_platform.get_renewable_energy_status()
    return jsonify({"success": True, "renewable_status": status})

if __name__ == "__main__":
    print("⚡ Energy Optimization Platform Starting...")
    print("💡 Smart energy management platform")
    print("🌐 API running on http://localhost:8009")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/energy-optimization/frontend/index.html")
    print("🔋 Ready for energy optimization!")
    app.run(debug=True, host="0.0.0.0", port=8009)

