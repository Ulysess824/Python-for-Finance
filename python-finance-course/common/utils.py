"""Shared helpers for the course notebooks."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"
TRADING_DAYS = 252

# Palette shared with the slides, so every notebook looks the same.
RED, INK, GRAY, LIGHT, TEAL = "#A6192E", "#1f1f1f", "#5f5f5f", "#d9d9d9", "#2a7f8e"
PALETTE = [RED, TEAL, INK, "#c98b2b", GRAY, "#7a4e9c"]


def set_plot_style() -> None:
    """One matplotlib style for every notebook."""
    import matplotlib.pyplot as plt
    from cycler import cycler

    plt.rcParams.update({
        "figure.figsize": (10, 4.5),
        "figure.dpi": 100,
        "axes.prop_cycle": cycler(color=PALETTE),
        "axes.grid": True,
        "grid.color": LIGHT,
        "grid.linewidth": 0.8,
        "axes.edgecolor": GRAY,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.labelcolor": GRAY,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "legend.frameon": False,
        "lines.linewidth": 1.8,
    })
    pd.options.display.float_format = "{:,.4f}".format


def _offline() -> bool:
    return os.environ.get("PFC_OFFLINE") == "1"


def synthetic_prices(tickers, start="2018-01-01", end=None, seed=0) -> pd.DataFrame:
    """Correlated random-walk prices. ONLY a last-resort fallback (clearly flagged)."""
    tickers = list(tickers)
    idx = pd.bdate_range(start, end or pd.Timestamp.today().normalize())
    rng = np.random.default_rng(seed)
    n = len(tickers)
    a = rng.uniform(0.2, 0.8, (n, n))
    corr = a @ a.T
    d = np.sqrt(np.diag(corr))
    corr = corr / np.outer(d, d)
    vol = rng.uniform(0.15, 0.40, n) / np.sqrt(TRADING_DAYS)
    z = rng.standard_normal((len(idx), n)) @ np.linalg.cholesky(corr).T
    rets = 0.0003 + z * vol
    return pd.DataFrame(100 * np.exp(np.cumsum(rets, axis=0)), index=idx, columns=tickers)


def download_prices(tickers, start="2018-01-01", end=None, use_fallback=True) -> pd.DataFrame:
    """Adjusted close prices (one column per ticker).

    Order: Yahoo Finance -> data/sample/prices.csv -> synthetic prices (with a loud warning).
    """
    tickers = [tickers] if isinstance(tickers, str) else list(tickers)
    try:
        if _offline():
            raise RuntimeError("PFC_OFFLINE=1")
        import yfinance as yf

        data = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False, timeout=15)["Close"]
        if isinstance(data, pd.Series):
            data = data.to_frame(tickers[0])
        data = data.dropna(how="all")
        if data.empty:
            raise ValueError("empty download")
        return data.reindex(columns=tickers).dropna(axis=1, how="all")
    except Exception as exc:  # noqa: BLE001
        if not use_fallback:
            raise
        path = SAMPLE_DIR / "prices.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            cols = [t for t in tickers if t in df.columns]
            if cols:
                print(f"[common] Descarga en vivo falló ({exc}); usando {path.name}")
                return df.loc[start:end, cols]
        print(f"[common] ⚠ Descarga falló ({exc}) y no hay data/sample: usando precios SINTÉTICOS (solo demostración).")
        return synthetic_prices(tickers, start, end)


def get_fundamentals(tickers, seed=0) -> pd.DataFrame:
    """Fundamentals per ticker (index = ticker). Yahoo -> data/sample/fundamentals.csv -> synthetic."""
    tickers = [tickers] if isinstance(tickers, str) else list(tickers)
    fields = {
        "sector": "sector", "marketCap": "market_cap", "trailingPE": "pe", "priceToBook": "pb",
        "returnOnEquity": "roe", "debtToEquity": "debt_to_equity",
        "profitMargins": "profit_margin", "revenueGrowth": "revenue_growth",
        "dividendYield": "dividend_yield",
    }
    try:
        if _offline():
            raise RuntimeError("PFC_OFFLINE=1")
        import yfinance as yf

        rows = {}
        for t in tickers:
            info = yf.Ticker(t).info
            rows[t] = {new: info.get(old) for old, new in fields.items()}
        df = pd.DataFrame.from_dict(rows, orient="index")
        if df.drop(columns="sector").dropna(how="all").empty:
            raise ValueError("empty fundamentals")
        return df
    except Exception as exc:  # noqa: BLE001
        path = SAMPLE_DIR / "fundamentals.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            keep = [t for t in tickers if t in df.index]
            if keep:
                print(f"[common] Descarga en vivo falló ({exc}); usando {path.name}")
                return df.loc[keep]
        print(f"[common] ⚠ Descarga falló ({exc}) y no hay data/sample: usando fundamentales SINTÉTICOS (solo demostración).")
        rng = np.random.default_rng(seed)
        n = len(tickers)
        return pd.DataFrame({
            "sector": rng.choice(["Tecnología", "Financiero", "Energía", "Salud", "Consumo", "Industria"], n),
            "market_cap": np.exp(rng.normal(24.5, 1.2, n)),
            "pe": rng.lognormal(2.8, 0.5, n),
            "pb": rng.lognormal(1.0, 0.7, n),
            "roe": rng.normal(0.14, 0.09, n),
            "debt_to_equity": rng.gamma(2.0, 45, n),
            "profit_margin": rng.normal(0.12, 0.07, n),
            "revenue_growth": rng.normal(0.07, 0.08, n),
            "dividend_yield": rng.uniform(0, 0.05, n),
        }, index=tickers)


def to_returns(prices, log: bool = True):
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
