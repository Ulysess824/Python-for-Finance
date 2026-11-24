#!/usr/bin/env python
"""Generate a self-contained HTML report for a list of tickers.

Usage:
    python report.py AAPL MSFT JPM --start 2020-01-01 --out output/report.html
"""
from __future__ import annotations

import argparse
import base64
import io
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from common import (  # noqa: E402
    annualized_return, annualized_vol, download_prices, max_drawdown,
    set_plot_style, sharpe_ratio, to_returns,
)


def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def build_report(tickers: list[str], start: str) -> str:
    set_plot_style()
    prices = download_prices(tickers, start=start)
    rets = to_returns(prices, log=False)

    stats = pd.DataFrame({
        "Retorno anual": annualized_return(rets),
        "Volatilidad": annualized_vol(rets),
        "Sharpe": sharpe_ratio(rets),
        "Max drawdown": (1 + rets).cumprod().apply(max_drawdown),
    })
    fmt = {c: "{:.1%}".format for c in ["Retorno anual", "Volatilidad", "Max drawdown"]}
    fmt["Sharpe"] = "{:.2f}".format

    fig, ax = plt.subplots()
    (prices / prices.iloc[0] * 100).plot(ax=ax, title="Precio rebasado a 100")
    img_prices = fig_to_b64(fig)

    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(rets.corr(), cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(rets.columns)), rets.columns, rotation=45)
    ax.set_yticks(range(len(rets.columns)), rets.columns)
    fig.colorbar(im)
    ax.set_title("Correlaciones")
    ax.grid(False)
    img_corr = fig_to_b64(fig)

    return f"""<!doctype html><html lang="es"><meta charset="utf-8">
<title>Informe de mercado</title>
<style>body{{font-family:system-ui;max-width:900px;margin:2rem auto;padding:0 1rem}}
table{{border-collapse:collapse}}td,th{{padding:.4rem .8rem;border-bottom:1px solid #ddd;text-align:right}}
th:first-child,td:first-child{{text-align:left}}img{{max-width:100%}}</style>
<h1>Informe de mercado</h1>
<p>{date.today():%d/%m/%Y} · {', '.join(tickers)} · desde {start}</p>
<h2>Métricas</h2>{stats.to_html(formatters=fmt, border=0)}
<h2>Evolución</h2><img src="data:image/png;base64,{img_prices}">
<h2>Correlaciones</h2><img src="data:image/png;base64,{img_corr}">
</html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--out", default="output/report.html")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(args.tickers, args.start), encoding="utf-8")
    print(f"Report written to {out}")


if __name__ == "__main__":
    main()
