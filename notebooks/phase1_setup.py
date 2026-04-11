# ============================================================
# PHASE 1 — Environment Setup & Verification
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import os
import warnings

warnings.filterwarnings('ignore')

# Create folder structure (safe to run multiple times)
for folder in ['data', 'charts', 'notebooks']:
    os.makedirs(folder, exist_ok=True)

print("=" * 50)
print("PHASE 1 — ENVIRONMENT CHECK")
print("=" * 50)
print(f"  pandas     : {pd.__version__}")
print(f"  numpy      : {np.__version__}")
print(f"  matplotlib : {matplotlib.__version__}")
print(f"  seaborn    : {sns.__version__}")
print(f"  plotly     : {plotly.__version__}")
print()
print("  Folders created: data/, charts/, notebooks/")
print()
print("  All good! Phase 1 complete. Move to Phase 2.")
print("=" * 50)
