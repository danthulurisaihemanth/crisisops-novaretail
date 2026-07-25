from typing import Any, Dict, List

from backend.data_store import DataStore
from tools.base import ToolError, log_tool_call, validate_required


def supplier_lookup(supplier_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("supplier_lookup", supplier_id=supplier_id)
    validate_required({"supplier_id": supplier_id}, ["supplier_id"])
    ds = data_store or DataStore()
    supplier = ds.find_supplier(supplier_id)
    if not supplier:
        raise ToolError(f"Supplier {supplier_id} was not found")
    return {"supplier_id": supplier_id, "supplier": supplier}


def supplier_availability(supplier_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("supplier_availability", supplier_id=supplier_id)
    supplier = supplier_lookup(supplier_id, data_store)
    return {"supplier_id": supplier_id, "available": supplier["supplier"].get("status") == "active", "lead_time_days": supplier["supplier"].get("lead_time_days")}


def alternative_supplier(product_id: str, current_supplier_id: str | None = None, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("alternative_supplier", product_id=product_id, current_supplier_id=current_supplier_id)
    ds = data_store or DataStore()
    product = ds.find_product(product_id)
    if not product:
        raise ToolError(f"Product {product_id} was not found")
    suppliers = [s for s in ds.suppliers() if s.get("status") == "active" and product.get("category") in s.get("product_categories", [])]
    ranked = sorted(suppliers, key=lambda s: (s.get("rating", 0), s.get("lead_time_days", 99)), reverse=True)
    return {"product_id": product_id, "current_supplier_id": current_supplier_id, "alternatives": ranked[:5]}


def compare_suppliers(product_id: str, candidate_ids: List[str], data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("compare_suppliers", product_id=product_id, candidate_ids=candidate_ids)
    ds = data_store or DataStore()
    product = ds.find_product(product_id)
    if not product:
        raise ToolError(f"Product {product_id} was not found")
    suppliers = [ds.find_supplier(candidate_id) for candidate_id in candidate_ids if ds.find_supplier(candidate_id)]
    return {"product_id": product_id, "comparisons": suppliers, "recommended": suppliers[0]["id"] if suppliers else None}
