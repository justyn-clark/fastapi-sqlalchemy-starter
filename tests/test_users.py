from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import auth, users


def test_app_health():
    """Test that the app starts up correctly"""
    # Create a minimal test app without database operations
    test_app = FastAPI()
    test_app.include_router(auth.router)
    test_app.include_router(users.router)
    
    with TestClient(test_app) as client:
        # Test that the app responds to a simple request
        res = client.get("/docs")
        assert res.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is generated correctly"""
    # Create a minimal test app without database operations
    test_app = FastAPI()
    test_app.include_router(auth.router)
    test_app.include_router(users.router)
    
    with TestClient(test_app) as client:
        res = client.get("/openapi.json")
        assert res.status_code == 200
        schema = res.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "FastAPI"
