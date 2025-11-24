from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import numpy as np
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

class DeFiYieldOptimizer:
    def __init__(self):
        self.protocols = [
            "Uniswap V3", "SushiSwap", "Compound", "Aave", "Curve",
            "Yearn Finance", "PancakeSwap", "Venus", "Synthetix"
        ]
        self.portfolio = {
            "total_value": 100000,
            "positions": [],
            "total_yield": 0,
            "daily_yield": 0
        }
        self.yield_history = []

    def generate_liquidity_pools(self):
        pool_types = ["ETH/USDC", "WBTC/ETH", "DAI/USDC", "LINK/ETH", "UNI/ETH"]
        pools = []
        
        for i in range(20):
            pool_type = random.choice(pool_types)
            protocol = random.choice(self.protocols)
            
            pool = {
                "id": f"POOL_{i:03d}",
                "name": f"{pool_type} - {protocol}",
                "protocol": protocol,
                "tokens": pool_type.split("/"),
                "tvl": random.randint(1000000, 50000000),
                "apy": round(random.uniform(5, 150), 2),
                "risk_score": random.uniform(1, 10),
                "impermanent_loss": round(random.uniform(0, 50), 2),
                "gas_cost": random.randint(50, 500),
                "minimum_deposit": random.randint(100, 10000),
                "last_updated": datetime.now().isoformat()
            }
            pools.append(pool)
        
        return sorted(pools, key=lambda x: x["apy"], reverse=True)

    def calculate_optimal_strategy(self, budget, risk_tolerance, time_horizon):
        pools = self.generate_liquidity_pools()
        
        # Filter pools based on criteria
        suitable_pools = [
            p for p in pools 
            if p["risk_score"] <= risk_tolerance * 10 and 
               p["minimum_deposit"] <= budget and
               p["tvl"] > 1000000  # Minimum TVL for safety
        ]
        
        if not suitable_pools:
            return {"message": "No suitable pools found for your criteria"}
        
        # Sort by risk-adjusted APY
        suitable_pools.sort(key=lambda x: x["apy"] / x["risk_score"], reverse=True)
        
        # Allocate budget across top pools
        allocation = []
        remaining_budget = budget
        
        for pool in suitable_pools[:5]:  # Top 5 pools
            if remaining_budget <= 0:
                break
                
            allocation_percent = random.uniform(0.1, 0.3)
            allocation_amount = min(budget * allocation_percent, remaining_budget)
            
            if allocation_amount >= pool["minimum_deposit"]:
                allocation.append({
                    "pool": pool,
                    "amount": allocation_amount,
                    "percentage": (allocation_amount / budget) * 100,
                    "expected_apy": pool["apy"],
                    "risk_score": pool["risk_score"]
                })
                remaining_budget -= allocation_amount
        
        # Calculate portfolio metrics
        total_weighted_apy = sum(a["expected_apy"] * (a["amount"] / budget) for a in allocation)
        avg_risk_score = sum(a["risk_score"] * (a["amount"] / budget) for a in allocation)
        
        return {
            "allocation": allocation,
            "total_invested": sum(a["amount"] for a in allocation),
            "expected_apy": round(total_weighted_apy, 2),
            "average_risk_score": round(avg_risk_score, 2),
            "estimated_daily_yield": round((total_weighted_apy / 365) * budget, 2),
            "estimated_monthly_yield": round((total_weighted_apy / 12) * budget, 2),
            "strategy_score": round((total_weighted_apy / avg_risk_score) * 10, 2)
        }

    def get_yield_rates(self):
        protocols_data = {}
        
        for protocol in self.protocols:
            protocols_data[protocol] = {
                "avg_apy": round(random.uniform(8, 80), 2),
                "tvl": random.randint(50000000, 2000000000),
                "active_pools": random.randint(10, 100),
                "risk_level": random.choice(["Low", "Medium", "High"]),
                "gas_efficiency": random.uniform(0.5, 1.0)
            }
        
        return protocols_data

    def simulate_yield_performance(self, days=30):
        # Simulate historical yield data
        base_yield = random.uniform(15, 45)
        performance = []
        
        for day in range(days):
            daily_change = random.uniform(-0.02, 0.02)
            base_yield += daily_change
            base_yield = max(5, min(100, base_yield))  # Keep within reasonable bounds
            
            performance.append({
                "day": day + 1,
                "apy": round(base_yield, 2),
                "daily_yield": round((base_yield / 365) * self.portfolio["total_value"], 2),
                "cumulative_yield": round(sum(p["daily_yield"] for p in performance), 2)
            })
        
        return performance

    def compound_yield(self, position_id, auto_compound=True):
        # Simulate compound yield action
        compound_result = {
            "position_id": position_id,
            "action": "compound",
            "amount": round(random.uniform(100, 1000), 2),
            "gas_cost": random.randint(20, 100),
            "timestamp": datetime.now().isoformat(),
            "success": random.choice([True, True, True, False])  # 75% success rate
        }
        
        if compound_result["success"]:
            self.portfolio["total_value"] += compound_result["amount"]
            self.yield_history.append(compound_result)
        
        return compound_result

    def get_portfolio_performance(self):
        # Calculate portfolio performance metrics
        total_deposited = 100000  # Initial deposit
        current_value = self.portfolio["total_value"]
        total_yield = current_value - total_deposited
        
        # Simulate some historical performance
        performance_history = self.simulate_yield_performance(30)
        
        return {
            "total_deposited": total_deposited,
            "current_value": current_value,
            "total_yield": total_yield,
            "yield_percentage": round((total_yield / total_deposited) * 100, 2),
            "daily_yield": round(performance_history[-1]["daily_yield"], 2),
            "monthly_yield": round(performance_history[-1]["cumulative_yield"], 2),
            "performance_history": performance_history,
            "positions": len(self.portfolio["positions"]),
            "avg_apy": round(random.uniform(20, 60), 2)
        }

