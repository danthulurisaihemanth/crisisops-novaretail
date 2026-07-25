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
