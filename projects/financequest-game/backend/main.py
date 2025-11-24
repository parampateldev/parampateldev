from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
from datetime import datetime, timedelta
import math

app = Flask(__name__)
CORS(app)

class FinanceQuestGame:
    def __init__(self):
        self.players = {}
        self.quests = self._initialize_quests()
        self.market_data = self._initialize_market()
        self.achievements = self._initialize_achievements()
        
    def _initialize_quests(self):
        return {
            "savings_kingdom": [
                {
                    "id": "emergency_fund_quest",
                    "name": "Build Your Emergency Castle",
                    "description": "Save $1000 to build your first emergency fund castle!",
                    "difficulty": "Beginner",
                    "reward": {"coins": 500, "xp": 100, "knowledge": "Emergency Fund Basics"},
                    "requirement": {"savings": 1000},
                    "completed": False
                },
                {
                    "id": "budget_master_quest",
                    "name": "Master the Budget Scroll",
                    "description": "Create a balanced budget with 50/30/20 rule",
                    "difficulty": "Beginner", 
                    "reward": {"coins": 300, "xp": 75, "knowledge": "Budgeting Principles"},
                    "requirement": {"budget_balance": 0.8},
                    "completed": False
                }
            ],
            "investment_valley": [
                {
                    "id": "first_investment",
                    "name": "Your First Stock Adventure",
                    "description": "Buy your first stock and learn about market basics",
                    "difficulty": "Intermediate",
                    "reward": {"coins": 800, "xp": 150, "knowledge": "Stock Market Basics"},
                    "requirement": {"stocks_owned": 1},
                    "completed": False
                },
                {
                    "id": "portfolio_diversity",
                    "name": "Diversify Your Treasure",
                    "description": "Build a diversified portfolio with 3 different assets",
                    "difficulty": "Intermediate",
                    "reward": {"coins": 1200, "xp": 200, "knowledge": "Portfolio Diversification"},
                    "requirement": {"portfolio_diversity": 3},
                    "completed": False
                }
            ],
            "debt_dungeon": [
                {
                    "id": "credit_card_dragon",
                    "name": "Slay the Credit Card Dragon",
                    "description": "Pay off $500 in credit card debt",
                    "difficulty": "Intermediate",
                    "reward": {"coins": 1000, "xp": 180, "knowledge": "Debt Management"},
                    "requirement": {"debt_reduced": 500},
                    "completed": False
                }
            ]
        }
    
    def _initialize_market(self):
        return {
            "stocks": [
                {"symbol": "AAPL", "name": "Apple Inc.", "price": 175.50, "change": 2.30},
                {"symbol": "GOOGL", "name": "Google", "price": 2850.75, "change": -15.25},
                {"symbol": "MSFT", "name": "Microsoft", "price": 340.20, "change": 5.80},
                {"symbol": "TSLA", "name": "Tesla", "price": 245.90, "change": -8.40},
                {"symbol": "NVDA", "name": "NVIDIA", "price": 420.15, "change": 12.60}
            ],
            "crypto": [
                {"symbol": "BTC", "name": "Bitcoin", "price": 43250.00, "change": 1250.00},
                {"symbol": "ETH", "name": "Ethereum", "price": 2650.50, "change": -85.25}
            ],
            "bonds": [
                {"symbol": "US10Y", "name": "10-Year Treasury", "price": 98.50, "yield": 4.25},
                {"symbol": "US30Y", "name": "30-Year Treasury", "price": 95.20, "yield": 4.50}
            ]
        }
    
    def _initialize_achievements(self):
        return [
            {"id": "first_save", "name": "First Saver", "description": "Save your first $100", "reward": 100},
            {"id": "emergency_hero", "name": "Emergency Fund Hero", "description": "Build a 6-month emergency fund", "reward": 500},
            {"id": "investment_novice", "name": "Investment Novice", "description": "Make your first investment", "reward": 300},
            {"id": "portfolio_master", "name": "Portfolio Master", "description": "Build a diversified portfolio", "reward": 800},
            {"id": "debt_free", "name": "Debt Free Champion", "description": "Eliminate all debt", "reward": 1000}
        ]
    
    def create_player(self, name, class_type="Financial Novice"):
        player_id = f"player_{len(self.players) + 1}"
        self.players[player_id] = {
            "id": player_id,
            "name": name,
            "class": class_type,
            "level": 1,
            "xp": 0,
            "coins": 1000,
            "savings": 0,
            "investments": {},
            "debt": 2000,  # Start with some debt to manage
            "portfolio_value": 0,
            "knowledge_points": 0,
            "completed_quests": [],
            "achievements": [],
            "current_realm": "savings_kingdom",
            "created_at": datetime.now().isoformat(),
            "stats": {
                "financial_literacy": 10,
                "risk_tolerance": 5,
                "investment_skill": 5,
                "saving_habit": 5
            }
        }
        return self.players[player_id]
    
    def get_player(self, player_id):
        return self.players.get(player_id)
    
    def update_market(self):
        # Simulate market movements
        for stock in self.market_data["stocks"]:
            change_percent = random.uniform(-0.05, 0.05)
            stock["change"] = stock["price"] * change_percent
            stock["price"] = max(1, stock["price"] + stock["change"])
        
        for crypto in self.market_data["crypto"]:
            change_percent = random.uniform(-0.08, 0.08)
            crypto["change"] = crypto["price"] * change_percent
            crypto["price"] = max(1, crypto["price"] + crypto["change"])
    
    def buy_investment(self, player_id, asset_type, symbol, quantity):
        player = self.get_player(player_id)
        if not player:
            return {"success": False, "error": "Player not found"}
        
        # Find the asset
        asset = None
        if asset_type == "stock":
            asset = next((s for s in self.market_data["stocks"] if s["symbol"] == symbol), None)
        elif asset_type == "crypto":
            asset = next((c for c in self.market_data["crypto"] if c["symbol"] == symbol), None)
        
        if not asset:
            return {"success": False, "error": "Asset not found"}
        
        total_cost = asset["price"] * quantity
        
        if player["coins"] < total_cost:
            return {"success": False, "error": "Insufficient coins"}
        
        # Execute purchase
        player["coins"] -= total_cost
        
        if symbol not in player["investments"]:
            player["investments"][symbol] = {"quantity": 0, "avg_price": 0}
        
        # Update average price
        old_quantity = player["investments"][symbol]["quantity"]
        old_avg_price = player["investments"][symbol]["avg_price"]
        
        new_quantity = old_quantity + quantity
        new_avg_price = ((old_quantity * old_avg_price) + total_cost) / new_quantity
        
        player["investments"][symbol]["quantity"] = new_quantity
        player["investments"][symbol]["avg_price"] = new_avg_price
        
        # Update portfolio value
        self._update_portfolio_value(player)
        
        return {
            "success": True,
            "message": f"Successfully bought {quantity} {symbol} for {total_cost:.2f} coins",
            "transaction": {
                "asset": symbol,
                "quantity": quantity,
                "price": asset["price"],
                "total_cost": total_cost
            }
        }
    
    def _update_portfolio_value(self, player):
        total_value = 0
        for symbol, investment in player["investments"].items():
            # Find current price
            current_price = 0
            for stock in self.market_data["stocks"]:
                if stock["symbol"] == symbol:
                    current_price = stock["price"]
                    break
            for crypto in self.market_data["crypto"]:
                if crypto["symbol"] == symbol:
                    current_price = crypto["price"]
                    break
            
            total_value += investment["quantity"] * current_price
        
        player["portfolio_value"] = total_value
    
    def complete_quest(self, player_id, quest_id):
        player = self.get_player(player_id)
        if not player:
            return {"success": False, "error": "Player not found"}
        
        # Find the quest
        quest = None
        for realm_quests in self.quests.values():
            for q in realm_quests:
                if q["id"] == quest_id:
                    quest = q
                    break
        
        if not quest:
            return {"success": False, "error": "Quest not found"}
        
        if quest_id in player["completed_quests"]:
            return {"success": False, "error": "Quest already completed"}
        
        # Check if player meets requirements
        if self._check_quest_requirements(player, quest):
            # Complete quest
            player["completed_quests"].append(quest_id)
            player["coins"] += quest["reward"]["coins"]
            player["xp"] += quest["reward"]["xp"]
            player["knowledge_points"] += 50
            
            # Level up check
            new_level = (player["xp"] // 200) + 1
            if new_level > player["level"]:
                player["level"] = new_level
                level_bonus = new_level * 100
                player["coins"] += level_bonus
            
            quest["completed"] = True
            
            return {
                "success": True,
                "message": f"Quest '{quest['name']}' completed!",
                "rewards": quest["reward"],
                "level_up": new_level > player["level"]
            }
        
        return {"success": False, "error": "Quest requirements not met"}
    
    def _check_quest_requirements(self, player, quest):
        requirements = quest["requirement"]
        
        for req_key, req_value in requirements.items():
            if req_key == "savings" and player["savings"] < req_value:
                return False
            elif req_key == "stocks_owned" and len([k for k in player["investments"].keys()]) < req_value:
                return False
            elif req_key == "debt_reduced" and player["debt"] > (2000 - req_value):
                return False
        
        return True
    
    def get_leaderboard(self):
        players_list = list(self.players.values())
        players_list.sort(key=lambda x: x["xp"], reverse=True)
        return players_list[:10]
    
    def get_game_stats(self):
        total_players = len(self.players)
        total_quests_completed = sum(len(p["completed_quests"]) for p in self.players.values())
        total_coins_in_circulation = sum(p["coins"] for p in self.players.values())
        
        return {
            "total_players": total_players,
            "total_quests_completed": total_quests_completed,
            "total_coins_in_circulation": total_coins_in_circulation,
            "average_level": sum(p["level"] for p in self.players.values()) / max(total_players, 1),
            "active_realms": len(self.quests)
        }

# Initialize game
finance_quest = FinanceQuestGame()

@app.route("/")
def root():
    return jsonify({
        "message": "🎮 FinanceQuest - The Ultimate Finance Learning Adventure",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "RPG-style finance learning",
            "Interactive quest system",
            "Real market simulation",
            "Achievement system",
            "Multiplayer leaderboards"
        ]
    })

