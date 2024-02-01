# Trading-Bot
## Overview
This project implements a simple trading bot using the Backtrader library, a popular Python library for backtesting and live trading of financial markets. The trading strategy implemented in this bot involves a combination of moving averages, relative strength index (RSI), and moving average convergence divergence (MACD) indicators.

## Functionality
The trading bot is designed to make buy and sell decisions based on various technical indicators. It aims to capture trends and reversals in the market. The key features include:
- **Golden Cross and Death Cross:** The bot uses a crossover of exponential moving averages (EMA) as a signal for buying (Golden Cross) or selling (Death Cross).
- **Trend Following with SMA:** The bot incorporates a simple moving average (SMA) to identify the overall trend, buying when the SMA crosses above the price and selling when it crosses below.
- **RSI and MACD Indicators:** The bot considers RSI for overbought and oversold conditions, and MACD for identifying potential trend reversals.
- **Dynamic Stop Loss:** A dynamic stop-loss mechanism is implemented to mitigate potential losses, set at 10% below the entry point.
- **Signal Validation:** Both RSI and MACD buying and selling signals are only taken into account when the signal is backed by the current trend marked by the SMA.

## Technologies Used
- **Backtrader:** The core library for backtesting and executing trading strategies.
- **Python**

## Usage
1. Install Backtrader: `pip install backtrader`
2. Clone the repository: `git clone <repo-url>`
3. Navigate to the project directory: `cd <project-directory>`
4. Run the bot: `python trading_bot.py`

## Data Source
The bot uses historical price data for Oracle Corporation (ORCL) from Yahoo Finance for the period 1995-2014.

## Configuration
The bot's behavior can be adjusted by modifying parameters in the `params` dictionary within the `Strategy` class. Parameters such as EMA periods, RSI thresholds, MACD periods, SMA period, and stop loss percentage can be fine-tuned.

## Results
The bot will output information about executed trades and the final portfolio value. Additionally, a plot of the historical data with buy and sell signals will be displayed.
