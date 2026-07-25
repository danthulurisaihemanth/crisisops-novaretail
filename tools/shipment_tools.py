from typing import Any, Dict

from backend.data_store import DataStore
from tools.base import ToolError, log_tool_call, validate_required


def track_shipment(shipment_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("track_shipment", shipment_id=shipment_id)
    if not shipment_id:
        raise ToolError("A shipment id is required")
    ds = data_store or DataStore()
    shipment = ds.find_shipment(shipment_id)
    if not shipment:
        raise ToolError(f"Shipment {shipment_id} was not found")
    return {"shipment_id": shipment_id, "status": shipment["status"], "route": shipment.get("route_id"), "eta": shipment.get("eta")}


def shipment_status(shipment_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("shipment_status", shipment_id=shipment_id)
    shipment = (data_store or DataStore()).find_shipment(shipment_id)
    if not shipment:
        raise ToolError(f"Shipment {shipment_id} was not found")
    return {"shipment_id": shipment_id, "status": shipment["status"], "delay_hours": shipment.get("delay_hours", 0)}


def shipment_delay(shipment_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("shipment_delay", shipment_id=shipment_id)
    shipment = (data_store or DataStore()).find_shipment(shipment_id)
    if not shipment:
        raise ToolError(f"Shipment {shipment_id} was not found")
    return {"shipment_id": shipment_id, "delay_hours": shipment.get("delay_hours", 0), "is_delayed": shipment.get("delay_hours", 0) > 12}


def route_status(route_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("route_status", route_id=route_id)
    ds = data_store or DataStore()
    for route in ds.routes():
        if route["id"] == route_id:
            return {"route_id": route_id, "status": route["status"], "cost": route.get("cost_per_km"), "eta_hours": route.get("eta_hours")}
    raise ToolError(f"Route {route_id} was not found")


def reroute_shipment(shipment_id: str, route_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("reroute_shipment", shipment_id=shipment_id, route_id=route_id)
    validate_required({"shipment_id": shipment_id, "route_id": route_id}, ["shipment_id", "route_id"])
    ds = data_store or DataStore()
    shipment = ds.find_shipment(shipment_id)
    if not shipment:
        raise ToolError(f"Shipment {shipment_id} was not found")
    return {"shipment_id": shipment_id, "rerouted_to": route_id, "message": "Reroute requested but pending confirmation"}


def affected_orders(shipment_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("affected_orders", shipment_id=shipment_id)
    ds = data_store or DataStore()
    impacted = [order for order in ds.orders() if order.get("shipment_id") == shipment_id]
    return {"shipment_id": shipment_id, "affected_orders": impacted[:10], "count": len(impacted)}


def customer_notification(order_id: str, message: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("customer_notification", order_id=order_id, message=message)
    validate_required({"order_id": order_id, "message": message}, ["order_id", "message"])
    ds = data_store or DataStore()
    order = ds.find_order(order_id)
    if not order:
        raise ToolError(f"Order {order_id} was not found")
    return {"order_id": order_id, "message": message, "status": "pending_confirmation"}