@app.route("/api/create-player", methods=["POST"])
def create_player():
    data = request.json
    name = data.get("name", "Anonymous Player")
    class_type = data.get("class", "Financial Novice")
    
    player = finance_quest.create_player(name, class_type)
    return jsonify({"success": True, "player": player})

@app.route("/api/player/<player_id>")
def get_player(player_id):
    player = finance_quest.get_player(player_id)
    if player:
        return jsonify({"success": True, "player": player})
    return jsonify({"success": False, "error": "Player not found"})

@app.route("/api/market")
def get_market():
    finance_quest.update_market()
    return jsonify({"success": True, "market": finance_quest.market_data})

@app.route("/api/buy", methods=["POST"])
def buy_investment():
    data = request.json
    player_id = data.get("player_id")
    asset_type = data.get("asset_type")
    symbol = data.get("symbol")
    quantity = data.get("quantity", 1)
    
    result = finance_quest.buy_investment(player_id, asset_type, symbol, quantity)
    return jsonify(result)

@app.route("/api/quests")
def get_quests():
    return jsonify({"success": True, "quests": finance_quest.quests})

@app.route("/api/complete-quest", methods=["POST"])
def complete_quest():
    data = request.json
    player_id = data.get("player_id")
    quest_id = data.get("quest_id")
    
    result = finance_quest.complete_quest(player_id, quest_id)
    return jsonify(result)

@app.route("/api/leaderboard")
def get_leaderboard():
    leaderboard = finance_quest.get_leaderboard()
    return jsonify({"success": True, "leaderboard": leaderboard})

@app.route("/api/game-stats")
def get_game_stats():
    stats = finance_quest.get_game_stats()
    return jsonify({"success": True, "stats": stats})

@app.route("/api/achievements")
def get_achievements():
    return jsonify({"success": True, "achievements": finance_quest.achievements})

if __name__ == "__main__":
    print("🎮 FinanceQuest Game Starting...")
    print("💡 The Ultimate Finance Learning Adventure")
    print("🌐 API running on http://localhost:8013")
    print("🎮 Frontend available at: file:///Users/parampatel/parampatel-dev/financequest-game/frontend/index.html")
    print("🚀 Ready for epic finance adventures!")
    app.run(debug=True, host="0.0.0.0", port=8013)

