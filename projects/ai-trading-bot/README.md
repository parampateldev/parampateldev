# AI Trading Bot

## Overview
Advanced AI-powered algorithmic trading platform with machine learning models for market prediction and automated trading strategies.

## Features
- **Machine Learning Models**: LSTM neural networks for price prediction
- **Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages
- **Risk Management**: Automated stop-loss and position sizing
- **Backtesting**: Historical performance analysis
- **Real-time Trading**: Live market data integration
- **Portfolio Management**: Multi-asset portfolio optimization

## Technology Stack
- **Backend**: Python, Flask, TensorFlow/PyTorch
- **ML Models**: LSTM, Random Forest, SVM
- **Data**: Yahoo Finance API, Alpha Vantage
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite for trade history

## API Endpoints
- `/api/predict` - Get ML price predictions
- `/api/backtest` - Run strategy backtesting
- `/api/trade` - Execute trades
- `/api/portfolio` - Portfolio management
- `/api/strategy` - Trading strategy management

## Installation
```bash
pip install -r requirements.txt
python backend/main.py
```

## Usage
Open `frontend/index.html` in your browser to access the trading dashboard.

## Risk Warning
Trading involves substantial risk of loss. This software is for educational purposes only.

