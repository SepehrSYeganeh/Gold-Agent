import yfinance as yf
import pandas as pd


def fetch_live_gold_price(ticker: str = "GC=F") -> dict:
    """
    Fetches the most recent live market price metrics for Gold
    """
    try:
        gold = yf.Ticker(ticker)
        data = gold.history(period="2d", interval="5m")

        if data.empty:
            # Fallback to daily bars during weekend closures
            data = gold.history(period="5d")

        if not data.empty:
            latest_row = data.iloc[-1]
            return {
                "status": "success",
                "ticker": ticker,
                "current_price": round(float(latest_row['Close']), 2),
                "high": round(float(latest_row['High']), 2),
                "low": round(float(latest_row['Low']), 2),
                "volume": int(latest_row['Volume']),
                "timestamp": str(data.index[-1])
            }
        else:
            raise ValueError("Yahoo Finance returned an empty dataset for gold.")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch live gold data: {str(e)}"
        }
