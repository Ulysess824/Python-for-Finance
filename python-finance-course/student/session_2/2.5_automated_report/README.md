# 2.5 · Informe automatizado

Script que descarga precios, calcula métricas (retorno, volatilidad, Sharpe, max drawdown) y genera un
informe HTML autocontenido (gráficos embebidos en base64).

```bash
python report.py AAPL MSFT JPM --start 2020-01-01 --out output/report.html
```

**Ejercicio:** añade una sección con el VaR de cada activo, o programa el script con `cron` / GitHub Actions
para generar el informe cada día.
