import pytest
from run import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200, "Expected status code 200 but got {}".format(response.status_code)
