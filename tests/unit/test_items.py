from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


def test_add_item() -> None:
    payload = {"name": "bread", "category": "food", "quantity": 2}
    response: Response = client.post("/api/items", json=payload)
    assert response.status_code == 201
    assert response.json() == {
        "status": "created",
        "item": {"id": 1, "name": "bread", "category": "food", "quantity": 2},
    }


def test_add_item_bad_quantity() -> None:
    payload = {"name": "bread", "category": "food", "quantity": 0}
    response: Response = client.post("/api/items", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity must be greater than 0."}


def test_get_items() -> None:
    response: Response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "items": [{"id": 1, "name": "bread", "category": "food", "quantity": 2}],
    }


def test_get_item() -> None:
    response: Response = client.get("/api/items/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "item": {"id": 1, "name": "bread", "category": "food", "quantity": 2},
    }


def test_get_item_no_item() -> None:
    response: Response = client.get("/api/items/1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No item with id: 1000 found."}


def test_update_item() -> None:
    payload = {"name": "bread", "category": "food", "quantity": 3}
    response: Response = client.patch("/api/items/1", json=payload)
    assert response.status_code == 202
    assert response.json() == {
        "status": "accepted",
        "item": {"id": 1, "name": "bread", "category": "food", "quantity": 3},
    }


def test_update_item_no_item() -> None:
    payload = {"name": "bread", "category": "food", "quantity": 3}
    response: Response = client.patch("/api/items/1000", json=payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "No item with id: 1000 found."}


def test_update_item_bad_quantity() -> None:
    payload = {"name": "bread", "category": "food", "quantity": -1}
    response: Response = client.patch("/api/items/1", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity must not be less than 0."}


def test_delete_item() -> None:
    response: Response = client.delete("/api/items/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "deleted",
        "message": "Item deleted successfully.",
    }


def test_delete_item_no_item() -> None:
    response: Response = client.delete("/api/items/1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No item with id: 1000 found."}
