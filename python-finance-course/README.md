# Python for Finance — Course

Curso práctico de finanzas cuantitativas con Python en dos sesiones.

## Contenido

| # | Notebook | Tema |
|---|---|---|
| 1.1 | [1.1_var_monte_carlo](student/session_1/1.1_var_monte_carlo.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_1/1.1_var_monte_carlo.ipynb) | VaR con Monte Carlo |
| 1.2 | [1.2_black_scholes](student/session_1/1.2_black_scholes.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_1/1.2_black_scholes.ipynb) | Black-Scholes y griegas |
| 1.3 | [1.3_garch](student/session_1/1.3_garch.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_1/1.3_garch.ipynb) | Volatilidad GARCH |
| 1.4 | [1.4_portfolio_optimization](student/session_1/1.4_portfolio_optimization.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_1/1.4_portfolio_optimization.ipynb) | Optimización de carteras |
| 1.5 | [1.5_backtesting](student/session_1/1.5_backtesting.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_1/1.5_backtesting.ipynb) | Backtesting |
| 2.1 | [2.1_data_consolidation](student/session_2/2.1_data_consolidation.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_2/2.1_data_consolidation.ipynb) | Consolidación de datos |
| 2.2 | [2.2_fundamental_screening](student/session_2/2.2_fundamental_screening.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_2/2.2_fundamental_screening.ipynb) | Screening fundamental |
| 2.3 | [2.3_loan_amortization](student/session_2/2.3_loan_amortization.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_2/2.3_loan_amortization.ipynb) | Amortización de préstamos |
| 2.4 | [2.4_dcf_uncertainty](student/session_2/2.4_dcf_uncertainty.ipynb) · [Colab](https://colab.research.google.com/github/Ulysess824/Python-for-Finance/blob/main/python-finance-course/student/session_2/2.4_dcf_uncertainty.ipynb) | DCF con incertidumbre |
| 2.5 | [2.5_automated_report](student/session_2/2.5_automated_report/2.5_automated_report.ipynb) · [script](instructor/session_2/2.5_automated_report/report.py) | Informe HTML automatizado |

Las diapositivas están en [`slides/presentation.html`](slides/presentation.html) (ábrelas en el navegador, navega con ← →).

## Estructura

```
instructor/   notebooks con soluciones (fuente de verdad)
student/      generados desde instructor/, sin soluciones
common/       utils.py: descarga de datos, estilo de gráficos, funciones compartidas
data/sample/  CSV de respaldo si falla la API en vivo
tools/        make_student_notebooks.py, refresh_sample_data.py
slides/       presentation.html
```

## Instalación local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

En Colab, añade al inicio de cada notebook: `!pip install -q yfinance arch` y clona el repositorio para que `common/` esté disponible.

> **Nota:** los enlaces de Colab asumen la ruta `python-finance-course/` dentro del repositorio `Ulysess824/Python-for-Finance`, rama `main`. Ajústalos si mueves la carpeta.

## Flujo de trabajo del instructor

1. Edita **solo** `instructor/`. Marca las celdas de solución con el tag `solution`
   (Jupyter: *View → Cell Toolbar → Tags*; JupyterLab: panel *Property Inspector*).
2. Regenera los notebooks de alumnos:
   ```bash
   python tools/make_student_notebooks.py
   ```
3. Comprueba que `student/` está al día (útil en CI): `python tools/make_student_notebooks.py --check`
4. Si la API falla en clase, `common.download_prices` usa automáticamente `data/sample/`. Para refrescar las copias:
   `python tools/refresh_sample_data.py`
