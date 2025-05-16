import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_expense():
    return {
        "title": "Test Lunch",
        "amount": 23.5,
        "category": "Food",
        "date": "2024-05-01",
        "notes": "Team lunch"
    }

def test_create_expense(sample_expense):
    response = client.post("/api/v1/expenses", json=sample_expense)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_expense["title"]
    assert data["amount"] == sample_expense["amount"]

def test_get_all_expenses():
    response = client.get("/api/v1/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_expense_by_id(sample_expense):
    create_resp = client.post("/api/v1/expenses", json=sample_expense)
    expense_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["id"] == expense_id

def test_update_expense(sample_expense):
    create_resp = client.post("/api/v1/expenses", json=sample_expense)
    expense_id = create_resp.json()["id"]
    updated_data = {"amount": 30.0, "notes": "Updated"}
    response = client.put(f"/api/v1/expenses/{expense_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["amount"] == 30.0
    assert response.json()["notes"] == "Updated"

def test_delete_expense(sample_expense):
    create_resp = client.post("/api/v1/expenses", json=sample_expense)
    expense_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/expenses/{expense_id}")
    assert response.status_code == 204
    get_resp = client.get(f"/api/v1/expenses/{expense_id}")
    assert get_resp.status_code == 404

def test_create_expense_invalid_data():
    invalid_data = {
        "title": "",
        "amount": -50,
        "category": "",
        "date": "invalid-date"
    }
    response = client.post("/api/v1/expenses", json=invalid_data)
    assert response.status_code == 422

def test_filter_expenses_by_category(sample_expense):
    client.post("/api/v1/expenses", json=sample_expense)
    response = client.get("/api/v1/expenses?category=Food")
    assert response.status_code == 200
    for expense in response.json():
        assert expense["category"] == "Food"

def test_filter_expenses_by_date_range():
    for i in range(3):
        client.post("/api/v1/expenses", json={
            "title": f"Expense {i}",
            "amount": 10,
            "category": "General",
            "date": f"2024-05-0{i+1}"
        })
    response = client.get("/api/v1/expenses?start_date=2024-05-01&end_date=2024-05-02")
    assert response.status_code == 200
    for exp in response.json():
        assert "2024-05-01" <= exp["date"] <= "2024-05-02"

def test_search_by_title():
    client.post("/api/v1/expenses", json={
        "title": "Groceries at Market",
        "amount": 50,
        "category": "Groceries",
        "date": "2024-05-03"
    })
    response = client.get("/api/v1/expenses?search=Market")
    assert response.status_code == 200
    assert any("Market" in exp["title"] for exp in response.json())

def test_pagination():
    for i in range(10):
        client.post("/api/v1/expenses", json={
            "title": f"Expense {i}",
            "amount": i + 1,
            "category": "Misc",
            "date": "2024-05-01"
        })
    response = client.get("/api/v1/expenses?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) <= 5

def test_sorting():
    response = client.get("/api/v1/expenses?sort=amount_desc")
    assert response.status_code == 200
    data = response.json()
    if len(data) >= 2:
        assert data[0]["amount"] >= data[1]["amount"]

def test_total_expense_summary():
    client.post("/api/v1/expenses", json={
        "title": "Item A",
        "amount": 40,
        "category": "Office",
        "date": "2024-05-04"
    })
    client.post("/api/v1/expenses", json={
        "title": "Item B",
        "amount": 60,
        "category": "Office",
        "date": "2024-05-04"
    })
    response = client.get("/api/v1/expenses/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total"] >= 100
