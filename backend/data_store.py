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
