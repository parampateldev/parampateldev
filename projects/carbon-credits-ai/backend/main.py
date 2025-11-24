#!/usr/bin/env python3
"""
CarbonCredits AI - Revolutionary Carbon Trading Platform
AI-powered carbon credit marketplace with real-time pricing and optimization
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class CarbonCredit(BaseModel):
    id: str
    type: str  # "renewable", "forest", "ocean", "industrial"
    price: float
    volume: int
    location: str
    certification: str
    co2_tons: float
    timestamp: datetime

class TradeRequest(BaseModel):
    credit_id: str
    quantity: int
    buyer_id: str
    price_per_ton: float

class PortfolioOptimization(BaseModel):
    user_id: str
    budget: float
    risk_tolerance: float
    sustainability_goals: List[str]

class CarbonCreditsAI:
    """AI-powered carbon credit trading system"""
    
    def __init__(self):
        self.credits: List[CarbonCredit] = []
        self.price_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.trading_history = []
        self.market_data = pd.DataFrame()
        self._initialize_market_data()
        self._train_price_model()
        
    def _initialize_market_data(self):
        """Initialize sample market data for AI training"""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        
        data = []
        for date in dates:
            # Simulate carbon credit market data
            base_price = 25 + np.random.normal(0, 5)
            volume = 1000 + np.random.normal(0, 200)
            temperature = 15 + 10 * np.sin(2 * np.pi * date.dayofyear / 365) + np.random.normal(0, 3)
            
            data.append({
                'date': date,
                'price': max(base_price, 5),  # Minimum price of $5
                'volume': max(volume, 100),
                'temperature': temperature,
                'season': date.month % 4,
                'day_of_week': date.weekday(),
                'carbon_demand': np.random.uniform(0.7, 1.3)
            })
        
        self.market_data = pd.DataFrame(data)
        
        # Initialize sample carbon credits
        credit_types = ["renewable", "forest", "ocean", "industrial"]
        certifications = ["VCS", "Gold Standard", "CDM", "CAR"]
        locations = ["USA", "Brazil", "India", "Germany", "Australia"]
        
        for i in range(50):
            credit_type = np.random.choice(credit_types)
            base_price = self._get_base_price_for_type(credit_type)
            price = base_price + np.random.normal(0, base_price * 0.1)
            
            credit = CarbonCredit(
                id=f"CC_{i:03d}",
                type=credit_type,
                price=max(price, 5),
                volume=np.random.randint(100, 5000),
                location=np.random.choice(locations),
                certification=np.random.choice(certifications),
                co2_tons=np.random.uniform(0.5, 10.0),
                timestamp=datetime.now() - timedelta(days=np.random.randint(0, 30))
            )
            self.credits.append(credit)
    
    def _get_base_price_for_type(self, credit_type: str) -> float:
        """Get base price for different credit types"""
        base_prices = {
            "renewable": 30,
            "forest": 25,
            "ocean": 35,
            "industrial": 20
        }
        return base_prices.get(credit_type, 25)
    
    def _train_price_model(self):
        """Train AI model for price prediction"""
        try:
            # Prepare features for ML model
            X = self.market_data[['volume', 'temperature', 'season', 'day_of_week', 'carbon_demand']]
            y = self.market_data['price']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.price_model.fit(X_train, y_train)
            
            # Calculate model accuracy
            score = self.price_model.score(X_test, y_test)
            logger.info(f"Carbon credit price prediction model trained with accuracy: {score:.3f}")
            
        except Exception as e:
            logger.error(f"Failed to train price model: {e}")
    
    def predict_optimal_price(self, credit: CarbonCredit) -> float:
        """Predict optimal price for a carbon credit using AI"""
        try:
            # Prepare features for prediction
            features = np.array([[
                credit.volume,
                np.random.uniform(10, 30),  # Simulated temperature
                datetime.now().month % 4,   # Season
                datetime.now().weekday(),   # Day of week
                np.random.uniform(0.8, 1.2) # Carbon demand
            ]])
            
            predicted_price = self.price_model.predict(features)[0]
            
            # Adjust based on credit type and certification
            type_multiplier = {
                "renewable": 1.1,
                "forest": 1.0,
                "ocean": 1.2,
                "industrial": 0.9
            }
            
            cert_multiplier = {
                "VCS": 1.0,
                "Gold Standard": 1.15,
                "CDM": 1.05,
                "CAR": 1.08
            }
            
            adjusted_price = predicted_price * type_multiplier.get(credit.type, 1.0) * cert_multiplier.get(credit.certification, 1.0)
            
            return max(adjusted_price, 5)  # Minimum price of $5
            
        except Exception as e:
            logger.error(f"Price prediction failed: {e}")
            return credit.price
    
    def optimize_portfolio(self, optimization: PortfolioOptimization) -> Dict:
        """AI-powered portfolio optimization"""
        try:
            # Filter credits by sustainability goals
            available_credits = []
            for credit in self.credits:
                if credit.type in optimization.sustainability_goals or not optimization.sustainability_goals:
                    available_credits.append(credit)
            
            if not available_credits:
                raise HTTPException(status_code=400, detail="No credits match sustainability goals")
            
            # Calculate risk-adjusted returns
            portfolio = []
            remaining_budget = optimization.budget
            
            # Sort credits by AI-predicted value
            credits_with_predictions = []
            for credit in available_credits:
                predicted_price = self.predict_optimal_price(credit)
                value_score = (predicted_price / credit.price) * (1 / (1 + optimization.risk_tolerance))
                credits_with_predictions.append((credit, predicted_price, value_score))
            
            credits_with_predictions.sort(key=lambda x: x[2], reverse=True)
            
            # Build optimal portfolio
            for credit, predicted_price, value_score in credits_with_predictions:
                if remaining_budget <= 0:
                    break
                
                max_quantity = min(
                    credit.volume,
                    int(remaining_budget / predicted_price)
                )
                
                if max_quantity > 0:
                    portfolio.append({
                        "credit_id": credit.id,
                        "type": credit.type,
                        "quantity": max_quantity,
                        "price_per_ton": predicted_price,
                        "total_cost": max_quantity * predicted_price,
                        "co2_tons": max_quantity * credit.co2_tons,
                        "predicted_return": value_score
                    })
                    remaining_budget -= max_quantity * predicted_price
            
            # Calculate portfolio metrics
            total_cost = sum(item["total_cost"] for item in portfolio)
            total_co2 = sum(item["co2_tons"] for item in portfolio)
            avg_price = total_cost / total_co2 if total_co2 > 0 else 0
            
            return {
                "portfolio": portfolio,
                "total_cost": total_cost,
                "total_co2_tons": total_co2,
                "average_price_per_ton": avg_price,
                "remaining_budget": remaining_budget,
                "diversification_score": len(set(item["type"] for item in portfolio)) / 4,
                "sustainability_impact": self._calculate_sustainability_impact(portfolio)
            }
            
        except Exception as e:
            logger.error(f"Portfolio optimization failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def _calculate_sustainability_impact(self, portfolio: List[Dict]) -> Dict:
        """Calculate sustainability impact metrics"""
        type_impacts = {
            "renewable": {"co2_reduction": 1.0, "biodiversity": 0.8, "social_impact": 0.9},
            "forest": {"co2_reduction": 1.2, "biodiversity": 1.0, "social_impact": 0.7},
            "ocean": {"co2_reduction": 0.9, "biodiversity": 1.1, "social_impact": 0.6},
            "industrial": {"co2_reduction": 1.1, "biodiversity": 0.5, "social_impact": 0.8}
        }
        
        total_impact = {"co2_reduction": 0, "biodiversity": 0, "social_impact": 0}
        
        for item in portfolio:
            impact = type_impacts.get(item["type"], {"co2_reduction": 1.0, "biodiversity": 0.8, "social_impact": 0.8})
            weight = item["co2_tons"]
            
            for metric in total_impact:
                total_impact[metric] += impact[metric] * weight
        
        # Normalize scores
        total_co2 = sum(item["co2_tons"] for item in portfolio)
        if total_co2 > 0:
            for metric in total_impact:
                total_impact[metric] /= total_co2
        
        return total_impact
    
    def execute_trade(self, trade: TradeRequest) -> Dict:
        """Execute a carbon credit trade"""
        try:
            # Find the credit
            credit = next((c for c in self.credits if c.id == trade.credit_id), None)
            if not credit:
                raise HTTPException(status_code=404, detail="Carbon credit not found")
            
            if credit.volume < trade.quantity:
                raise HTTPException(status_code=400, detail="Insufficient credit volume")
            
            # Execute trade
            trade_cost = trade.quantity * trade.price_per_ton
            co2_tons = trade.quantity * credit.co2_tons
            
            # Update credit volume
            credit.volume -= trade.quantity
            
            # Record trade
            trade_record = {
                "trade_id": f"TRADE_{len(self.trading_history) + 1:06d}",
                "credit_id": trade.credit_id,
                "buyer_id": trade.buyer_id,
                "quantity": trade.quantity,
                "price_per_ton": trade.price_per_ton,
                "total_cost": trade_cost,
                "co2_tons": co2_tons,
                "timestamp": datetime.now(),
                "credit_type": credit.type,
                "location": credit.location
            }
            
            self.trading_history.append(trade_record)
            
            return {
                "success": True,
                "trade_record": trade_record,
                "remaining_volume": credit.volume
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Trade execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Initialize FastAPI app
app = FastAPI(title="CarbonCredits AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI system
carbon_ai = CarbonCreditsAI()

@app.get("/")
async def root():
    return {
        "message": "🚀 CarbonCredits AI - Revolutionary Carbon Trading Platform",
        "version": "1.0.0",
        "status": "operational",
        "ai_model_accuracy": "trained"
    }

@app.get("/api/credits")
async def get_carbon_credits():
    """Get all available carbon credits"""
    return {
        "success": True,
        "credits": carbon_ai.credits,
        "total_count": len(carbon_ai.credits)
    }

@app.get("/api/credits/{credit_id}")
async def get_credit_details(credit_id: str):
    """Get details of a specific carbon credit"""
    credit = next((c for c in carbon_ai.credits if c.id == credit_id), None)
    if not credit:
        raise HTTPException(status_code=404, detail="Carbon credit not found")
    
    # Get AI price prediction
    predicted_price = carbon_ai.predict_optimal_price(credit)
    
    return {
        "success": True,
        "credit": credit,
        "ai_predicted_price": predicted_price,
        "price_confidence": 0.85  # Simulated confidence score
    }

@app.post("/api/optimize-portfolio")
async def optimize_portfolio(optimization: PortfolioOptimization):
    """AI-powered portfolio optimization"""
    result = carbon_ai.optimize_portfolio(optimization)
    return {"success": True, "optimization": result}

@app.post("/api/trade")
async def execute_trade(trade: TradeRequest):
    """Execute a carbon credit trade"""
    result = carbon_ai.execute_trade(trade)
    return result

@app.get("/api/market-analytics")
async def get_market_analytics():
    """Get market analytics and trends"""
    if carbon_ai.market_data.empty:
        return {"success": False, "error": "No market data available"}
    
    latest_data = carbon_ai.market_data.tail(30)  # Last 30 days
    
    analytics = {
        "average_price": float(latest_data['price'].mean()),
        "price_volatility": float(latest_data['price'].std()),
        "total_volume": int(latest_data['volume'].sum()),
        "price_trend": "up" if latest_data['price'].iloc[-1] > latest_data['price'].iloc[0] else "down",
        "market_sentiment": "bullish" if latest_data['price'].mean() > carbon_ai.market_data['price'].mean() else "bearish"
    }
    
    return {"success": True, "analytics": analytics}

@app.get("/api/trading-history")
async def get_trading_history():
    """Get recent trading history"""
    recent_trades = carbon_ai.trading_history[-20:]  # Last 20 trades
    return {"success": True, "trades": recent_trades}

if __name__ == "__main__":
    print("🌱 CarbonCredits AI Starting...")
    print("💡 Revolutionary AI-powered carbon trading platform")
    print("🌐 API running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
