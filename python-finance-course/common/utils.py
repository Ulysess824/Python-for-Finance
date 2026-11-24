"""Shared helpers for the course notebooks."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"
TRADING_DAYS = 252


def set_plot_style() -> None:
    """Consistent matplotlib style for every notebook."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.figsize": (10, 5),
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "legend.frameon": False,
    })


def download_prices(tickers, start="2018-01-01", end=None, use_sample_fallback=True) -> pd.DataFrame:
    """Adjusted close prices (one column per ticker).

    Tries Yahoo Finance first; if it fails (or returns nothing) falls back to
    ``data/sample/prices.csv`` so the class can continue without the live API.
    """
    tickers = [tickers] if isinstance(tickers, str) else list(tickers)
    try:
        import yfinance as yf

        data = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
        if isinstance(data, pd.Series):
            data = data.to_frame(tickers[0])
        data = data.dropna(how="all")
        if data.empty:
            raise ValueError("empty download")
        return data[tickers]
    except Exception as exc:  # noqa: BLE001
        if not use_sample_fallback:
            raise
        path = SAMPLE_DIR / "prices.csv"
        if not path.exists():
            raise FileNotFoundError(f"Live download failed ({exc}) and {path} does not exist.") from exc
        print(f"[common.utils] Live download failed ({exc}); using {path.name}")
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        cols = [t for t in tickers if t in df.columns]
        return df.loc[start:end, cols] if cols else df.loc[start:end]


def get_fundamentals(tickers) -> pd.DataFrame:
    """Key fundamentals per ticker (index = ticker). Falls back to data/sample/fundamentals.csv."""
    tickers = [tickers] if isinstance(tickers, str) else list(tickers)
    fields = {
        "marketCap": "market_cap", "trailingPE": "pe", "priceToBook": "pb",
        "returnOnEquity": "roe", "debtToEquity": "debt_to_equity",
        "profitMargins": "profit_margin", "revenueGrowth": "revenue_growth",
        "dividendYield": "dividend_yield",
    }
    try:
        import yfinance as yf

        rows = {t: {new: yf.Ticker(t).info.get(old) for old, new in fields.items()} for t in tickers}
        df = pd.DataFrame.from_dict(rows, orient="index")
        if df.dropna(how="all").empty:
            raise ValueError("empty fundamentals")
        return df
    except Exception as exc:  # noqa: BLE001
        path = SAMPLE_DIR / "fundamentals.csv"
        if not path.exists():
            raise FileNotFoundError(f"Live download failed ({exc}) and {path} does not exist.") from exc
        print(f"[common.utils] Live download failed ({exc}); using {path.name}")
        df = pd.read_csv(path, index_col=0)
        return df.loc[[t for t in tickers if t in df.index]] if tickers else df


def to_returns(prices: pd.DataFrame | pd.Series, log: bool = True):
    r = np.log(prices / prices.shift(1)) if log else prices.pct_change()
    return r.dropna()


def annualized_return(returns, periods: int = TRADING_DAYS):
    return returns.mean() * periods


def annualized_vol(returns, periods: int = TRADING_DAYS):
    return returns.std() * np.sqrt(periods)


def sharpe_ratio(returns, rf: float = 0.0, periods: int = TRADING_DAYS):
    return (annualized_return(returns, periods) - rf) / annualized_vol(returns, periods)


def max_drawdown(equity_curve: pd.Series) -> float:
    peak = equity_curve.cummax()
    return float((equity_curve / peak - 1).min())
