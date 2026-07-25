from typing import Any, Dict

from backend.data_store import DataStore
from tools.base import ToolError, log_tool_call, validate_required


def create_incident(title: str, incident_type: str, severity: str, description: str, affected_ids: list[str], data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("create_incident", title=title, severity=severity)
    validate_required({"title": title, "incident_type": incident_type, "severity": severity, "description": description}, ["title", "incident_type", "severity", "description"])
    return {"id": "INC-NEW", "title": title, "incident_type": incident_type, "severity": severity, "description": description, "affected_ids": affected_ids, "status": "pending_confirmation"}


def incident_status(incident_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("incident_status", incident_id=incident_id)
    ds = data_store or DataStore()
    incident = ds.find_incident(incident_id)
    if not incident:
        raise ToolError(f"Incident {incident_id} was not found")
    return {"incident_id": incident_id, "status": incident.get("status"), "severity": incident.get("severity")}


def incident_summary(incident_id: str, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("incident_summary", incident_id=incident_id)
    ds = data_store or DataStore()
    incident = ds.find_incident(incident_id)
    if not incident:
        raise ToolError(f"Incident {incident_id} was not found")
    return {"incident_id": incident_id, "summary": f"{incident['title']} - {incident.get('severity')} impact"}


def recovery_plan(incident_id: str, strategy: str | None = None, data_store: DataStore | None = None) -> Dict[str, Any]:
    log_tool_call("recovery_plan", incident_id=incident_id, strategy=strategy)
    validate_required({"incident_id": incident_id}, ["incident_id"])
    ds = data_store or DataStore()
    incident = ds.find_incident(incident_id)
    if not incident:
        raise ToolError(f"Incident {incident_id} was not found")
    return {"incident_id": incident_id, "strategy": strategy or "split-shipments", "status": "pending_confirmation", "message": "Recovery plan drafted"}
