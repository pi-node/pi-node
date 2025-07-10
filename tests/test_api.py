import pytest
from fastapi.testclient import TestClient
from src.api import app

# Create a test client for the FastAPI app
client = TestClient(app)

@pytest.fixture(scope="module")
def create_user():
    """Fixture to create a user for testing."""
    return {
        "username": "user",
        "password": "test_password"
    }

@pytest.fixture(scope="module")
def token(create_user):
    """Fixture to log in and get a token for authenticated requests."""
    response = client.post("/token", data={"username": create_user["username"], "password": create_user["password"]})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_login(create_user):
    """Test user login and token generation."""
    response = client.post("/token", data={"username": create_user["username"], "password": create_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_address(token):
    """Test creating a new wallet address."""
    response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "address" in response.json()
    assert "balance" in response.json()

def test_get_addresses(token):
    """Test retrieving all wallet addresses."""
    response = client.get("/addresses", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_balance(token):
    """Test getting the balance of a specific address."""
    address_response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    address = address_response.json()["address"]

    response = client.get(f"/balance/{address}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == 0.0  # New address should have a balance of 0

def test_create_transaction(token):
    """Test creating a transaction."""
    address1_response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    address1 = address1_response.json()["address"]
    address2_response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    address2 = address2_response.json()["address"]

    # Fund address1
    client.post("/transactions", json={"from_address": address1, "to_address": address2, "amount": 50.0}, headers={"Authorization": f"Bearer {token}"})

    response = client.post("/transactions", json={"from_address": address1, "to_address": address2, "amount": 10.0}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_transaction_insufficient_balance(token):
    """Test that a transaction fails with insufficient balance."""
    address1_response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    address1 = address1_response.json()["address"]
    address2_response = client.post("/addresses", headers={"Authorization": f"Bearer {token}"})
    address2 = address2_response.json()["address"]

    response = client.post("/transactions", json={"from_address": address1, "to_address": address2, "amount": 100.0}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance."

def test_save_and_load_wallet(token):
    """Test saving and loading the wallet."""
    save_response = client.post("/save", headers={"Authorization": f"Bearer {token}"})
    assert save_response.status_code == 200
    assert save_response.json()["message"] == "Wallet saved successfully"

    load_response = client.post("/load", headers={"Authorization": f"Bearer {token}"})
    assert load_response.status_code == 200
    assert load_response.json()["message"] == "Wallet loaded successfully"

def test_get_balance_nonexistent_address(token):
    """Test getting the balance of a nonexistent address."""
    response = client.get("/balance/nonexistent_address", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

def test_create_address_without_token():
    """Test creating an address without authentication."""
    response = client.post("/addresses")
    assert response.status_code == 403  # Forbidden

def test_login_with_invalid_credentials(create_user):
    """Test login with invalid credentials."""
    response = client.post("/token", data={"username": create_user["username"], "password": "wrong_password"})
    assert response.status_code == 400
    assert "detail" in response.json()

if __name__ == "__main__":
    pytest.main()