defi_optimizer = DeFiYieldOptimizer()

@app.route("/")
def root():
    return jsonify({
        "message": "🌾 DeFi Yield Farming Optimizer - Maximize your DeFi returns",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Multi-protocol yield optimization",
            "Risk-adjusted portfolio allocation",
            "Automated compounding strategies",
            "Real-time yield monitoring",
            "Gas fee optimization"
        ]
    })

@app.route("/api/pools")
def get_liquidity_pools():
    pools = defi_optimizer.generate_liquidity_pools()
    return jsonify({"success": True, "pools": pools})

@app.route("/api/yield-rates")
def get_yield_rates():
    rates = defi_optimizer.get_yield_rates()
    return jsonify({"success": True, "rates": rates})

@app.route("/api/optimize", methods=["POST"])
def optimize_strategy():
    data = request.json
    budget = data.get("budget", 10000)
    risk_tolerance = data.get("risk_tolerance", 0.5)
    time_horizon = data.get("time_horizon", 30)
    
    strategy = defi_optimizer.calculate_optimal_strategy(budget, risk_tolerance, time_horizon)
    return jsonify({"success": True, "strategy": strategy})

@app.route("/api/portfolio")
def get_portfolio_performance():
    performance = defi_optimizer.get_portfolio_performance()
    return jsonify({"success": True, "performance": performance})

@app.route("/api/compound", methods=["POST"])
def compound_yield():
    data = request.json
    position_id = data.get("position_id", "POSITION_001")
    auto_compound = data.get("auto_compound", True)
    
    result = defi_optimizer.compound_yield(position_id, auto_compound)
    return jsonify({"success": True, "result": result})

@app.route("/api/performance-history")
def get_performance_history():
    performance = defi_optimizer.get_portfolio_performance()
    return jsonify({"success": True, "history": performance["performance_history"]})

if __name__ == "__main__":
    print("🌾 DeFi Yield Farming Optimizer Starting...")
    print("💡 Maximize your DeFi returns with AI optimization")
    print("🌐 API running on http://localhost:8003")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/defi-yield-optimizer/frontend/index.html")
    print("🚀 Ready for yield farming optimization!")
    app.run(debug=True, host="0.0.0.0", port=8003)

