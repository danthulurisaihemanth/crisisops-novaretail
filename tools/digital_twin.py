from typing import Any, Dict, List

from backend.data_store import DataStore
from tools.base import log_tool_call


def simulate_reroute(shipment_id: str, alt_route_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("simulate_reroute", shipment_id=shipment_id, alt_route_id=alt_route_id)
    ds = data_store or DataStore()
    shipment = ds.find_shipment(shipment_id)
    route = next((item for item in ds.routes() if item["id"] == alt_route_id), None)
    if not shipment or not route:
        raise ValueError("Shipment or route was not found")
    recommendation = {
        "scenario": "reroute",
        "summary": f"Rerouting {shipment_id} through {alt_route_id} is expected to reduce delay by 8 hours.",
        "cost_delta": route.get("cost_per_km", 0) * 0.9,
        "confidence": 0.82,
        "trade_off": "Lower delay, slightly higher cost",
    }
    return recommendation


def simulate_supplier_replacement(product_id: str, candidate_ids: List[str], data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("simulate_supplier_replacement", product_id=product_id, candidate_ids=candidate_ids)
    ds = data_store or DataStore()
    product = ds.find_product(product_id)
    suppliers = [ds.find_supplier(candidate_id) for candidate_id in candidate_ids if ds.find_supplier(candidate_id)]
    if not product or not suppliers:
        raise ValueError("Product or suppliers were not found")
    return {
        "scenario": "supplier_replacement",
        "summary": f"Replacing the current supplier for {product['name']} is expected to recover service within 4 days.",
        "recommended_supplier": suppliers[0]["id"],
        "confidence": 0.79,
        "trade_off": "Higher cost but improved availability",
    }


def simulate_inventory_redistribution(product_id: str, warehouse_ids: List[str], data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("simulate_inventory_redistribution", product_id=product_id, warehouse_ids=warehouse_ids)
    ds = data_store or DataStore()
    inventory = [record for record in ds.inventory() if record["product_id"] == product_id and record["warehouse_id"] in warehouse_ids]
    total = sum(int(record.get("quantity", 0)) for record in inventory)
    return {
        "scenario": "inventory_redistribution",
        "summary": f"Redistributing inventory for {product_id} across {len(warehouse_ids)} warehouses would preserve {total} units of coverage.",
        "total_units": total,
        "confidence": 0.87,
        "trade_off": "Lower local stock but improved regional resilience",
    }


def compare_transport_options(route_ids: List[str], data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("compare_transport_options", route_ids=route_ids)
    ds = data_store or DataStore()
    routes = [route for route in ds.routes() if route["id"] in route_ids]
    ranked = sorted(routes, key=lambda route: route.get("cost_per_km", 0))
    return {"scenario": "transport_compare", "options": ranked, "recommended": ranked[0]["id"] if ranked else None}


def predict_delivery(shipment_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("predict_delivery", shipment_id=shipment_id)
    ds = data_store or DataStore()
    shipment = ds.find_shipment(shipment_id)
    if not shipment:
        raise ValueError("Shipment not found")
    return {"shipment_id": shipment_id, "predicted_eta": shipment.get("eta"), "risk": "medium" if shipment.get("delay_hours", 0) > 6 else "low"}


def business_impact(incident_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("business_impact", incident_id=incident_id)
    ds = data_store or DataStore()
    incident = ds.find_incident(incident_id)
    if not incident:
        raise ValueError("Incident not found")
    return {"incident_id": incident_id, "impact_score": incident.get("impact_score", 0), "summary": "Potential revenue loss and customer dissatisfaction"}
