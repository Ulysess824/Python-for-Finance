"""Demo datasets generated on the fly (so the class never depends on external files)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def make_sales_files(folder, n_files: int = 50, seed: int = 7) -> list[Path]:
    """Create `n_files` messy monthly sales CSVs (one per branch) with deliberate errors:
    mixed date formats, duplicated rows, negative units, missing prices, inconsistent column names."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    products = {"Crédito libre": 1200, "Crédito vehículo": 2500, "Tarjeta": 300, "CDT": 5000, "Seguro": 150}
    paths = []
    for i in range(1, n_files + 1):
        n = int(rng.integers(40, 120))
        df = pd.DataFrame({
            "fecha": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 90, n), unit="D"),
            "producto": rng.choice(list(products), n),
            "unidades": rng.integers(1, 20, n),
        })
        df["precio"] = df["producto"].map(products) * rng.normal(1, 0.05, n)
        if rng.random() < 0.5:   # mixed date format
            df["fecha"] = df["fecha"].dt.strftime("%d/%m/%Y")
        else:
            df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
        if rng.random() < 0.4:   # duplicated rows
            df = pd.concat([df, df.sample(3, random_state=i)])
        if rng.random() < 0.3:   # negative units
            df.loc[df.sample(2, random_state=i).index[:1], "unidades"] = -5
        if rng.random() < 0.3:   # missing prices
            df.loc[df.sample(2, random_state=i + 1).index[:1], "precio"] = np.nan
        if rng.random() < 0.25:  # inconsistent headers
            df = df.rename(columns={"fecha": "Fecha", "producto": "Producto"})
        p = folder / f"sucursal_{i:02d}.csv"
        df.to_csv(p, index=False)
        paths.append(p)
    return paths
