from typing import Any, Dict

from backend.data_store import DataStore
from tools.base import ToolError, log_tool_call, validate_required


def inventory_lookup(product_id: str, warehouse_id: str | None = None, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("inventory_lookup", product_id=product_id, warehouse_id=warehouse_id)
    validate_required({"product_id": product_id}, ["product_id"])
    ds = data_store or DataStore()
    matches = [record for record in ds.inventory() if record["product_id"] == product_id and (not warehouse_id or record["warehouse_id"] == warehouse_id)]
    if not matches:
        raise ToolError(f"No inventory record found for product {product_id}")
    return {"product_id": product_id, "warehouse_id": warehouse_id, "records": matches}


def warehouse_stock(warehouse_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("warehouse_stock", warehouse_id=warehouse_id)
    validate_required({"warehouse_id": warehouse_id}, ["warehouse_id"])
    ds = data_store or DataStore()
    matches = [record for record in ds.inventory() if record["warehouse_id"] == warehouse_id]
    return {"warehouse_id": warehouse_id, "records": matches, "count": len(matches)}


def inventory_shortage(product_id: str | None = None, threshold: float = 0.2, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("inventory_shortage", product_id=product_id, threshold=threshold)
    ds = data_store or DataStore()
    records = ds.inventory()
    if product_id:
        records = [record for record in records if record["product_id"] == product_id]
    shortages = [record for record in records if record.get("quantity", 0) <= int(record.get("reorder_level", 0) * (1 + threshold))]
    return {"product_id": product_id, "threshold": threshold, "shortages": shortages[:20], "count": len(shortages)}
