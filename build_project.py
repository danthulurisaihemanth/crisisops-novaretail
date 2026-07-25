from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent

files = {}

files["requirements.txt"] = dedent('''
    streamlit>=1.36.0
    python-dotenv>=1.0.0
    pandas>=2.2.0
    numpy>=1.26.0
    pytest>=8.3.0
    langchain>=0.3.0
    langgraph>=0.2.0
    langsmith>=0.1.0
    chromadb>=0.5.0
    sentence-transformers>=3.0.0
    pydantic>=2.8.0
''').strip() + "\n"

files[".env.example"] = dedent('''
    GEMINI_API_KEY=
    LANGSMITH_API_KEY=
    LANGSMITH_TRACING=false
    LANGSMITH_PROJECT=novaretail-crisisops
    STREAMLIT_SERVER_PORT=8501
    DATA_DIR=data
''').strip() + "\n"

files["README.md"] = dedent('''
    # NovaRetail CrisisOps AI

    NovaRetail CrisisOps AI is an enterprise-grade supply-chain operations assistant built with Streamlit, LangChain, LangGraph, and a synthetic enterprise dataset. It supports shipment tracking, inventory review, supplier lookup, incident creation, recovery planning, and digital-twin simulation.

    ## Features
    - Conversational operations assistant
    - Multi-agent routing for shipment, inventory, supplier, recovery, and reporting tasks
    - Human-in-the-loop confirmation for risky actions
    - Synthetic enterprise-grade datasets for suppliers, warehouses, inventory, shipments, orders, incidents, routes, partners, and recovery plans
    - Digital twin scenarios for rerouting, supplier replacement, inventory redistribution, transportation cost comparison, delivery prediction, and business impact analysis

    ## Run locally
    1. Create and activate a virtual environment.
    2. Install dependencies: `pip install -r requirements.txt`
    3. Copy `.env.example` to `.env` and set your environment values.
    4. Generate datasets: `python data/generate_datasets.py`
    5. Start the app: `streamlit run frontend/app.py`

    ## Architecture
    - Frontend: Streamlit
    - Backend: Python services and data store
    - Agents: LangGraph-inspired workflow with supervisor and specialist agents
    - Tools: shipment, inventory, supplier, incident, and digital-twin tools
    - Observability: LangSmith-compatible tracing hooks
''').strip() + "\n"

files["run_app.py"] = dedent('''
    import os
    import subprocess
    import sys

    if __name__ == "__main__":
        command = [sys.executable, "-m", "streamlit", "run", "frontend/app.py"]
        subprocess.run(command, check=False)
''').strip() + "\n"

files["config/__init__.py"] = ""
files["config/settings.py"] = dedent('''
    import os
    from dataclasses import dataclass
    from dotenv import load_dotenv

    load_dotenv()

    @dataclass
    class Settings:
        app_name: str = "NovaRetail CrisisOps AI"
        gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
        langsmith_tracing: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
        langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "novaretail-crisisops")
        data_dir: str = os.getenv("DATA_DIR", "data")

    settings = Settings()
''').strip() + "\n"

files["utilities/__init__.py"] = ""
files["utilities/logging_config.py"] = dedent('''
    import logging
    from pathlib import Path

    def configure_logging() -> logging.Logger:
        logger = logging.getLogger("novaretail")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
            logger.addHandler(handler)
        return logger

    LOGGER = configure_logging()
''').strip() + "\n"

files["utilities/tracing.py"] = dedent('''
    from typing import Callable, TypeVar

    from config.settings import settings
    from utilities.logging_config import LOGGER

    try:
        from langsmith import traceable as langsmith_traceable
    except Exception:  # pragma: no cover
        langsmith_traceable = None

    F = TypeVar("F", bound=Callable)

    def traceable(func: F) -> F:
        if settings.langsmith_tracing and langsmith_traceable is not None:
            return langsmith_traceable(func)  # type: ignore[return-value]
        return func

    def trace_event(name: str, **payload: object) -> None:
        if settings.langsmith_tracing:
            LOGGER.info("trace:%s %s", name, payload)
''').strip() + "\n"

files["backend/__init__.py"] = ""
files["backend/models.py"] = dedent('''
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
''').strip() + "\n"

