import json

from fastapi.testclient import TestClient

from app.main import app

if __name__ == "__main__":
    with TestClient(app) as client:
        resp = client.get("/openapi.json")
        resp.raise_for_status()
        spec = resp.json()
    with open("docs/openapi.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print("Exported to docs/openapi.json")
