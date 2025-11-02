# models/garment.py
"""
Garment model helpers for pandas + SQLite.
Compatible with routes/outfits.py (list_garments + ID lookups).
"""

from __future__ import annotations
import uuid
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String

DB_URL = "sqlite:///database.db"
engine = create_engine(DB_URL, future=True)

# Ensure table exists
metadata = MetaData()
garments_table = Table(
    "garments", metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("category", String),
    Column("color", String),
)
metadata.create_all(engine)

COLUMNS = ["id", "name", "category", "color"]

def _empty_df() -> pd.DataFrame:
    return pd.DataFrame(columns=COLUMNS)

def _load() -> pd.DataFrame:
    try:
        return pd.read_sql_table("garments", con=engine)
    except Exception:
        return _empty_df()

def _save(df: pd.DataFrame) -> None:
    df.to_sql("garments", con=engine, if_exists="replace", index=False)

# -------- Public API --------

def list_garments() -> list[dict]:
    """Return all garments as list[dict] with keys id, name, category, color."""
    return _load().to_dict(orient="records")

def get_garments_by_ids(ids: list[str]) -> list[dict]:
    """Return garments whose id is in ids (order preserved as given)."""
    if not ids:
        return []
    df = _load()
    subset = df[df["id"].isin(set(ids))]
    # preserve request order
    order = {gid: i for i, gid in enumerate(ids)}
    subset = subset.assign(_o=subset["id"].map(order)).sort_values("_o").drop(columns="_o")
    return subset.to_dict(orient="records")

def add_garment(name: str, category: str, color: str) -> dict:
    df = _load()
    row = {"id": str(uuid.uuid4()), "name": name, "category": category, "color": color}
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    _save(df)
    return row

def update_garment(garment_id: str, updates: dict) -> dict:
    df = _load()
    idx = df.index[df["id"] == garment_id]
    if not len(idx):
        raise KeyError(f"Garment '{garment_id}' not found")
    i = idx[0]
    for k, v in updates.items():
        if k in COLUMNS and k != "id":
            df.at[i, k] = v
    _save(df)
    return df.loc[i].to_dict()

def remove_garment(garment_id: str) -> None:
    df = _load()
    df = df[df["id"] != garment_id].reset_index(drop=True)
    _save(df)

# Quick local test
if __name__ == "__main__":
    print("Adding sample items...")
    g1 = add_garment("T-shirt", "Top", "Blue")
    g2 = add_garment("Jeans", "Bottom", "Black")
    print("All:", list_garments())
    print("By IDs:", get_garments_by_ids([g2["id"], g1["id"]]))
