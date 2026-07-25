import re
from typing import Any, Dict

from agents.graph import AgentGraph
from agents.human_loop import HumanLoopManager
from agents.llm_service import LLMService
from agents.prompts import SYSTEM_PROMPT
from backend.data_store import DataStore
from backend.memory import ConversationMemory
from tools.digital_twin import business_impact, compare_transport_options, predict_delivery, simulate_inventory_redistribution, simulate_reroute, simulate_supplier_replacement
from tools.incident_tools import create_incident, incident_summary, recovery_plan
from tools.inventory_tools import inventory_lookup, inventory_shortage, warehouse_stock
from tools.shipment_tools import customer_notification, reroute_shipment, shipment_delay, track_shipment
from tools.supplier_tools import alternative_supplier, compare_suppliers, supplier_availability
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
