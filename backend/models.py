from typing import Any, Dict, List, Optional

Supplier = Dict[str, Any]
Warehouse = Dict[str, Any]
Product = Dict[str, Any]
InventoryRecord = Dict[str, Any]
Shipment = Dict[str, Any]
Customer = Dict[str, Any]
Order = Dict[str, Any]
Incident = Dict[str, Any]
Route = Dict[str, Any]
Partner = Dict[str, Any]
RecoveryPlan = Dict[str, Any]

def ensure_id(item: Dict[str, Any], prefix: str) -> Dict[str, Any]:
    if "id" not in item:
        item["id"] = f"{prefix}-{len(item)}"
    return item