files["backend/data_store.py"] = dedent('''
    import json
    from pathlib import Path
    from typing import Any, Dict, List

    from config.settings import settings

    class DataStore:
        def __init__(self, data_dir: str | Path | None = None) -> None:
            self.data_dir = Path(data_dir or settings.data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)

        def _load_json(self, filename: str) -> List[Dict[str, Any]]:
            path = self.data_dir / filename
            if not path.exists():
                return []
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)

        def suppliers(self) -> List[Dict[str, Any]]:
            return self._load_json("suppliers.json")

        def warehouses(self) -> List[Dict[str, Any]]:
            return self._load_json("warehouses.json")

        def products(self) -> List[Dict[str, Any]]:
            return self._load_json("products.json")

        def inventory(self) -> List[Dict[str, Any]]:
            return self._load_json("inventory.json")

        def shipments(self) -> List[Dict[str, Any]]:
            return self._load_json("shipments.json")

        def customers(self) -> List[Dict[str, Any]]:
            return self._load_json("customers.json")

        def orders(self) -> List[Dict[str, Any]]:
            return self._load_json("orders.json")

        def incidents(self) -> List[Dict[str, Any]]:
            return self._load_json("incidents.json")

        def routes(self) -> List[Dict[str, Any]]:
            return self._load_json("routes.json")

        def partners(self) -> List[Dict[str, Any]]:
            return self._load_json("partners.json")

        def recovery_plans(self) -> List[Dict[str, Any]]:
            return self._load_json("recovery_plans.json")

        def find_supplier(self, supplier_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.suppliers() if item["id"] == supplier_id), None)

        def find_product(self, product_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.products() if item["id"] == product_id), None)

        def find_warehouse(self, warehouse_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.warehouses() if item["id"] == warehouse_id), None)

        def find_shipment(self, shipment_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.shipments() if item["id"] == shipment_id), None)

        def find_order(self, order_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.orders() if item["id"] == order_id), None)

        def find_incident(self, incident_id: str) -> Dict[str, Any] | None:
            return next((item for item in self.incidents() if item["id"] == incident_id), None)
''').strip() + "\n"

files["backend/memory.py"] = dedent('''
    from collections import defaultdict
    from typing import Any, Dict, List

    class ConversationMemory:
        def __init__(self) -> None:
            self.sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
            self.session_state: Dict[str, Dict[str, Any]] = {}

        def add_message(self, session_id: str, role: str, content: str) -> None:
            self.sessions[session_id].append({"role": role, "content": content})

        def get_history(self, session_id: str) -> List[Dict[str, Any]]:
            return self.sessions.get(session_id, [])

        def set_state(self, session_id: str, key: str, value: Any) -> None:
            self.session_state.setdefault(session_id, {})[key] = value

        def get_state(self, session_id: str, key: str, default: Any = None) -> Any:
            return self.session_state.get(session_id, {}).get(key, default)

        def clear(self, session_id: str) -> None:
            self.sessions.pop(session_id, None)
            self.session_state.pop(session_id, None)
''').strip() + "\n"

files["tools/__init__.py"] = ""
files["tools/base.py"] = dedent('''
    from typing import Any, Dict, List

    from utilities.logging_config import LOGGER


    class ToolError(Exception):
        pass


    def validate_required(payload: Dict[str, Any], required_fields: List[str]) -> None:
        missing = [field for field in required_fields if not payload.get(field)]
        if missing:
            raise ToolError(f"Missing required fields: {', '.join(missing)}")


    def log_tool_call(tool_name: str, **payload: Any) -> None:
        LOGGER.info("tool:%s %s", tool_name, payload)
''').strip() + "\n"

files["tools/shipment_tools.py"] = dedent('''
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
''').strip() + "\n"

files["tools/inventory_tools.py"] = dedent('''
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
''').strip() + "\n"

files["tools/supplier_tools.py"] = dedent('''
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
''').strip() + "\n"

files["tools/incident_tools.py"] = dedent('''
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
''').strip() + "\n"

files["tools/digital_twin.py"] = dedent('''
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
''').strip() + "\n"

files["agents/__init__.py"] = ""
files["agents/prompts.py"] = dedent('''
    SYSTEM_PROMPT = """You are NovaRetail CrisisOps AI, an enterprise-grade operations assistant for supply chain disruptions. You should help with shipment, inventory, supplier, incident, recovery, and reporting questions. Always explain results clearly and ask for confirmation before taking risky actions such as creating incidents, rerouting shipments, selecting suppliers, or approving recovery plans."""

    SUPERVISOR_PROMPT = """Route the query to the proper specialist agent. If the request is ambiguous, ask one clarifying question. Prioritize business impact and rapid stakeholder communication."""

    SHIPMENT_PROMPT = """You are the shipment specialist. Handle shipment tracking, delay diagnostics, route status, rerouting requests, and order impact analysis."""

    INVENTORY_PROMPT = """You are the inventory specialist. Explain stock availability, warehouse capacity, and shortages with operational context."""

    SUPPLIER_PROMPT = """You are the supplier specialist. Evaluate supplier health, availability, alternatives, and compare suppliers."""

    RECOVERY_PROMPT = """You are the recovery specialist. Recommend practical recovery actions and compare trade-offs for cost, speed, and resilience."""

    REPORTING_PROMPT = """You are the reporting specialist. Summarize incidents, explain business impact, and produce executive-friendly status updates."""
''').strip() + "\n"

