import yfinance as yf
from matplotlib import pyplot as plt


def fetch_recent_gold_price(ticker: str = "GC=F") -> dict:
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
                "current_price": round(float(latest_row["Close"]), 2),
                "high": round(float(latest_row["High"]), 2),
                "low": round(float(latest_row["Low"]), 2),
                "volume": int(latest_row["Volume"]),
                "timestamp": str(data.index[-1].date())
            }
        else:
            return {
                "status": "error",
                "message": "Yahoo Finance returned an empty dataset for gold."
            }

    except Exception as e:
        return {"error": f"[yfinance] Failed to fetch live gold data: {str(e)}"}


def fetch_recent_dxy(ticker: str = "DX-Y.NYB") -> dict:
    """
    Fetches the most recent closing price indicators for the US Dollar Index (DXY)
    """
    try:
        dxy = yf.Ticker(ticker)
        data = dxy.history(period="5d", interval="1d")

        if data.empty:
            return {
                "status": "error",
                "message": "Yahoo Finance returned an empty dataset for DXY."
            }

        latest_row = data.iloc[-1]
        return {
            "status": "success",
            "ticker": ticker,
            "dxy_index": round(float(latest_row["Close"]), 2),
            "dxy_high": round(float(latest_row["High"]), 2),
            "dxy_low": round(float(latest_row["Low"]), 2),
            "timestamp": str(data.index[-1].date())
        }

    except Exception as e:
        return {"error": f"[yfinance] Failed to fetch DXY indicators: {str(e)}"}


def fetch_gold_trend(ticker: str = "GC=F") -> dict:
    """"
    Fetches historical data for Gold Futures (GC=F) over the last 7 trading days,
    calculates directional and numeric trends.
    """
    try:
        gold_ticker = yf.Ticker(ticker)
        data = gold_ticker.history(period="7d", interval="15m")

        # Check if we have sufficient data points to compute a trend
        if data.empty:
            return {
                "status": "error",
                "message": "Gold historical trend data is currently unavailable."
            }

        prices = data['Close'].tolist()
        start_price = prices[0]
        end_price = prices[-1]
        price_diff = end_price - start_price
        pct_change = (price_diff / start_price) * 100

        # Determine strict directional market sentiment
        direction = "UPWARD (Bullish)" if price_diff > 0 else "DOWNWARD (Bearish)"
        if abs(pct_change) < 0.2:
            direction = "SIDEWAYS (Neutral)"

        return {
            "status": "success",
            "direction": direction,
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "net_change": round(price_diff, 2),
            "percentage_change": round(pct_change, 2)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to compute trend metrics: {str(e)}"
        }


def plot_gold_price(ticker: str = "GC=F") -> dict:
    """
    Fetches historical data for Gold Futures (GC=F) over the last 7 trading days and plots it
    """
    try:
        gold_ticker = yf.Ticker(ticker)
        data = gold_ticker.history(period="7d", interval="15m")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data.index, data['Close'], label='Gold Price', color='#FFD700')
        ax.set_title('Gold Futures (GC=F) – Last 7 Days', fontsize=14)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return {"status": "success"}

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to plot the trend: {str(e)}"
        }


def fetch_gold_macro_news() -> dict:
    """
    Fetches the latest macroeconomic news relevant to Gold markets
    """
    from .config import tavily
    try:
        search_query = "gold price macroeconomics US interest rates DXY inflation geopolitics news"
        response = tavily.get_search_context(
            query=search_query,
            max_results=3,
            search_depth="advanced"
        )

        return {"macro_news_context": response}

    except Exception as e:
        return {"error": f"[Tavily] Failed to aggregate news data: {str(e)}"}
