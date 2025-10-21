import json
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient

from app.main import app

if __name__ == "__main__":
    # Ensure docs directory exists
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    with TestClient(app) as client:
        resp = client.get("/openapi.json")
        resp.raise_for_status()
        spec = resp.json()
    with open("docs/openapi.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print("Exported to docs/openapi.json")