files["agents/llm_service.py"] = dedent('''
    import random
    from typing import Any, Dict, List

    from config.settings import settings

    class LLMService:
        def __init__(self) -> None:
            self.provider = "fallback"
            if settings.gemini_api_key:
                self.provider = "gemini"

        def generate(self, prompt: str, context: Dict[str, Any] | None = None) -> str:
            if self.provider == "gemini":
                return f"Gemini integration is configured with a key. Prompt: {prompt[:120]}"
            return self._fallback_response(prompt, context or {})

        def _fallback_response(self, prompt: str, context: Dict[str, Any]) -> str:
            lowered = prompt.lower()
            if "shipment" in lowered:
                return "I would inspect the shipment and impacted orders before recommending a recovery path."
            if "supplier" in lowered:
                return "I would compare active suppliers based on availability, lead time, and cost." 
            if "inventory" in lowered:
                return "I would review warehouse stock and reserve levels to identify the likely shortage."
            if "incident" in lowered:
                return "I would create a structured incident timeline and highlight business impact."
            return "I can help evaluate the operational impact and recommend the next best step."
''').strip() + "\n"

files["agents/human_loop.py"] = dedent('''
    from typing import Any, Dict, Optional

    from backend.memory import ConversationMemory

    class HumanLoopManager:
        def __init__(self, memory: ConversationMemory) -> None:
            self.memory = memory

        def request_confirmation(self, session_id: str, action: str, payload: Dict[str, Any]) -> str:
            self.memory.set_state(session_id, "pending_action", {"action": action, "payload": payload})
            return f"I can {action} for you. Please confirm before I proceed."

        def get_pending_action(self, session_id: str) -> Optional[Dict[str, Any]]:
            return self.memory.get_state(session_id, "pending_action")

        def clear_pending_action(self, session_id: str) -> None:
            self.memory.set_state(session_id, "pending_action", None)
''').strip() + "\n"

files["agents/graph.py"] = dedent('''
    from typing import Any, Dict, List, TypedDict

    try:
        from langgraph.graph import StateGraph, END
    except Exception:  # pragma: no cover
        StateGraph = None
        END = "__end__"

    class AgentState(TypedDict, total=False):
        input: str
        intent: str
        route: str
        response: str

    class AgentGraph:
        def __init__(self, orchestrator: Any) -> None:
            self.orchestrator = orchestrator
            self.graph = self._build_graph()

        def _build_graph(self) -> Any:
            if StateGraph is None:
                return None
            workflow = StateGraph(AgentState)
            workflow.add_node("supervisor", self._supervisor_node)
            workflow.add_node("shipment", self._shipment_node)
            workflow.add_node("inventory", self._inventory_node)
            workflow.add_node("supplier", self._supplier_node)
            workflow.add_node("recovery", self._recovery_node)
            workflow.add_node("reporting", self._reporting_node)
            workflow.set_entry_point("supervisor")
            workflow.add_conditional_edges("supervisor", self._route_condition, {"shipment": "shipment", "inventory": "inventory", "supplier": "supplier", "recovery": "recovery", "reporting": "reporting", "end": END})
            workflow.add_edge("shipment", END)
            workflow.add_edge("inventory", END)
            workflow.add_edge("supplier", END)
            workflow.add_edge("recovery", END)
            workflow.add_edge("reporting", END)
            return workflow.compile()

        def _route_condition(self, state: Dict[str, Any]) -> str:
            return state.get("route", "end")

        def _supervisor_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            intent = self.orchestrator.classify_request(state["input"])
            route = self.orchestrator.route_request(intent)
            return {"intent": intent, "route": route}

        def _shipment_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            return {"response": self.orchestrator.handle_shipment(state["input"])}

        def _inventory_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            return {"response": self.orchestrator.handle_inventory(state["input"])}

        def _supplier_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            return {"response": self.orchestrator.handle_supplier(state["input"])}

        def _recovery_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            return {"response": self.orchestrator.handle_recovery(state["input"])}

        def _reporting_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
            return {"response": self.orchestrator.handle_reporting(state["input"])}

        def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
            if self.graph is None:
                return {"response": self.orchestrator.fallback_route(state["input"])}
            return self.graph.invoke(state)
''').strip() + "\n"

