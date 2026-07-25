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
