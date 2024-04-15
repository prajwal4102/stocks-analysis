# INTELIINVEST(STOCK-ANALYSIS)
Discover our Stock Prediction and Analysis Toolkit! Python programs for historical stock data analysis and future trend prediction. It offers a comprehensive toolset for informed investment decisions based on data analysis and machine learning.

## Overview
This project is an INTELIINVEST designed to provide buy/sell signals for trading based on technical analysis indicators. It uses historical price data from Yahoo Finance and implements a candlestick pattern recognition strategy along with support and resistance levels, ATR (Average True Range), and RSI (Relative Strength Index) indicators.

## Features
- **Candlestick pattern recognition (shooting star pattern)
- **Support and resistance levels identification
- **Fixed Stop Loss (SL) and Take Profit (TP) levels based on risk percentage and reward-to-risk ratio
- **Backtesting functionality to test the strategy performance on historical data

## Requirements
-Python 3.x
-Required libraries: yfinance, pandas, numpy, plotly, pandas_ta, backtesting

## Usage

Install the required libraries:
```bash
pip install yfinance pandas numpy plotly pandas_ta backtesting
```

Run the support_and_rejection_strategy.py script to fetch historical data, identify candlestick patterns and support/resistance levels, calculate ATR and RSI indicators, generate buy/sell signals, and perform backtesting.
```bash
python support_and_rejection_strategy.py
```

View the backtest results and performance metrics.


##Strategy Details
- **Candlestick Pattern Recognition**: Identifies shooting star patterns based on specific criteria.
- **Support and Resistance Levels**: Determines support and resistance levels based on historical price data.
- **Stop Loss and Take Profit**: Implements fixed SL and TP levels based on risk percentage and reward-to-risk ratio.

## Files
- **support_and_rejection_strategy.py**: Contains the main code for data fetching, signal generation, and backtesting.
- **README.md**: This file, providing an overview of the project and instructions.

## Disclaimer
This project is for educational and informational purposes only. It does not constitute financial advice. Trading involves risks, and past performance is not indicative of future results. Use this tool at your own risk and discretion.

## Author
# prajwal4102