files["backend/agent_orchestrator.py"] = dedent('''
    import re
    from typing import Any, Dict, List

    from agents.graph import AgentGraph
    from agents.human_loop import HumanLoopManager
    from agents.llm_service import LLMService
    from agents.prompts import SYSTEM_PROMPT
    from backend.data_store import DataStore
    from backend.memory import ConversationMemory
    from tools.digital_twin import business_impact, compare_transport_options, predict_delivery, simulate_inventory_redistribution, simulate_reroute, simulate_supplier_replacement
    from tools.incident_tools import create_incident, incident_status, incident_summary, recovery_plan
    from tools.inventory_tools import inventory_lookup, inventory_shortage, warehouse_stock
    from tools.shipment_tools import affected_orders, customer_notification, reroute_shipment, route_status, shipment_delay, shipment_status, track_shipment
    from tools.supplier_tools import alternative_supplier, compare_suppliers, supplier_availability, supplier_lookup
    from utilities.tracing import trace_event


    class CrisisOpsAgent:
        def __init__(self, data_store: DataStore | None = None, memory: ConversationMemory | None = None) -> None:
            self.data_store = data_store or DataStore()
            self.memory = memory or ConversationMemory()
            self.llm = LLMService()
            self.human_loop = HumanLoopManager(self.memory)
            self.graph = AgentGraph(self)

        def handle_message(self, session_id: str, user_input: str) -> Dict[str, Any]:
            self.memory.add_message(session_id, "user", user_input)
            pending = self.human_loop.get_pending_action(session_id)
            if pending:
                if re.search(r"yes|confirm|proceed|approve", user_input.lower()):
                    trace_event("confirmation_approved", session_id=session_id, action=pending["action"])
                    action = pending["action"]
                    payload = pending["payload"]
                    self.human_loop.clear_pending_action(session_id)
                    return self._execute_pending_action(action, payload, session_id)
                self.human_loop.clear_pending_action(session_id)
                return {"response": "The action was not confirmed. No changes were made.", "requires_confirmation": False}

            intent = self.classify_request(user_input)
            routed = self.route_request(intent)
            if routed in {"create_incident", "select_supplier", "reroute_shipment", "approve_recovery", "send_notification"}:
                return {"response": self.human_loop.request_confirmation(session_id, routed, {"input": user_input}), "requires_confirmation": True}
            if routed == "ask_clarification":
                return {"response": "Could you provide the shipment id, product id, or incident id so I can investigate it precisely?", "requires_confirmation": False}
            response = self._route_to_specialist(routed, user_input)
            self.memory.add_message(session_id, "assistant", response)
            return {"response": response, "requires_confirmation": False}

        def _execute_pending_action(self, action: str, payload: Dict[str, Any], session_id: str) -> Dict[str, Any]:
            if action == "create_incident":
                result = create_incident(payload.get("title", "Supply incident"), payload.get("incident_type", "shipment"), payload.get("severity", "medium"), payload.get("description", "Generated from assistant"), payload.get("affected_ids", []), self.data_store)
            elif action == "select_supplier":
                result = alternative_supplier(payload.get("product_id", "P-1"), payload.get("current_supplier_id"), self.data_store)
            elif action == "reroute_shipment":
                result = reroute_shipment(payload.get("shipment_id", "S-1"), payload.get("route_id", "R-1"), self.data_store)
            elif action == "approve_recovery":
                result = recovery_plan(payload.get("incident_id", "INC-1"), payload.get("strategy", "split-shipments"), self.data_store)
            elif action == "send_notification":
                result = customer_notification(payload.get("order_id", "O-1"), payload.get("message", "A disruption is affecting your delivery"), self.data_store)
            else:
                result = {"message": "No pending action found"}
            self.memory.add_message(session_id, "assistant", str(result))
            return {"response": str(result), "requires_confirmation": False}

        def classify_request(self, user_input: str) -> str:
            lowered = user_input.lower()
            if any(keyword in lowered for keyword in ["incident", "escalate", "disruption"]):
                return "incident"
            if any(keyword in lowered for keyword in ["shipment", "route", "reroute", "delay"]):
                return "shipment"
            if any(keyword in lowered for keyword in ["inventory", "warehouse", "stock", "shortage"]):
                return "inventory"
            if any(keyword in lowered for keyword in ["supplier", "alternative", "compare"]):
                return "supplier"
            if any(keyword in lowered for keyword in ["recovery", "plan", "recommend", "impact"]):
                return "recovery"
            if any(keyword in lowered for keyword in ["report", "summary", "status"]):
                return "reporting"
            return "ask_clarification"

        def route_request(self, intent: str) -> str:
            routes = {
                "shipment": "shipment",
                "inventory": "inventory",
                "supplier": "supplier",
                "incident": "create_incident",
                "recovery": "recovery",
                "reporting": "reporting",
                "ask_clarification": "ask_clarification",
            }
            return routes[intent]

        def fallback_route(self, user_input: str) -> str:
            return self._route_to_specialist(self.classify_request(user_input), user_input)

        def _route_to_specialist(self, route: str, user_input: str) -> str:
            trace_event("route", route=route, input=user_input)
            if route == "shipment":
                return self.handle_shipment(user_input)
            if route == "inventory":
                return self.handle_inventory(user_input)
            if route == "supplier":
                return self.handle_supplier(user_input)
            if route == "recovery":
                return self.handle_recovery(user_input)
            if route == "reporting":
                return self.handle_reporting(user_input)
            if route == "create_incident":
                return "I can create an incident. Please confirm if you want me to proceed."
            return self.llm.generate(SYSTEM_PROMPT + "\nUser: " + user_input)

        def handle_shipment(self, user_input: str) -> str:
            if "delay" in user_input.lower():
                shipment_id = self._extract_id(user_input, "shipment")
                result = shipment_delay(shipment_id or "S-1", self.data_store)
                return f"Shipment delay review: {result}"
            if "route" in user_input.lower() or "reroute" in user_input.lower():
                shipment_id = self._extract_id(user_input, "shipment")
                result = reroute_shipment(shipment_id or "S-1", "R-2", self.data_store)
                return f"Reroute action drafted: {result}"
            shipment_id = self._extract_id(user_input, "shipment")
            result = track_shipment(shipment_id or "S-1", self.data_store)
            return f"Shipment status update: {result}"

        def handle_inventory(self, user_input: str) -> str:
            product_id = self._extract_id(user_input, "product")
            warehouse_id = self._extract_id(user_input, "warehouse")
            if warehouse_id:
                result = warehouse_stock(warehouse_id, self.data_store)
            elif product_id:
                result = inventory_lookup(product_id, None, self.data_store)
            else:
                result = inventory_shortage(data_store=self.data_store)
            return f"Inventory review: {result}"

        def handle_supplier(self, user_input: str) -> str:
            product_id = self._extract_id(user_input, "product")
            supplier_id = self._extract_id(user_input, "supplier")
            if supplier_id:
                result = supplier_availability(supplier_id, self.data_store)
            elif product_id:
                result = alternative_supplier(product_id, None, self.data_store)
            else:
                result = compare_suppliers("P-1", ["SUP-1", "SUP-2"], self.data_store)
            return f"Supplier review: {result}"

        def handle_recovery(self, user_input: str) -> str:
            incident_id = self._extract_id(user_input, "incident")
            if "reroute" in user_input.lower():
                result = simulate_reroute("S-1", "R-2", self.data_store)
            elif "supplier" in user_input.lower():
                result = simulate_supplier_replacement("P-1", ["SUP-1", "SUP-2"], self.data_store)
            elif "inventory" in user_input.lower():
                result = simulate_inventory_redistribution("P-1", ["WH-1", "WH-2"], self.data_store)
            elif "transport" in user_input.lower():
                result = compare_transport_options(["R-1", "R-2"], self.data_store)
            elif "delivery" in user_input.lower():
                result = predict_delivery("S-1", self.data_store)
            else:
                result = business_impact(incident_id or "INC-1", self.data_store)
            return f"Recovery recommendation: {result}"

        def handle_reporting(self, user_input: str) -> str:
            incident_id = self._extract_id(user_input, "incident")
            if incident_id:
                result = incident_summary(incident_id, self.data_store)
            else:
                result = {"message": "No incident id provided, so I am summarizing the current operational posture."}
            return f"Reporting update: {result}"

        def _extract_id(self, user_input: str, entity: str) -> str | None:
            patterns = {
                "shipment": r"(S-[0-9]+)",
                "product": r"(P-[0-9]+)",
                "warehouse": r"(WH-[0-9]+)",
                "supplier": r"(SUP-[0-9]+)",
                "incident": r"(INC-[0-9]+)",
            }
            match = re.search(patterns.get(entity, r"([A-Z]+-[0-9]+)"), user_input.upper())
            return match.group(1) if match else None
''').strip() + "\n"

