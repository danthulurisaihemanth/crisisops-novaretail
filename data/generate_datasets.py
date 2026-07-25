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
