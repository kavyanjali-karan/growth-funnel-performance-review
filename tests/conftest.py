"""Shared fixtures for growth funnel tests."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
import pandas as pd

DATA_DIR = ROOT / "data" / "raw"

RAW_FILES = [
    "visitors.csv",
    "signups.csv",
    "trials.csv",
    "paid_customers.csv",
    "activated_feature.csv",
]


def _ensure_data() -> None:
    """Build the (gitignored, seeded) datasets on a fresh clone."""
    if all((DATA_DIR / name).exists() for name in RAW_FILES):
        return
    subprocess.run(
        [sys.executable, str(ROOT / "data" / "generate_data.py")],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


_ensure_data()


@pytest.fixture(scope="session")
def visitors():
    return pd.read_csv(DATA_DIR / "visitors.csv")


@pytest.fixture(scope="session")
def signups():
    return pd.read_csv(DATA_DIR / "signups.csv")


@pytest.fixture(scope="session")
def trials():
    return pd.read_csv(DATA_DIR / "trials.csv")


@pytest.fixture(scope="session")
def paid_customers():
    return pd.read_csv(DATA_DIR / "paid_customers.csv")


@pytest.fixture(scope="session")
def activated():
    return pd.read_csv(DATA_DIR / "activated_feature.csv")