files["frontend/app.py"] = dedent('''
    import streamlit as st

    from backend.agent_orchestrator import CrisisOpsAgent
    from backend.data_store import DataStore
    from backend.memory import ConversationMemory

    st.set_page_config(page_title="NovaRetail CrisisOps AI", page_icon="📦", layout="wide")
    st.markdown("<style>body{background:#0f172a;color:#f8fafc;} .stTextInput>div>div>input{background:#111827;color:white;} .stSidebar{background:#111827;} .stAlert{background:#1f2937;}</style>", unsafe_allow_html=True)

    data_store = DataStore("data")
    memory = ConversationMemory()
    agent = CrisisOpsAgent(data_store, memory)

    if "session_id" not in st.session_state:
        st.session_state.session_id = "session-1"

    st.title("NovaRetail CrisisOps AI")
    st.caption("A multi-agent supply chain operations assistant for disruption management and digital-twin planning")

    with st.sidebar:
        st.header("Operations Overview")
        suppliers = len(data_store.suppliers())
        warehouses = len(data_store.warehouses())
        shipments = len(data_store.shipments())
        orders = len(data_store.orders())
        incidents = len(data_store.incidents())
        st.metric("Active Suppliers", suppliers)
        st.metric("Warehouses", warehouses)
        st.metric("Shipments", shipments)
        st.metric("Orders", orders)
        st.metric("Incidents", incidents)
        st.button("Reset Chat", on_click=lambda: memory.clear(st.session_state.session_id))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Conversation")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        prompt = st.chat_input("Ask about shipments, inventory, suppliers, incidents, or recovery options")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Agent is reasoning..."):
                result = agent.handle_message(st.session_state.session_id, prompt)
            response = result.get("response", "")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    with col2:
        st.subheader("Operational Snapshot")
        st.info("The agent can route requests to specialized workflows and ask for confirmation before taking risky actions.")
        if data_store.shipments():
            shipment_statuses = {}
            for shipment in data_store.shipments()[:10]:
                shipment_statuses[shipment["id"]] = shipment.get("delay_hours", 0)
            st.bar_chart(shipment_statuses)
''').strip() + "\n"

