# Python for Finance 📈
### Quantitative Analysis, Asset Pricing & Portfolio Management

Este repositorio constituye un ecosistema de herramientas cuantitativas desarrolladas en **Python**, orientadas a la implementación de teorías financieras clásicas y modernas. El objetivo central es transformar modelos teóricos en aplicaciones prácticas para la toma de decisiones basada en datos.

---

## 🗂️ Estructura del repositorio

```
Python-for-Finance/
├── 01_Portfolio_Management/     # Gestión y optimización de carteras
│   ├── Retorno y Volatilidad de un Portafolio.ipynb
│   └── Random Portfolios/
│       ├── Obteniendo ETFs válido.ipynb
│       ├── Random Portfolios Vs Actively ETFs.ipynb
│       ├── etfs_details_type_fund_flow.csv
│       ├── portafolios_aleatorios.csv
│       └── prices_etf.csv
├── 02_Asset_Pricing/             # Valoración de activos y modelos de equilibrio
│   └── CAPM.ipynb
├── 03_Risk_Analysis/             # Riesgo, volatilidad y ratios de rendimiento
│   ├── Midiendo la Volatilidad.ipynb
│   └── Risk-Return Measures.ipynb
├── 04_Technical_Analysis/        # Indicadores técnicos y señales de trading
│   └── Indicadores Técnicos.ipynb
├── 05_Market_Studies/            # Econometría y comportamiento de mercados
│   ├── Estacionaridad de Indices bursatiles.ipynb
│   └── IBEX 35 y Euribor.ipynb
└── Data/                         # Datos auxiliares compartidos entre notebooks
    └── resultado.csv
```

---

## 🚀 Áreas de Enfoque (Core Pillars)

### 1. [Portfolio Management](./01_Portfolio_Management/)
*Implementación de estrategias de inversión y simulación.*
- **[Retorno y Volatilidad de un Portafolio](./01_Portfolio_Management/Retorno%20y%20Volatilidad%20de%20un%20Portafolio.ipynb):** Cálculo de retornos esperados y varianzas de una cartera bajo el enfoque de Markowitz.
- **[Random Portfolios](./01_Portfolio_Management/Random%20Portfolios/):** Generación de carteras aleatorias y comparación de su desempeño frente a ETFs de gestión activa.

### 2. [Asset Pricing](./02_Asset_Pricing/)
*Modelización teórica del valor y equilibrio de mercado.*
- **[CAPM](./02_Asset_Pricing/CAPM.ipynb):** Modelo de Valoración de Activos de Capital — estimación de Beta mediante regresión OLS y cálculo de rentabilidades exigidas.

### 3. [Risk Analysis](./03_Risk_Analysis/)
*Métricas avanzadas para la gestión de la exposición al riesgo.*
- **[Midiendo la Volatilidad](./03_Risk_Analysis/Midiendo%20la%20Volatilidad.ipynb):** Cálculo de retornos simples y logarítmicos, y estimación de volatilidad histórica.
- **[Risk-Return Measures](./03_Risk_Analysis/Risk-Return%20Measures.ipynb):** Ratios de rendimiento ajustado al riesgo (Sharpe, Sortino, entre otros).

### 4. [Technical Analysis](./04_Technical_Analysis/)
*Algoritmos de trading y señales de mercado.*
- **[Indicadores Técnicos](./04_Technical_Analysis/Indicadores%20T%C3%A9cnicos.ipynb):** Construcción de indicadores como medias móviles, RSI y MACD aplicados a series de precios.

### 5. [Market Studies](./05_Market_Studies/)
*Estudio del comportamiento estadístico de los mercados.*
- **[Estacionaridad de Índices Bursátiles](./05_Market_Studies/Estacionaridad%20de%20Indices%20bursatiles.ipynb):** Pruebas de raíces unitarias (ADF/PP) para análisis de series temporales.
- **[IBEX 35 y Euribor](./05_Market_Studies/IBEX%2035%20y%20Euribor.ipynb):** Análisis exploratorio y correlación entre el IBEX 35 y los tipos de interés (Euribor).

### 📁 [Data](./Data/)
*Conjuntos de datos auxiliares* utilizados como insumo o resultado intermedio de los notebooks (p. ej. `resultado.csv`).

---

## 🛠️ Stack Tecnológico
- **Análisis de Datos:** `Pandas`, `NumPy`.
- **Visualización:** `Matplotlib`, `Plotly` (Interacción dinámica).
- **Estadística/Econometría:** `SciPy`, `statsmodels`.
- **Data Sourcing:** APIs financieras (Yahoo Finance, etc.).

---

**Autor:** [Ulysess824](https://github.com/Ulysess824)
*Finanzas Cuantitativas | Análisis de Datos | Inversión Inteligente*
