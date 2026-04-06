"""
state.py

Shared application state — loaded once at startup.

All modules that need the raw dataset or initial enriched rows
import from here instead of re-loading independently.
"""

from __future__ import annotations

from typing import Any

from config import DEFAULT_SELECTED_DATE
from aggregations import enrich_dashboard_rows
from data_loader import load_dashboard_data, load_unmatched_vendor_rows
from logger import setup_logger

logger = setup_logger(__name__)

# ---------------------------------------------------------------------------
# Load once at process start — used by layout and callbacks
# ---------------------------------------------------------------------------
RAW_DF = load_dashboard_data()
logger.info("Dashboard dataset loaded at startup with %s rows", len(RAW_DF))

UNMATCHED_VENDOR_ROWS: list[dict] = load_unmatched_vendor_rows()
logger.info("Unmatched vendor pool loaded: %s rows", len(UNMATCHED_VENDOR_ROWS))

initial_rows: list[dict[str, Any]] = enrich_dashboard_rows(RAW_DF, DEFAULT_SELECTED_DATE)


# ---------------------------------------------------------------------------
# Shared utility
# ---------------------------------------------------------------------------
def get_city_options(enriched_rows: list[dict[str, Any]]) -> list[str]:
    """Return sorted list of regions from LPG rows only."""
    lpg = [r for r in enriched_rows if not r.get("is_alternative", False)]
    cities = {str(row["region"]).strip() for row in lpg if row.get("region")}
    return sorted(cities)
