import pytest
from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_customer_generator_index_contains_keywords(client):
    response = client.get('/')
    data = response.data.decode()
    print(data)  # Add this line to debug what is actually returned
    assert "Customer Generator" in data