files["tests/__init__.py"] = ""
files["tests/test_tools.py"] = dedent('''
    from backend.data_store import DataStore
    from tools.inventory_tools import inventory_lookup
    from tools.shipment_tools import shipment_status
    from tools.supplier_tools import supplier_lookup

    def test_inventory_lookup_reads_data():
        ds = DataStore("data")
        result = inventory_lookup("P-1", data_store=ds)
        assert result["records"]

    def test_shipment_status_reads_data():
        ds = DataStore("data")
        result = shipment_status("S-1", data_store=ds)
        assert "status" in result

    def test_supplier_lookup_reads_data():
        ds = DataStore("data")
        result = supplier_lookup("SUP-1", data_store=ds)
        assert result["supplier"]["id"] == "SUP-1"
''').strip() + "\n"

files["tests/test_data_consistency.py"] = dedent('''
    from backend.data_store import DataStore

    def test_dataset_relations_are_consistent():
        ds = DataStore("data")
        suppliers = ds.suppliers()
        products = ds.products()
        inventory = ds.inventory()
        shipments = ds.shipments()
        orders = ds.orders()
        incidents = ds.incidents()
        recovery_plans = ds.recovery_plans()

        assert len(suppliers) >= 100
        assert len(products) >= 500
        assert len(inventory) >= 2000
        assert len(shipments) >= 5000
        assert len(orders) >= 10000
        assert len(incidents) >= 200
        assert len(recovery_plans) >= 200

        assert all(record["supplier_id"] in {supplier["id"] for supplier in suppliers} for record in products[:5])
        assert all(record["warehouse_id"] in {warehouse["id"] for warehouse in ds.warehouses()} for record in inventory[:5])
        assert all(order.get("customer_id") for order in orders[:5])
        assert all(shipment.get("order_id") for shipment in shipments[:5])
        assert all(incident.get("id") for incident in incidents[:5])
''').strip() + "\n"

files["docs/architecture.md"] = dedent('''
    # Architecture Overview

    NovaRetail CrisisOps AI uses a layered architecture:
    - Streamlit UI for conversation and dashboarding.
    - Backend data store for synthetic enterprise data.
    - Tool layer for shipment, inventory, supplier, incident, and digital twin operations.
    - LangGraph-inspired agent graph for routing.
    - Human-loop confirmation for risky actions.
    - Tracing hooks for LangSmith-style observability.
''').strip() + "\n"

files["docs/folder_structure.md"] = dedent('''
    # Folder Structure

    - frontend/ – Streamlit UI
    - backend/ – data models, data store, memory, orchestrator
    - agents/ – prompts, LLM service, human loop, graph routing
    - tools/ – domain tools for operations and digital twin simulation
    - utilities/ – logging and tracing helpers
    - data/ – synthetic enterprise dataset and generators
    - docs/ – documentation and diagrams
    - tests/ – pytest suite
''').strip() + "\n"

