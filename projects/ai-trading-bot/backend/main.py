from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import numpy as np
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

class AITradingBot:
    def __init__(self):
        self.portfolio = {
            "cash": 100000,
            "positions": {},
            "total_value": 100000
        }
        self.trade_history = []
        self.strategies = [
            "LSTM Neural Network",
            "Random Forest",
            "Support Vector Machine",
            "Moving Average Crossover",
            "RSI Mean Reversion"
        ]

    def generate_market_data(self, symbol="AAPL"):
        # Simulate realistic stock data
        base_price = random.uniform(100, 300)
        change = random.uniform(-0.05, 0.05)
        volume = random.randint(1000000, 10000000)
        
        return {
            "symbol": symbol,
            "price": round(base_price, 2),
            "change": round(change, 4),
            "change_percent": round(change * 100, 2),
            "volume": volume,
            "high": round(base_price * 1.02, 2),
            "low": round(base_price * 0.98, 2),
            "timestamp": datetime.now().isoformat()
        }

    def predict_price(self, symbol, strategy="LSTM Neural Network"):
        # Simulate ML prediction
        current_data = self.generate_market_data(symbol)
        prediction = current_data["price"] * random.uniform(0.95, 1.05)
        confidence = random.uniform(0.6, 0.95)
        
        return {
            "symbol": symbol,
            "current_price": current_data["price"],
            "predicted_price": round(prediction, 2),
            "confidence": round(confidence, 3),
            "strategy": strategy,
            "direction": "BUY" if prediction > current_data["price"] else "SELL",
            "timestamp": datetime.now().isoformat()
        }

    def backtest_strategy(self, symbol, strategy, days=30):
        # Simulate backtesting results
        initial_price = random.uniform(100, 200)
        final_price = initial_price * random.uniform(0.8, 1.3)
        
        trades = []
        for i in range(random.randint(5, 15)):
            trade_price = initial_price * random.uniform(0.9, 1.1)
            trades.append({
                "date": (datetime.now() - timedelta(days=random.randint(1, days))).isoformat(),
                "action": random.choice(["BUY", "SELL"]),
                "price": round(trade_price, 2),
                "quantity": random.randint(10, 100)
            })
        
        return_percent = ((final_price - initial_price) / initial_price) * 100
        
        return {
            "strategy": strategy,
            "symbol": symbol,
            "period_days": days,
            "initial_price": round(initial_price, 2),
            "final_price": round(final_price, 2),
            "return_percent": round(return_percent, 2),
            "total_trades": len(trades),
            "win_rate": round(random.uniform(0.4, 0.8), 2),
            "max_drawdown": round(random.uniform(-0.15, -0.05), 2),
            "trades": trades
        }

    def execute_trade(self, symbol, action, quantity, price):
        trade = {
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now().isoformat(),
            "status": "EXECUTED"
        }
        
        self.trade_history.append(trade)
        
        # Update portfolio
        if action == "BUY":
            cost = quantity * price
            if cost <= self.portfolio["cash"]:
                self.portfolio["cash"] -= cost
                if symbol in self.portfolio["positions"]:
                    self.portfolio["positions"][symbol] += quantity
                else:
                    self.portfolio["positions"][symbol] = quantity
                trade["status"] = "EXECUTED"
            else:
                trade["status"] = "FAILED - Insufficient funds"
        else:  # SELL
            if symbol in self.portfolio["positions"] and self.portfolio["positions"][symbol] >= quantity:
                self.portfolio["positions"][symbol] -= quantity
                self.portfolio["cash"] += quantity * price
                trade["status"] = "EXECUTED"
            else:
                trade["status"] = "FAILED - Insufficient shares"
        
        return trade

    def get_portfolio_status(self):
        # Calculate total portfolio value
        total_value = self.portfolio["cash"]
        for symbol, quantity in self.portfolio["positions"].items():
            market_data = self.generate_market_data(symbol)
            total_value += quantity * market_data["price"]
        
        self.portfolio["total_value"] = total_value
        
        return {
            "cash": self.portfolio["cash"],
            "positions": self.portfolio["positions"],
            "total_value": round(total_value, 2),
            "total_return": round(total_value - 100000, 2),
            "return_percent": round(((total_value - 100000) / 100000) * 100, 2)
        }

trading_bot = AITradingBot()

@app.route("/")
def root():
    return jsonify({
        "message": "🤖 AI Trading Bot - Advanced algorithmic trading platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "ML-powered price predictions",
            "Automated trading strategies",
            "Risk management systems",
            "Real-time market analysis",
            "Portfolio optimization"
        ]
    })

@app.route("/api/market-data/<symbol>")
def get_market_data(symbol="AAPL"):
    data = trading_bot.generate_market_data(symbol)
    return jsonify({"success": True, "data": data})

@app.route("/api/predict", methods=["POST"])
def predict_price():
    data = request.json
    symbol = data.get("symbol", "AAPL")
    strategy = data.get("strategy", "LSTM Neural Network")
    
    prediction = trading_bot.predict_price(symbol, strategy)
    return jsonify({"success": True, "prediction": prediction})

@app.route("/api/backtest", methods=["POST"])
def backtest_strategy():
    data = request.json
    symbol = data.get("symbol", "AAPL")
    strategy = data.get("strategy", "LSTM Neural Network")
    days = data.get("days", 30)
    
    results = trading_bot.backtest_strategy(symbol, strategy, days)
    return jsonify({"success": True, "results": results})

@app.route("/api/trade", methods=["POST"])
def execute_trade():
    data = request.json
    symbol = data.get("symbol", "AAPL")
    action = data.get("action", "BUY")
    quantity = data.get("quantity", 10)
    price = data.get("price", 150.0)
    
    trade = trading_bot.execute_trade(symbol, action, quantity, price)
    return jsonify({"success": True, "trade": trade})

@app.route("/api/portfolio")
def get_portfolio():
    portfolio = trading_bot.get_portfolio_status()
    return jsonify({"success": True, "portfolio": portfolio})

@app.route("/api/strategies")
def get_strategies():
    return jsonify({"success": True, "strategies": trading_bot.strategies})

@app.route("/api/trade-history")
def get_trade_history():
    return jsonify({"success": True, "trades": trading_bot.trade_history})

if __name__ == "__main__":
    print("🤖 AI Trading Bot Starting...")
    print("💡 Advanced algorithmic trading platform")
    print("🌐 API running on http://localhost:8002")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/ai-trading-bot/frontend/index.html")
    print("📈 Ready for AI-powered trading!")
    app.run(debug=True, host="0.0.0.0", port=8002)

