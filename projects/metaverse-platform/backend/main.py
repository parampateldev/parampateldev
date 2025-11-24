from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

class MetaversePlatform:
    def __init__(self):
        self.virtual_worlds = ["Virtual City", "Space Station", "Fantasy Realm", "Digital Office"]
        self.avatars = []
        self.generate_avatars()

    def generate_avatars(self):
        for i in range(15):
            avatar = {
                "id": f"AVATAR_{i:03d}",
                "name": f"Player_{i+1}",
                "world": random.choice(self.virtual_worlds),
                "level": random.randint(1, 100),
                "experience": random.randint(100, 10000),
                "currency": random.randint(100, 50000),
                "status": random.choice(["Online", "Offline", "Away"]),
                "last_active": datetime.now().isoformat(),
                "achievements": random.randint(0, 25)
            }
            self.avatars.append(avatar)

    def get_world_analytics(self):
        return {
            "total_avatars": len(self.avatars),
            "online_users": len([a for a in self.avatars if a["status"] == "Online"]),
            "worlds_active": len(self.virtual_worlds),
            "total_currency": sum(a["currency"] for a in self.avatars),
            "average_level": round(sum(a["level"] for a in self.avatars) / len(self.avatars), 1),
            "engagement_score": round(random.uniform(75, 95), 1)
        }

metaverse_platform = MetaversePlatform()

@app.route("/")
def root():
    return jsonify({
        "message": "🌐 Metaverse Platform - Virtual world experience platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Virtual world creation",
            "Avatar management",
            "Social interactions",
            "Digital economy"
        ]
    })

@app.route("/api/avatars")
def get_avatars():
    avatars = metaverse_platform.avatars
    return jsonify({"success": True, "avatars": avatars})

@app.route("/api/analytics")
def get_analytics():
    analytics = metaverse_platform.get_world_analytics()
    return jsonify({"success": True, "analytics": analytics})

if __name__ == "__main__":
    print("🌐 Metaverse Platform Starting...")
    print("💡 Virtual world experience platform")
    print("🌐 API running on http://localhost:8012")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/metaverse-platform/frontend/index.html")
    print("🎮 Ready for virtual experiences!")
    app.run(debug=True, host="0.0.0.0", port=8012)