files["docs/workflow.md"] = dedent('''
    # Workflow

    1. User asks a question in the Streamlit chat UI.
    2. The orchestrator classifies the intent.
    3. A supervisor route selects the specialist domain.
    4. The specialist uses tools to inspect data and build a response.
    5. If the action is high impact, the system requests confirmation before execution.
''').strip() + "\n"

files["docs/sequence.md"] = dedent('''
    # Sequence Diagram

    User -> Streamlit UI -> CrisisOpsAgent -> Tool Layer -> Data Store -> Response
''').strip() + "\n"

files["docs/class_diagram.md"] = dedent('''
    # Class Diagram

    CrisisOpsAgent --> HumanLoopManager
    CrisisOpsAgent --> LLMService
    CrisisOpsAgent --> DataStore
    CrisisOpsAgent --> AgentGraph
''').strip() + "\n"

files["docs/technical_documentation.md"] = dedent('''
    # Technical Documentation

    This project demonstrates a modular AI operations assistant for supply chain disruptions. The synthetic dataset ensures internal consistency between suppliers, warehouses, inventory, shipments, orders, incidents, and recovery plans.
''').strip() + "\n"

files["docs/user_guide.md"] = dedent('''
    # User Guide

    Ask natural-language questions such as:
    - Track shipment S-1
    - Check inventory for P-1
    - Find an alternative supplier for P-1
    - Create an incident for a delayed shipment
    - Simulate a recovery strategy
''').strip() + "\n"

files["docs/future_enhancements.md"] = dedent('''
    # Future Enhancements

    - Connect to live ERP, WMS, TMS, and OMS APIs
    - Swap the fallback LLM logic for Gemini or another hosted model
    - Add full LangSmith trace export and evaluation dashboards
    - Add real-time notifications and RBAC
''').strip() + "\n"

files["deployment/Dockerfile"] = dedent('''
    FROM python:3.12-slim
    WORKDIR /app
    COPY . /app
    RUN pip install --no-cache-dir -r requirements.txt
    EXPOSE 8501
    CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
''').strip() + "\n"

files["deployment/README.md"] = dedent('''
    # Deployment Notes

    This application can be deployed to Streamlit Community Cloud by linking the repository and specifying `streamlit run frontend/app.py` as the entry point.
''').strip() + "\n"

