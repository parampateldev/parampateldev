from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class IoTEdgePlatform:
    def __init__(self):
        self.devices = []
        self.generate_devices()

    def generate_devices(self):
        device_types = ["Sensor", "Actuator", "Gateway", "Camera", "Thermostat"]
        for i in range(20):
            device = {
                "id": f"DEVICE_{i:03d}",
                "name": f"Smart {random.choice(device_types)} {i}",
                "type": random.choice(device_types),
                "status": random.choice(["Online", "Offline", "Maintenance"]),
                "location": f"Building {random.randint(1, 10)} Floor {random.randint(1, 5)}",
                "last_seen": datetime.now().isoformat(),
                "data_points": random.randint(100, 10000),
                "battery_level": random.randint(10, 100),
                "temperature": round(random.uniform(15, 35), 1),
                "humidity": round(random.uniform(30, 80), 1)
            }
            self.devices.append(device)

    def get_devices(self):
        return self.devices

    def get_analytics(self):
        return {
            "total_devices": len(self.devices),
            "online_devices": len([d for d in self.devices if d["status"] == "Online"]),
            "offline_devices": len([d for d in self.devices if d["status"] == "Offline"]),
            "maintenance_devices": len([d for d in self.devices if d["status"] == "Maintenance"]),
            "avg_temperature": round(sum(d["temperature"] for d in self.devices) / len(self.devices), 1),
            "avg_humidity": round(sum(d["humidity"] for d in self.devices) / len(self.devices), 1),
            "total_data_points": sum(d["data_points"] for d in self.devices)
        }

iot_platform = IoTEdgePlatform()

@app.route("/")
def root():
    return jsonify({
        "message": "🌐 IoT Edge Computing Platform - Smart device management",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Device management",
            "Real-time monitoring",
            "Edge analytics",
            "Predictive maintenance"
        ]
    })

@app.route("/api/devices")
def get_devices():
    devices = iot_platform.get_devices()
    return jsonify({"success": True, "devices": devices})

@app.route("/api/analytics")
def get_analytics():
    analytics = iot_platform.get_analytics()
    return jsonify({"success": True, "analytics": analytics})

if __name__ == "__main__":
    print("🌐 IoT Edge Computing Platform Starting...")
    print("💡 Smart device management platform")
    print("🌐 API running on http://localhost:8006")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/iot-edge-platform/frontend/index.html")
    print("🔗 Ready for IoT device management!")
    app.run(debug=True, host="0.0.0.0", port=8006)

