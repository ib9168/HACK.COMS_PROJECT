# models/garments.py
"""
Garment data model and utility functions.
Handles creation, retrieval, update, and deletion of garments
stored in an SQLite database, using pandas for manipulation.
"""

import uuid
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String

# ---- Database setup ----
DB_URL = "sqlite:///database.db"
engine = create_engine(DB_URL, future=True)

# ---- Define and ensure table exists ----
metadata = MetaData()
garments_table = Table(
    "garments", metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("category", String),
    Column("color", String),
)
metadata.create_all(engine)


# ---- Utility functions ----
def load_table(table_name: str = "garments") -> pd.DataFrame:
    """Read a database table into a pandas DataFrame.
    Returns an empty DataFrame if the table is missing.
    """
    try:
        return pd.read_sql_table(table_name, con=engine)
    except Exception:
        return pd.DataFrame(columns=["id", "name", "category", "color"])


def save_table(df: pd.DataFrame, table_name: str = "garments") -> None:
    """Write a DataFrame back to the given table, replacing existing data."""
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)


# ---- CRUD operations ----
def add_garment(name: str, category: str, color: str) -> dict:
    """Add a new garment and return its record."""
    df = load_table()
    new_row = {
        "id": str(uuid.uuid4()),
        "name": name,
        "category": category,
        "color": color,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_table(df)
    return new_row


def remove_garment(garment_id: str) -> None:
    """Remove a garment by its ID."""
    df = load_table()
    df = df[df["id"] != garment_id].reset_index(drop=True)
    save_table(df)


def update_garment(garment_id: str, updates: dict) -> dict:
    """Update one garment’s fields and return the updated record."""
    df = load_table()
    idx = df.index[df["id"] == garment_id]
    if not len(idx):
        raise KeyError(f"Garment '{garment_id}' not found")

    for key, val in updates.items():
        if key in df.columns:
            df.at[idx[0], key] = val

    save_table(df)
    return df.loc[idx[0]].to_dict()


def list_garments() -> list[dict]:
    """Return all garments as a list of dictionaries."""
    df = load_table()
    return df.to_dict(orient="records")


# ---- Local test ----
if __name__ == "__main__":
    print("Adding garments...")
    g1 = add_garment("T-shirt", "Top", "Blue")
    g2 = add_garment("Jeans", "Bottom", "Black")
    print("Added:", g1)
    print("Added:", g2)

    print("\nAll garments:")
    print(list_garments())

    print("\nUpdating first garment...")
    updated = update_garment(g1["id"], {"color": "Green"})
    print("Updated:", updated)

    print("\nRemoving first garment...")
    remove_garment(g1["id"])
    print("Remaining garments:")
    print(list_garments())