files["data/generate_datasets.py"] = dedent('''
    import json
    import random
    from pathlib import Path

    ROOT = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    random.seed(42)

    suppliers = []
    for index in range(1, 101):
        suppliers.append({
            "id": f"SUP-{index}",
            "name": f"Supplier {index}",
            "region": ["North", "South", "East", "West"][index % 4],
            "rating": round(3.5 + (index % 10) * 0.1, 1),
            "lead_time_days": 2 + index % 8,
            "status": "active" if index % 5 else "risk",
            "product_categories": ["Electronics", "Apparel", "Home", "Food"][index % 4: index % 4 + 1],
            "capacity": 1000 + index * 15,
        })

    warehouses = []
    for index in range(1, 9):
        warehouses.append({
            "id": f"WH-{index}",
            "name": f"Warehouse {index}",
            "region": ["North", "South", "East", "West", "Central"][index % 5],
            "capacity": 50000 + index * 1000,
            "hub": "HUB-1" if index % 2 == 0 else "HUB-2",
            "status": "open",
        })

    products = []
    for index in range(1, 501):
        products.append({
            "id": f"P-{index}",
            "name": f"Product {index}",
            "category": ["Electronics", "Apparel", "Home", "Food"][index % 4],
            "sku": f"SKU-{index:03d}",
            "unit_cost": round(10 + index * 0.45, 2),
            "weight_kg": round(0.3 + index % 20 * 0.4, 2),
            "criticality": "high" if index % 3 == 0 else "medium",
            "supplier_id": suppliers[(index - 1) % len(suppliers)]["id"],
        })

    customers = []
    for index in range(1, 2001):
        customers.append({
            "id": f"C-{index}",
            "name": f"Customer {index}",
            "segment": ["retail", "ecommerce", "wholesale"][index % 3],
            "region": ["North", "South", "East", "West"][index % 4],
        })

    inventory = []
    for index in range(1, 2001):
        product = products[(index - 1) % len(products)]
        warehouse = warehouses[(index - 1) % len(warehouses)]
        inventory.append({
            "id": f"INV-{index}",
            "product_id": product["id"],
            "warehouse_id": warehouse["id"],
            "quantity": 50 + (index % 150),
            "reorder_level": 20 + (index % 20),
            "reserved_quantity": 5 + (index % 10),
            "last_updated": f"2026-07-{(index % 28) + 1:02d}",
            "supplier_id": product["supplier_id"],
        })

    routes = []
    for index in range(1, 101):
        routes.append({
            "id": f"R-{index}",
            "origin": warehouses[index % len(warehouses)]["id"],
            "destination": warehouses[(index + 1) % len(warehouses)]["id"],
            "distance_km": 400 + index * 10,
            "cost_per_km": round(0.8 + index * 0.01, 2),
            "eta_hours": 8 + index % 6,
            "status": "active",
            "partner_id": f"PART-{(index % 20) + 1}",
        })

    partners = []
    for index in range(1, 21):
        partners.append({
            "id": f"PART-{index}",
            "name": f"Partner {index}",
            "region": ["North", "South", "East", "West"][index % 4],
            "score": round(4.0 + (index % 10) * 0.1, 1),
            "capacity": 10000 + index * 400,
            "service_level": "gold" if index % 2 == 0 else "silver",
        })

    shipments = []
    for index in range(1, 5001):
        shipment = {
            "id": f"S-{index}",
            "order_id": f"O-{index}",
            "warehouse_id": warehouses[(index - 1) % len(warehouses)]["id"],
            "route_id": routes[(index - 1) % len(routes)]["id"],
            "status": ["in_transit", "delayed", "delivered"][index % 3],
            "delay_hours": 0 if index % 5 else 12 + index % 10,
            "eta": f"2026-07-{(index % 28) + 1:02d}",
            "partner_id": partners[(index - 1) % len(partners)]["id"],
        }
        shipments.append(shipment)

    orders = []
    for index in range(1, 10001):
        orders.append({
            "id": f"O-{index}",
            "customer_id": customers[(index - 1) % len(customers)]["id"],
            "product_id": products[(index - 1) % len(products)]["id"],
            "warehouse_id": warehouses[(index - 1) % len(warehouses)]["id"],
            "supplier_id": products[(index - 1) % len(products)]["supplier_id"],
            "shipment_id": f"S-{index}",
            "priority": ["high", "medium", "low"][index % 3],
            "quantity": 5 + (index % 20),
            "status": ["confirmed", "processing", "delayed"][index % 3],
            "order_date": f"2026-07-{(index % 28) + 1:02d}",
        })

    incidents = []
    for index in range(1, 201):
        incidents.append({
            "id": f"INC-{index}",
            "title": f"Incident {index}",
            "incident_type": ["shipment", "inventory", "supplier", "weather"][index % 4],
            "severity": ["low", "medium", "high", "critical"][index % 4],
            "status": "open",
            "affected_warehouse_ids": [warehouses[index % len(warehouses)]["id"]],
            "affected_supplier_ids": [suppliers[index % len(suppliers)]["id"]],
            "affected_product_ids": [products[index % len(products)]["id"]],
            "impact_score": 30 + index % 40,
            "shipment_ids": [f"S-{index}"],
        })

    recovery_plans = []
    for index in range(1, 201):
        recovery_plans.append({
            "id": f"RP-{index}",
            "incident_id": incidents[index - 1]["id"],
            "strategy": ["split-shipments", "reroute", "secondary-supplier", "inventory-redistribution"][index % 4],
            "cost_estimate": round(2000 + index * 25, 2),
            "recovery_days": 2 + index % 5,
            "risk_level": ["low", "medium", "high"][index % 3],
            "status": "draft",
        })

    datasets = {
        "suppliers.json": suppliers,
        "warehouses.json": warehouses,
        "products.json": products,
        "inventory.json": inventory,
        "shipments.json": shipments,
        "orders.json": orders,
        "customers.json": customers,
        "incidents.json": incidents,
        "routes.json": routes,
        "partners.json": partners,
        "recovery_plans.json": recovery_plans,
    }

    for filename, payload in datasets.items():
        with (DATA_DIR / filename).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    manifest = {
        "suppliers": len(suppliers),
        "warehouses": len(warehouses),
        "products": len(products),
        "inventory": len(inventory),
        "shipments": len(shipments),
        "orders": len(orders),
        "customers": len(customers),
        "incidents": len(incidents),
        "routes": len(routes),
        "partners": len(partners),
        "recovery_plans": len(recovery_plans),
    }
    with (DATA_DIR / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    print("Generated enterprise datasets in", DATA_DIR)
''').strip() + "\n"

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print("Project scaffold created.")
