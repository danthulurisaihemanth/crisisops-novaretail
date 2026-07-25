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
