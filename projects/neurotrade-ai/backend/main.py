#!/usr/bin/env python3
"""
NeuroTrade AI - Neural Network Trading System
Revolutionary AI-powered trading system with neural network predictions
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import asyncio
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class TradingSignal(BaseModel):
    symbol: str
    action: str  # "BUY", "SELL", "HOLD"
    confidence: float
    price: float
    timestamp: datetime
    neural_network_output: Dict

class Portfolio(BaseModel):
    user_id: str
    cash: float
    positions: Dict[str, int]
    total_value: float
    pnl: float

class TradeOrder(BaseModel):
    symbol: str
    action: str
    quantity: int
    price: float
    order_type: str  # "MARKET", "LIMIT"

class NeuroTradeAI:
    """Neural network-powered trading system"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.portfolio = Portfolio(
            user_id="demo_user",
            cash=100000.0,
            positions={},
            total_value=100000.0,
            pnl=0.0
        )
        self.trading_history = []
        self.market_data = {}
        self._initialize_neural_models()
        self._generate_sample_data()
        
    def _initialize_neural_models(self):
        """Initialize neural network models for different assets"""
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "BTC", "ETH"]
        
        for symbol in symbols:
            # Create LSTM model for price prediction
            model = tf.keras.Sequential([
                tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(60, 5)),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.LSTM(50, return_sequences=True),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.LSTM(50),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(25),
                tf.keras.layers.Dense(3)  # BUY, SELL, HOLD probabilities
            ])
            
            model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
            
            # Train with sample data (in production, use real historical data)
            self._train_model_with_sample_data(model, symbol)
            
            self.models[symbol] = model
            self.scalers[symbol] = MinMaxScaler()
            
    def _train_model_with_sample_data(self, model, symbol):
        """Train model with sample data"""
        # Generate sample training data
        np.random.seed(42)
        sequence_length = 60
        
        # Create sample OHLCV data
        base_price = 100 if symbol in ["AAPL", "GOOGL", "MSFT", "TSLA"] else 1000
        prices = []
        current_price = base_price
        
        for _ in range(1000):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            current_price *= (1 + change)
            prices.append(current_price)
        
        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(prices) - 3):
            sequence = []
            for j in range(i - sequence_length, i):
                # OHLCV data
                o = prices[j]
                h = o * (1 + abs(np.random.normal(0, 0.01)))
                l = o * (1 - abs(np.random.normal(0, 0.01)))
                c = prices[j + 1]
                v = np.random.uniform(1000000, 10000000)
                sequence.append([o, h, l, c, v])
            
            X.append(sequence)
            
            # Create target (BUY=0, SELL=1, HOLD=2)
            future_price = prices[i + 3]
            current_price = prices[i]
            
            if future_price > current_price * 1.02:  # 2% threshold
                y.append([1, 0, 0])  # BUY
            elif future_price < current_price * 0.98:  # 2% threshold
                y.append([0, 1, 0])  # SELL
            else:
                y.append([0, 0, 1])  # HOLD
        
        X = np.array(X)
        y = np.array(y)
        
        # Normalize features
        X_reshaped = X.reshape(-1, X.shape[-1])
        X_scaled = self.scalers[symbol].fit_transform(X_reshaped)
        X_scaled = X_scaled.reshape(X.shape)
        
        # Train model
        model.fit(X_scaled, y, epochs=10, batch_size=32, verbose=0)
        logger.info(f"Neural network trained for {symbol}")
    
    def _generate_sample_data(self):
        """Generate sample market data"""
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "BTC", "ETH"]
        base_prices = {"AAPL": 150, "GOOGL": 2800, "MSFT": 300, "TSLA": 800, "BTC": 45000, "ETH": 3000}
        
        for symbol in symbols:
            self.market_data[symbol] = {
                "price": base_prices[symbol] + np.random.normal(0, base_prices[symbol] * 0.02),
                "volume": np.random.randint(1000000, 10000000),
                "change": np.random.normal(0, 0.02),
                "timestamp": datetime.now()
            }
    
    def predict_signal(self, symbol: str) -> TradingSignal:
        """Generate trading signal using neural network"""
        try:
            if symbol not in self.models:
                raise ValueError(f"No model available for {symbol}")
            
            # Get recent market data (in production, fetch from real API)
            recent_data = self._get_recent_data(symbol)
            
            # Prepare input for neural network
            X = np.array([recent_data])
            X_scaled = self.scalers[symbol].transform(X.reshape(-1, X.shape[-1]))
            X_scaled = X_scaled.reshape(X.shape)
            
            # Get prediction
            prediction = self.models[symbol].predict(X_scaled, verbose=0)[0]
            
            # Convert to trading signal
            action_scores = {
                "BUY": prediction[0],
                "SELL": prediction[1],
                "HOLD": prediction[2]
            }
            
            best_action = max(action_scores, key=action_scores.get)
            confidence = action_scores[best_action]
            
            current_price = self.market_data[symbol]["price"]
            
            return TradingSignal(
                symbol=symbol,
                action=best_action,
                confidence=float(confidence),
                price=current_price,
                timestamp=datetime.now(),
                neural_network_output={
                    "buy_probability": float(prediction[0]),
                    "sell_probability": float(prediction[1]),
                    "hold_probability": float(prediction[2])
                }
            )
            
        except Exception as e:
            logger.error(f"Prediction failed for {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def _get_recent_data(self, symbol: str) -> List:
        """Get recent market data for neural network input"""
        # Generate sample recent data (in production, fetch from real API)
        base_price = self.market_data[symbol]["price"]
        recent_data = []
        
        for i in range(60):  # 60 time steps
            price = base_price * (1 + np.random.normal(0, 0.01))
            high = price * (1 + abs(np.random.normal(0, 0.005)))
            low = price * (1 - abs(np.random.normal(0, 0.005)))
            close = price * (1 + np.random.normal(0, 0.005))
            volume = np.random.uniform(1000000, 10000000)
            
            recent_data.append([price, high, low, close, volume])
        
        return recent_data
    
    def execute_trade(self, order: TradeOrder) -> Dict:
        """Execute a trade order"""
        try:
            symbol = order.symbol
            current_price = self.market_data[symbol]["price"]
            execution_price = current_price if order.order_type == "MARKET" else order.price
            
            total_cost = execution_price * order.quantity
            
            if order.action == "BUY":
                if self.portfolio.cash < total_cost:
                    raise HTTPException(status_code=400, detail="Insufficient cash")
                
                self.portfolio.cash -= total_cost
                self.portfolio.positions[symbol] = self.portfolio.positions.get(symbol, 0) + order.quantity
                
            elif order.action == "SELL":
                if self.portfolio.positions.get(symbol, 0) < order.quantity:
                    raise HTTPException(status_code=400, detail="Insufficient shares")
                
                self.portfolio.cash += total_cost
                self.portfolio.positions[symbol] -= order.quantity
                
                if self.portfolio.positions[symbol] == 0:
                    del self.portfolio.positions[symbol]
            
            # Update portfolio value
            self._update_portfolio_value()
            
            # Record trade
            trade_record = {
                "trade_id": f"TRADE_{len(self.trading_history) + 1:06d}",
                "symbol": symbol,
                "action": order.action,
                "quantity": order.quantity,
                "price": execution_price,
                "total_value": total_cost,
                "timestamp": datetime.now(),
                "order_type": order.order_type
            }
            
            self.trading_history.append(trade_record)
            
            return {
                "success": True,
                "trade_record": trade_record,
                "portfolio": self.portfolio
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Trade execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def _update_portfolio_value(self):
        """Update portfolio total value"""
        total_value = self.portfolio.cash
        
        for symbol, quantity in self.portfolio.positions.items():
            if symbol in self.market_data:
                total_value += self.market_data[symbol]["price"] * quantity
        
        self.portfolio.total_value = total_value
        self.portfolio.pnl = total_value - 100000.0  # Initial value was 100k
    
    def get_portfolio_performance(self) -> Dict:
        """Get portfolio performance metrics"""
        self._update_portfolio_value()
        
        # Calculate metrics
        total_return = (self.portfolio.total_value - 100000.0) / 100000.0 * 100
        
        # Calculate daily returns for volatility
        if len(self.trading_history) > 1:
            returns = []
            for i in range(1, min(len(self.trading_history), 30)):
                # Simulate daily returns
                returns.append(np.random.normal(0.001, 0.02))  # 0.1% daily return, 2% volatility
            
            volatility = np.std(returns) * np.sqrt(252) * 100  # Annualized volatility
            sharpe_ratio = (np.mean(returns) * 252) / (np.std(returns) * np.sqrt(252)) if np.std(returns) > 0 else 0
        else:
            volatility = 0
            sharpe_ratio = 0
        
        return {
            "total_value": self.portfolio.total_value,
            "cash": self.portfolio.cash,
            "total_return": total_return,
            "pnl": self.portfolio.pnl,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "positions": self.portfolio.positions,
            "total_trades": len(self.trading_history)
        }

# Initialize FastAPI app
app = FastAPI(title="NeuroTrade AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI system
neuro_trade = NeuroTradeAI()

@app.get("/")
async def root():
    return {
        "message": "🚀 NeuroTrade AI - Neural Network Trading System",
        "version": "1.0.0",
        "status": "operational",
        "neural_models": len(neuro_trade.models)
    }

@app.get("/api/signals/{symbol}")
async def get_trading_signal(symbol: str):
    """Get AI trading signal for a symbol"""
    signal = neuro_trade.predict_signal(symbol.upper())
    return {"success": True, "signal": signal}

@app.get("/api/signals")
async def get_all_signals():
    """Get trading signals for all symbols"""
    signals = []
    for symbol in neuro_trade.models.keys():
        try:
            signal = neuro_trade.predict_signal(symbol)
            signals.append(signal)
        except Exception as e:
            logger.error(f"Failed to get signal for {symbol}: {e}")
    
    return {"success": True, "signals": signals}

@app.post("/api/trade")
async def execute_trade(order: TradeOrder):
    """Execute a trade order"""
    result = neuro_trade.execute_trade(order)
    return result

@app.get("/api/portfolio")
async def get_portfolio():
    """Get portfolio information"""
    performance = neuro_trade.get_portfolio_performance()
    return {"success": True, "portfolio": performance}

@app.get("/api/market-data")
async def get_market_data():
    """Get current market data"""
    return {"success": True, "market_data": neuro_trade.market_data}

@app.get("/api/trading-history")
async def get_trading_history():
    """Get trading history"""
    recent_trades = neuro_trade.trading_history[-20:]  # Last 20 trades
    return {"success": True, "trades": recent_trades}

@app.post("/api/predict-batch")
async def predict_batch(symbols: List[str]):
    """Get predictions for multiple symbols"""
    predictions = []
    for symbol in symbols:
        try:
            signal = neuro_trade.predict_signal(symbol.upper())
            predictions.append(signal)
        except Exception as e:
            logger.error(f"Batch prediction failed for {symbol}: {e}")
    
    return {"success": True, "predictions": predictions}

if __name__ == "__main__":
    print("🚀 NeuroTrade AI Starting...")
    print("🧠 Neural Network Trading System")
    print("🌐 API running on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
