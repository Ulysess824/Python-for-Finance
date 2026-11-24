#!/usr/bin/env python
"""Download live data and store it in data/sample/ as a fallback for the class."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import download_prices, get_fundamentals  # noqa: E402
from common.utils import SAMPLE_DIR  # noqa: E402

TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "JNJ", "NVDA", "KO", "PG", "CVX", "BAC",
           "WMT", "PFE", "GLD", "TLT", "SPY", "^GSPC", "EC", "CIB"]

SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
download_prices(TICKERS, start="2005-01-01", use_sample_fallback=False).to_csv(SAMPLE_DIR / "prices.csv")
get_fundamentals([t for t in TICKERS if not t.startswith("^") and t not in {"GLD", "TLT", "SPY"}]).to_csv(
    SAMPLE_DIR / "fundamentals.csv")
print("Sample data refreshed in", SAMPLE_DIR)
