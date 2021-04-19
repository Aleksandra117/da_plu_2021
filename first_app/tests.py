from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello world!"}

def test_method():
	response = client.post(f"/method")
	assert response.status_code == 201
	assert response.json() == {"method": "POST"}