# Sample data

Copias de seguridad en CSV por si falla la API en vivo (Yahoo Finance). `common.utils` las usa automáticamente.

| Archivo | Contenido |
|---|---|
| `prices.csv` | Precios ajustados diarios (índice = fecha, columnas = tickers) |
| `fundamentals.csv` | Fundamentales por ticker (`pe, pb, roe, debt_to_equity, profit_margin, revenue_growth, dividend_yield, market_cap`) |

Regenerar: `python tools/refresh_sample_data.py` (requiere conexión).
