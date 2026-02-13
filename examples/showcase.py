# %% [markdown]

# # dfview showcase
# Demonstrates the main features of dfview:
# sorting, Excel-style filter dropdowns, column resizing, and cell expansion.

# %%

import numpy as np
import pandas as pd

import dfview

# %%

rng = np.random.default_rng(42)

n = 60
cities = ["Ljubljana", "Maribor", "Celje", "Koper", "Kranj", "Novo Mesto"]
departments = ["Engineering", "Sales", "Marketing", "HR", "Finance"]
levels = ["Junior", "Mid", "Senior", "Lead"]

df = pd.DataFrame(
    {
        "Name": [f"Employee_{i:03d}" for i in range(n)],
        "City": rng.choice(cities, n),
        "Department": rng.choice(departments, n),
        "Level": rng.choice(levels, n),
        "Salary": (rng.normal(55000, 12000, n)).astype(int),
        "Years": rng.integers(0, 25, n),
        "Rating": (rng.uniform(2.5, 5.0, n)).round(1),
        "Notes": rng.choice(
            [
                "Exceeds expectations",
                "Meets expectations",
                "On track for promotion",
                "New hire — probation period",
                "Transferred from another branch recently",
            ],
            n,
        ),
    }
)

dfview.show(df)



# %%

